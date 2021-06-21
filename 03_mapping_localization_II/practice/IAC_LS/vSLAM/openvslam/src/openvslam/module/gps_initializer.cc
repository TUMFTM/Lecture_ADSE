#include "openvslam/mapping_module.h"
#include "openvslam/data/keyframe.h"
#include "openvslam/data/landmark.h"
#include "openvslam/data/map_database.h"
#include "openvslam/module/gps_initializer.h"
#include "openvslam/gps/data.h"
#include "openvslam/solve/sim3_solver.h"

#include <spdlog/spdlog.h>
#include <iostream>
namespace openvslam {
namespace module {

gps_initializer::gps_initializer(data::map_database* map_db)
    : map_db_(map_db) {
    spdlog::debug("CONSTRUCT: module::gps_initializer");
}

void gps_initializer::set_mapping_module(mapping_module* mapper) {
    mapper_ = mapper;
}

void gps_initializer::enable_gps_initializer() {
    is_initializer_enabled_ = true;
}

void gps_initializer::disable_gps_initializer() {
    is_initializer_enabled_ = false;
}

bool gps_initializer::is_enabled() const {
    return is_initializer_enabled_;
}

void mean_of_eigen_vec(const eigen_alloc_vector<Vec3_t>& in_vec,
                       Vec3_t& mean) {
    mean.setZero();
    for (size_t i = 0; i < in_vec.size(); ++i) {
        for (int j = 0; j < 3; ++j) {
            mean[j] += in_vec[i][j];
        }
    }
    const double nr_els = static_cast<double>(in_vec.size());
    for (int j = 0; j < 3; ++j) {
        mean[j] /= nr_els;
    }
}

bool gps_initializer::start_map_scale_initalization() {

    if (!is_initializer_enabled_) {
        return false;
    }
    if (map_scale_initialized_) {
        return true;
    }
    // loop all keyframes and start it
    auto kfs = map_db_->get_all_keyframes();
    eigen_alloc_vector<Vec3_t> gps_pos;
    std::vector<double> sigma;
    eigen_alloc_vector<Vec3_t> cam_pos;

    for (auto kf : kfs) {
        const auto gps = kf->get_gps_data();
        if (gps.fix_ == gps::gps_fix_state_t::FIX_3D) {
            gps_pos.push_back(gps.scaled_xyz_);
            cam_pos.push_back(kf->get_cam_center());
        }
    }

    if (gps_pos.size() == 0 || cam_pos.size() == 0) {
        std::cout << "no gps pos" << std::endl;
        return false;
    }

    // now calculate scale
    Vec3_t mean_gps;
    Vec3_t mean_cam;
    mean_of_eigen_vec(gps_pos, mean_gps);
    mean_of_eigen_vec(cam_pos, mean_cam);

    double sum_gps_diff = 0.0;
    double sum_cam_diff = 0.0;
    for (size_t i = 0; i < gps_pos.size(); ++i) {
        sum_gps_diff += (gps_pos[i] - mean_gps).squaredNorm();
        sum_cam_diff += (cam_pos[i] - mean_cam).squaredNorm();
    }
    const double scale = std::sqrt(sum_gps_diff/sum_cam_diff);
    const double diff_to_last = std::abs(last_scale_estimate_ - scale) / last_scale_estimate_;
    last_scale_estimate_ = scale;
    std::cout<<"Estimated scale: "<<scale<<std::endl;
    std::cout<<"Diff to last estimate: "<<diff_to_last<<std::endl;
    if (diff_to_last > 1e-2) {
        return false;
    }
    double total_distance_traveled = 0.0;
    // calculate traveled distance
    //for (size_t i = 1; i < gps_pos.size(); ++i) {
    total_distance_traveled = (gps_pos[gps_pos.size()-1]-gps_pos[0]).norm() * gps_scaler;
    //}

    if (total_distance_traveled < min_traveled_distance_) {
        state_ = gps_initializer_state_t::AwaitingScaleInit;
        std::cout<<"total_distance_traveled not big enough: "<<total_distance_traveled<<"m"<<std::endl;
        return false;
    }

    // scale map
    // stop all threads and scale the map
    {
        std::lock_guard<std::mutex> lock(mtx_thread_);
        gps_scaling_is_running_ = true;
        abort_gps_scaling_ = false;
    }
    // stop mapping module
    mapper_->request_pause();
    while (!mapper_->is_paused() && !mapper_->is_terminated()) {
        std::this_thread::sleep_for(std::chrono::microseconds(50));
    }
    // lock the map
    std::lock_guard<std::mutex> lock2(data::map_database::mtx_database_);

    auto landmarks = map_db_->get_all_landmarks();
    for (auto lm : landmarks) {
        if (!lm) {
            continue;
        }
        lm->set_pos_in_world(lm->get_pos_in_world() * scale);
    }
    for (auto kf : kfs) {
        if (kf->id_ != 0) {
            Mat44_t cam_pose_cw = kf->get_cam_pose();
            cam_pose_cw.block<3, 1>(0, 3) *= scale;
            kf->set_cam_pose(cam_pose_cw);
        }
    }
    state_ = gps_initializer_state_t::ScaleInitSucceeded;
    // finished scaling return to normal behaviour
    mapper_->resume();

    gps_scaling_is_running_ = false;
    map_scale_initialized_ = true;
    spdlog::info("scaled the map with gps measurements");
    return true;
}

bool gps_initializer::start_map_rotation_initalization() {
    if (!is_initializer_enabled_) {
        return false;
    }

    if (map_alignment_initialized_) {
        return true;
    }

    // loop all keyframes and start it
    auto kfs = map_db_->get_all_keyframes();
    eigen_alloc_vector<Vec3_t> gps_pos;
    std::vector<double> sigma;
    eigen_alloc_vector<Vec3_t> cam_pos;

    for (auto kf : kfs) {
        const auto gps = kf->get_gps_data();
        if (gps.fix_ == gps::gps_fix_state_t::FIX_3D) {
            gps_pos.push_back(gps.scaled_xyz_);
            cam_pos.push_back(kf->get_cam_center());
        }
    }
    const unsigned int min_num_inliers = 5;
    const double max_chi2_sqrt = 0.15 / gps_scaler;
    const double min_lambda2 = 1.0 / gps_scaler;
    solve::sim3_solver solver(gps_pos, cam_pos, false,
                              min_num_inliers, max_chi2_sqrt, min_lambda2);
    unsigned int nr_inliers = solver.find_pcl_alignment(200, 6);
    // we get 2->1 which is gps -> cam, but we nedd cam -> gps system
    const Mat33_t R_cam_to_gps = solver.get_best_rotation_12();
    const double s_cam_to_gps = solver.get_best_scale_12();
    const Vec3_t t_cam_to_gps = solver.get_best_translation_12();

    if (nr_inliers < min_num_inliers) {
        std::cout<<"Not enough inliers for rotation initialization..."<<std::endl;
        std::cout<<"Found only "<<nr_inliers<<" correspondences.\n";
        return false;
    }

    std::cout<<"R_cam_to_gps: "<<R_cam_to_gps<<std::endl;
    std::cout<<"s_cam_to_gps: "<<s_cam_to_gps<<std::endl;
    std::cout<<"t_cam_to_gps: "<<t_cam_to_gps<<std::endl;
    std::cout<<"nr_inliers: "<<nr_inliers<<std::endl;
    const double inlier_percent = static_cast<double>(nr_inliers)/gps_pos.size();
    std::cout<<"nr_inliers/gps_pos.size: "<<inlier_percent<<std::endl;

    // scale map
    // stop all threads and scale the map
    {
        std::lock_guard<std::mutex> lock(mtx_thread_);
        gps_scaling_is_running_ = true;
        abort_gps_scaling_ = false;
    }
    // stop mapping module
    mapper_->request_pause();
    while (!mapper_->is_paused() && !mapper_->is_terminated()) {
        std::this_thread::sleep_for(std::chrono::microseconds(50));
    }
    // lock the map
    std::lock_guard<std::mutex> lock2(data::map_database::mtx_database_);

    auto landmarks = map_db_->get_all_landmarks();
    for (auto lm : landmarks) {
        if (!lm) {
            continue;
        }
        lm->set_pos_in_world(s_cam_to_gps * R_cam_to_gps * lm->get_pos_in_world() + t_cam_to_gps);
    }

    for (auto kf : kfs) {
        //if (kf->id_ != 0) {
//        g2o::Sim3 sim3;
//        ret.r = r*other.r;
//        ret.t=s*(r*other.t)+t;
//        ret.s=s*other.s;
        Mat33_t R_cam = kf->get_rotation().transpose();
        Vec3_t X_cam = kf->get_cam_center();
        Mat44_t new_cam_pos = Mat44_t::Identity();
        new_cam_pos.block<3,3>(0,0) = (R_cam_to_gps * R_cam);
        new_cam_pos.block<3,1>(0,3) = s_cam_to_gps * (R_cam_to_gps * X_cam) + t_cam_to_gps;
        kf->set_cam_pose(new_cam_pos.inverse());
        //}
    }
    state_ = gps_initializer_state_t::ScaleInitSucceeded;
    // finished scaling return to normal behaviour
    mapper_->resume();

    gps_scaling_is_running_ = false;
    map_alignment_initialized_ = true;
    spdlog::info("rotation and translation initialized");

    return true;
}

void gps_initializer::abort() {
    std::lock_guard<std::mutex> lock(mtx_thread_);
    abort_gps_scaling_ = true;
}

bool gps_initializer::is_running() const {
    std::lock_guard<std::mutex> lock(mtx_thread_);
    return gps_scaling_is_running_;
}

bool gps_initializer::is_map_scale_initialized() const {
    return map_scale_initialized_;
}

}
}
