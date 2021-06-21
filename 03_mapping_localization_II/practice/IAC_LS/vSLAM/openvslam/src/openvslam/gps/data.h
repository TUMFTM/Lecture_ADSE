#ifndef OPENVSLAM_GPS_DATA_H
#define OPENVSLAM_GPS_DATA_H

#include "openvslam/type.h"

namespace openvslam {
namespace gps {

enum gps_fix_state_t {
    NO_FIX = 0,
    FIX_2D = 2,
    FIX_3D = 3
};


class data {
public:
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    //! default constructor
    data() : fix_(gps_fix_state_t::NO_FIX) {}
//    //! Constructor for scalar inputs
//    data(const double latitude, const double longitude, const double height,
//         const double dop_precision, const gps_fix_state_t fix, const int speed_2d, const int speed_3d,
//         const double ts);
//
//    //! Constructor for vector inputs
//    data(const Vec3_t& llh, const double dop_precision, const gps_fix_state_t fix,
//         const double speed_2d, const double speed_3d, const double ts);

    //! Constructor for xyz input (IAC simulation)
    data(const double x, const double y, const double z, const double dop_precision,
                   const gps_fix_state_t fix, const int speed_2d, const int speed_3d, const double ts);

    //! Set XYZ data
    void Set_XYZ(const Vec3_t& xyz);

    //! gps measurement in latitude, longitude and height
    Vec3_t llh_;
    //! gps measurement in x y z ellipsoid coordinates
    Vec3_t xyz_;
    //! scaled gps measurement in x y z ellipsoid coordinates for better numerical stability and plotting
    Vec3_t scaled_xyz_;
    //! dilusion of precision
    double dop_precision_;
    //! 2D speed
    double speed_2d_;
    //! 3D speed
    double speed_3d_;
    //! fix -> 0: no fix, 2: 2D fix, 3: 3D fix
    gps::gps_fix_state_t fix_;
    //! timestamp [s]
    double ts_;
};

} // namespace gps
} // namespace openvslam

#endif // OPENVSLAM_GPS_DATA_H
