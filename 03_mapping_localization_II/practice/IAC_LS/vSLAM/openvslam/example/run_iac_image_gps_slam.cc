#include "util/image_util.h"

#ifdef USE_PANGOLIN_VIEWER
#include "pangolin_viewer/viewer.h"
#elif USE_SOCKET_PUBLISHER
#include "socket_publisher/publisher.h"
#endif

#include <math.h>

#include "openvslam/system.h"
#include "openvslam/config.h"

#include <iostream>
#include <chrono>
#include <numeric>

#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/core/affine.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/core/eigen.hpp>
#include <spdlog/spdlog.h>
#include <popl.hpp>

#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <string>
#include <algorithm>
#include <boost/algorithm/string.hpp>
#include <openvslam/gps/config.h>

#ifdef USE_STACK_TRACE_LOGGER
#include <glog/logging.h>
#endif

#ifdef USE_GOOGLE_PERFTOOLS
#include <gperftools/profiler.h>
#endif

void mono_tracking(const std::shared_ptr<openvslam::config>& cfg,
                   const std::string& vocab_file_path, const std::string& image_dir_path, const std::string& mask_img_path,
                   const std::string& ground_truth_path, const unsigned int frame_skip, const bool no_sleep, const bool auto_term,
                   const bool eval_log, const std::string& map_db_path) {
    // load the mask image
    const cv::Mat mask = mask_img_path.empty() ? cv::Mat{} : cv::imread(mask_img_path, cv::IMREAD_GRAYSCALE);

    const image_sequence sequence(image_dir_path, cfg->camera_->fps_);
    const auto frames = sequence.get_frames();

    // load ground truth data
    std::vector<openvslam::gps::data> iac_gps_data;

    // read csv
    std::cout << "reading ground truth data from csv: " << ground_truth_path << std::endl;
    std::ifstream file(ground_truth_path);
    std::string line;

    // Iterate through each line and split the content using delimiter
    while (getline(file, line))
    {
        // do not read first line
        if (boost::algorithm::contains(line, "time")) {
            continue;
        }

        std::vector<std::string> vec;
        boost::algorithm::split(vec, line, boost::is_any_of(","));

        float ts = std::stof(vec.at(0)) - 12.0; // deleted first 12 seconds from images and imu data
        float x = std::stof(vec.at(7));
        float y = std::stof(vec.at(9));
        float z = std::stof(vec.at(8));
        float precision = std::stof(vec.at(10));
        float velocity = std::stof(vec.at(11));

        iac_gps_data.push_back(
            openvslam::gps::data(
                x,  // latitude
                y,  // longitude
                z,  // height
                precision, // precision
                static_cast<const openvslam::gps::gps_fix_state_t>(3),       // fix
                velocity,  // speed 2d
                velocity,  // speed 3d
                ts));      // timestamp
    }
    file.close();

    // configure gps
    const double gps_hz = 1.0 / (iac_gps_data[1].ts_ - iac_gps_data[0].ts_);
    openvslam::gps::config gps_config("iac_gps", gps_hz, openvslam::Mat44_t::Identity());

    // build a SLAM system
    openvslam::system SLAM(cfg, vocab_file_path);
    // startup the SLAM process
    SLAM.startup();
    SLAM.set_use_gps_data();

#ifdef USE_PANGOLIN_VIEWER
    pangolin_viewer::viewer viewer(cfg, &SLAM, SLAM.get_frame_publisher(), SLAM.get_map_publisher());
#elif USE_SOCKET_PUBLISHER
    socket_publisher::publisher publisher(cfg, &SLAM, SLAM.get_frame_publisher(), SLAM.get_map_publisher());
#endif

    std::vector<double> track_times;
    track_times.reserve(frames.size());


    unsigned int num_kfs_last_global_optim = 0;

    // run the SLAM in another thread
    std::thread thread([&]() {
        for (unsigned int i = 0; i < frames.size(); ++i) {
            const auto& frame = frames.at(i);
            const auto img = cv::imread(frame.img_path_, cv::IMREAD_UNCHANGED);

            const auto tp_1 = std::chrono::steady_clock::now();

            //std::cout << img.size << std::endl;

            if (!img.empty() && (i % frame_skip == 0)) {

                openvslam::gps::data frame_gps_data;
                int gps_id = 0;
                while (frame.timestamp_ >= iac_gps_data[gps_id].ts_) {
                    frame_gps_data = iac_gps_data[gps_id];
                    gps_id++;
                }
                frame_gps_data.ts_ = frame.timestamp_;
                SLAM.feed_GPS_data(frame_gps_data);

                // input the current frame and estimate the camera pose
                SLAM.feed_monocular_frame(img, frame.timestamp_, mask);

            }

            const auto tp_2 = std::chrono::steady_clock::now();

            const auto track_time = std::chrono::duration_cast<std::chrono::duration<double>>(tp_2 - tp_1).count();
            if (i % frame_skip == 0) {
                track_times.push_back(track_time);
            }

            // wait until the timestamp of the next frame
            if (!no_sleep && i < frames.size() - 1) {
                const auto wait_time = frames.at(i + 1).timestamp_ - (frame.timestamp_ + track_time);
                if (0.0 < wait_time) {
                    std::this_thread::sleep_for(std::chrono::microseconds(static_cast<unsigned int>(wait_time * 1e6)));
                }
            }

            // check if the termination of SLAM system is requested or not
            if (SLAM.terminate_is_requested()) {
                break;
            }

            while (SLAM.is_local_ba_running()) {
                std::this_thread::sleep_for(std::chrono::microseconds(5));
            }
            if (SLAM.is_gps_initialized()) {
                const unsigned int cur_nr_kfs = SLAM.get_current_nr_kfs();
                if ((cur_nr_kfs - num_kfs_last_global_optim) > 30) {
                    num_kfs_last_global_optim = cur_nr_kfs;
                    SLAM.request_global_GPS_optim();
                    std::this_thread::sleep_for(std::chrono::microseconds(10));
                }
            }
            // wait until the loop BA is finished
            while (SLAM.global_GPS_optim_is_running()) {
                std::this_thread::sleep_for(std::chrono::microseconds(250));
            }
        }

        // wait until the loop BA is finished
        while (SLAM.loop_BA_is_running()) {
            std::this_thread::sleep_for(std::chrono::microseconds(5000));
        }

        // automatically close the viewer
#ifdef USE_PANGOLIN_VIEWER
        if (auto_term) {
            viewer.request_terminate();
        }
#elif USE_SOCKET_PUBLISHER
        if (auto_term) {
            publisher.request_terminate();
        }
#endif
    });

    // run the viewer in the current thread
#ifdef USE_PANGOLIN_VIEWER
    viewer.run();
#elif USE_SOCKET_PUBLISHER
    publisher.run();
#endif

    thread.join();

    // shutdown the SLAM process
    SLAM.shutdown();

    if (eval_log) {
        // output the trajectories for evaluation
        SLAM.save_frame_trajectory("frame_trajectory.txt", "TUM");
        SLAM.save_keyframe_trajectory("keyframe_trajectory.txt", "TUM");
        // output the tracking times for evaluation
        std::ofstream ofs("track_times.txt", std::ios::out);
        if (ofs.is_open()) {
            for (const auto track_time : track_times) {
                ofs << track_time << std::endl;
            }
            ofs.close();
        }
    }

    if (!map_db_path.empty()) {
        // output the map database
        SLAM.save_map_database(map_db_path);
    }

    std::sort(track_times.begin(), track_times.end());
    const auto total_track_time = std::accumulate(track_times.begin(), track_times.end(), 0.0);
    std::cout << "median tracking time: " << track_times.at(track_times.size() / 2) << "[s]" << std::endl;
    std::cout << "mean tracking time: " << total_track_time / track_times.size() << "[s]" << std::endl;
}

int main(int argc, char* argv[]) {
#ifdef USE_STACK_TRACE_LOGGER
    google::InitGoogleLogging(argv[0]);
    google::InstallFailureSignalHandler();
#endif

    // create options
    popl::OptionParser op("Allowed options");
    auto help = op.add<popl::Switch>("h", "help", "produce help message");
    auto vocab_file_path = op.add<popl::Value<std::string>>("v", "vocab", "vocabulary file path");
    auto img_dir_path = op.add<popl::Value<std::string>>("i", "img-dir", "directory path which contains images");
    auto config_file_path = op.add<popl::Value<std::string>>("c", "config", "config file path");
    auto mask_img_path = op.add<popl::Value<std::string>>("", "mask", "mask image path", "");
    auto ground_truth_path = op.add<popl::Value<std::string>>("g", "ground-truth", "ground truth xml file path");
    auto frame_skip = op.add<popl::Value<unsigned int>>("", "frame-skip", "interval of frame skip", 1);
    auto no_sleep = op.add<popl::Switch>("", "no-sleep", "not wait for next frame in real time");
    auto auto_term = op.add<popl::Switch>("", "auto-term", "automatically terminate the viewer");
    auto debug_mode = op.add<popl::Switch>("", "debug", "debug mode");
    auto eval_log = op.add<popl::Switch>("", "eval-log", "store trajectory and tracking times for evaluation");
    auto map_db_path = op.add<popl::Value<std::string>>("p", "map-db", "store a map database at this path after SLAM", "");
    try {
        op.parse(argc, argv);
    }
    catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        std::cerr << std::endl;
        std::cerr << op << std::endl;
        return EXIT_FAILURE;
    }

    // check validness of options
    if (help->is_set()) {
        std::cerr << op << std::endl;
        return EXIT_FAILURE;
    }
    if (!vocab_file_path->is_set() || !img_dir_path->is_set() || !config_file_path->is_set()) {
        std::cerr << "invalid arguments" << std::endl;
        std::cerr << std::endl;
        std::cerr << op << std::endl;
        return EXIT_FAILURE;
    }

    // setup logger
    spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e] %^[%L] %v%$");
    if (debug_mode->is_set()) {
        spdlog::set_level(spdlog::level::debug);
    }
    else {
        spdlog::set_level(spdlog::level::info);
    }

    // load configuration
    std::shared_ptr<openvslam::config> cfg;
    try {
        cfg = std::make_shared<openvslam::config>(config_file_path->value());
    }
    catch (const std::exception& e) {
        std::cout << config_file_path->value() << std::endl;
        std::cerr << e.what() << std::endl;
        return EXIT_FAILURE;
    }

#ifdef USE_GOOGLE_PERFTOOLS
    ProfilerStart("slam.prof");
#endif

    // run tracking
    if (cfg->camera_->setup_type_ == openvslam::camera::setup_type_t::Monocular) {
        mono_tracking(cfg, vocab_file_path->value(), img_dir_path->value(), mask_img_path->value(),
                      ground_truth_path->value(), frame_skip->value(), no_sleep->is_set(), auto_term->is_set(),
                      eval_log->is_set(), map_db_path->value());
    }
    else {
        throw std::runtime_error("Invalid setup type: " + cfg->camera_->get_setup_type_string());
    }

#ifdef USE_GOOGLE_PERFTOOLS
    ProfilerStop();
#endif

    return EXIT_SUCCESS;
}
