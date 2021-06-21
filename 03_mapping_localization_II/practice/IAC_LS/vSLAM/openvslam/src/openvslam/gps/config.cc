// created by Steffen Urban April 2020, urbste@gmail.com
#include "openvslam/gps/config.h"

namespace openvslam {
namespace gps {

config::config(const std::string& name, const double rate_hz, const Mat44_t& rel_pose_ic)
    : name_(name), rate_hz_(rate_hz), rate_dt_(1.0 / rate_hz), rel_pose_ic_(rel_pose_ic){
    update_pose();
    update_covariance();
}

std::string config::get_name() const {
    return name_;
}

double config::get_rate_hz() const {
    return rate_hz_;
}

double config::get_rate_dt() const {
    return rate_dt_;
}

Mat44_t config::get_rel_pose_ic() const {
    return rel_pose_ic_;
}

Mat33_t config::get_rel_rot_ic() const {
    return rel_pose_ic_.block<3, 3>(0, 0);
}

Vec3_t config::get_rel_trans_ic() const {
    return rel_pose_ic_.block<3, 1>(0, 3);
}

Mat44_t config::get_rel_pose_ci() const {
    return rel_pose_ci_;
}

Mat33_t config::get_rel_rot_ci() const {
    return rel_pose_ci_.block<3, 3>(0, 0);
}

Vec3_t config::get_rel_trans_ci() const {
    return rel_pose_ci_.block<3, 1>(0, 3);
}

Mat33_t config::get_gps_covariance() const {
    return cov_gps_;
}
void config::update_pose() {
    const Mat33_t rel_rot_ic = rel_pose_ic_.block<3, 3>(0, 0);
    const Vec3_t rel_trans_ic = rel_pose_ic_.block<3, 1>(0, 3);
    rel_pose_ci_ = Mat44_t::Identity();
    rel_pose_ci_.block<3, 3>(0, 0) = rel_rot_ic.transpose();
    rel_pose_ci_.block<3, 1>(0, 3) = -rel_rot_ic.transpose() * rel_trans_ic;
}

void config::update_covariance() {
    //cov_gps_ = Mat33_t::Identity() * rate_hz_;
}

} // namespace gps
} // namespace openvslam
