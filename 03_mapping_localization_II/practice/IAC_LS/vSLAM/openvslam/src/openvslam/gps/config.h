#ifndef OPENVSLAM_GPS_CONFIG_H
#define OPENVSLAM_GPS_CONFIG_H

#include "openvslam/type.h"

namespace openvslam {
namespace gps {

class config {
public:
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    config() {}
    //! Constructor
    config(const std::string& name, const double rate_hz, const Mat44_t& rel_pose_ic);

    //---------------------------
    // Setters and Getters

    //! Get GPS model name
    std::string get_name() const;
    //! Get GPS rate [Hz]
    double get_rate_hz() const;
    //! Get GPS rate [s]
    double get_rate_dt() const;

    //! Get GPS's relative pose w.r.t. the camera
    Mat44_t get_rel_pose_ic() const;
    //! Get GPS's relative rotation w.r.t. the camera
    Mat33_t get_rel_rot_ic() const;
    //! Get GPS's relative translation w.r.t. the camera
    Vec3_t get_rel_trans_ic() const;
    //! Get camera's relative pose w.r.t. the GPS
    Mat44_t get_rel_pose_ci() const;
    //! Get camera's relative rotation w.r.t. the GPS
    Mat33_t get_rel_rot_ci() const;
    //! Get camera's relative translation w.r.t. the GPS
    Vec3_t get_rel_trans_ci() const;

    //! Get acceleration covariance [(m/s^2)^2]
    Mat33_t get_gps_covariance() const;
private:
    //! Update rel_pose_ci_ using rel_pose_ic_
    void update_pose();
    //! Update covariances using the currently assigned variables
    void update_covariance();

    //! GPS model name
    std::string name_;
    //! GPS rate [Hz]
    double rate_hz_;
    //! GPS rate [s]
    double rate_dt_;

    //! GPS's relative pose w.r.t the camera
    Mat44_t rel_pose_ic_;
    //! camera's relative pose w.r.t the GPS
    Mat44_t rel_pose_ci_;

    //! covariance
    Mat33_t cov_gps_ = Mat33_t::Identity();
};

} // namespace gps
} // namespace openvslam

#endif // OPENVSLAM_GPS_CONFIG_H
