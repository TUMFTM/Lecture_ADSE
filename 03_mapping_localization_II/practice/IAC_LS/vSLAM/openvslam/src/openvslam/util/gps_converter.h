// created by Steffen Urban April 2020, urbste@gmail.com
// taken from TheiaSfM
#ifndef OPENVSLAM_UTIL_GPS_CONVERTER_H
#define OPENVSLAM_UTIL_GPS_CONVERTER_H

#include "openvslam/type.h"
#include "openvslam/gps/data.h"

namespace openvslam {
namespace util {

static const double kRadToDeg = 180.0 / M_PI;
static const double kDegToRad = M_PI / 180.0;

inline double RadToDeg(double angle_radians) {
  return angle_radians * kRadToDeg;
}

inline double DegToRad(double angle_degrees) {
  return angle_degrees * kDegToRad;
}

// This helper class contains static methods to convert between Geodetic
// coordinates (latitude, longitude, and altitude) and Earth-Center-Earth-Fixed
// (ECEF) coordinates. The method used is very fast, does not require special
// treatment at the poles or equator, and is extremely accurate. In tests by
// csweeney with randomly generated points, the maximum error of lat/lon is
// roughly 4e-16 and the maximum altitude error is roughly 3e-9 meters. These
// errors are smaller than the wavelength of visible light!!
//
// The original method was presenting in this paper:
// Olson, D.K. "Converting earth-Centered, Earth-Fixed Coordinates to Geodetic
// Coordinates," IEEE Transactions on Aerospace and Electronic Systems, Vol. 32,
// No. 1, January 1996, pp. 473-476.
class gps_converter {
public:
    // Converts ECEF coordinates to GPS latitude, longitude, and altitude. ECEF
    // coordinates should be in meters. The returned latitude and longitude are in
    // degrees, and the altitude will be in meters.
    static Vec3_t ECEFToLLA(const Vec3_t& ecef);

    // Converts ECEF coordinates to GPS latitude, longitude, and altitude. ECEF
    // coordinates should be in meters. The returned latitude and longitude are in
    // degrees, and the altitude will be in meters.
    // Karl Osen (2019): Accurate Conversion of Earth-Fixed Earth-Centered
    // Coordinates to Geodetic Coordinates
    static void ECEFToLLA_new(const Vec3_t& ecef, Vec3_t& lla);

    // Converts GPS latitude, longitude, and altitude to ECEF coordinates. The
    // latitude and longitude should be in degrees and the altitude in meters. The
    // returned ECEF coordinates will be in meters.
    static Vec3_t LLAToECEF(const Vec3_t& lla);
};

} // namespace util
} // namespace openvslam
#endif
