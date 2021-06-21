// created by Steffen Urban April 2020, urbste@gmail.com
#include "openvslam/util/gps_converter.h"
#include "openvslam/type.h"

namespace openvslam {
namespace util {

// The variables below are constants defined to aid the conversion between ECEF
// and Geodetic coordinates.
//
// WGS-84 semi-major axis
static const double a = 6378137.0;
// WGS-84 first eccentricity squared
//static const double e2 = 6.6943799901377997e-3;
// a1 = a*e2
static const double a1 = 4.2697672707157535e+4;
// a2 = a1*a1
static const double a2 = 1.8230912546075455e+9;
// a3 = a1*e2/2
static const double a3 = 1.4291722289812413e+2;
// a4 = 2.5*a2
static const double a4 = 4.5577281365188637e+9;
// a5 = a1+a3
static const double a5 = 4.2840589930055659e+4;
// a6 = 1-e2
static const double a6 = 9.9330562000986220e-1;

static constexpr double f = 1.0/298.257223563;

static const double e = std::pow(2.0*f - f*f, 0.5);

static const double e2 = e*e;

template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}

// Converts ECEF coordinates to GPS latitude, longitude, and altitude
// Karl Olsen
void gps_converter::ECEFToLLA_new(const Vec3_t& ecef,
                                    Vec3_t& lla) {
  const double x = ecef[0];
  const double y = ecef[1];
  const double z = ecef[2];
  const double a2 = a*a;

  const double w2 = x * x + y * y;
  const double l = e2 * 0.5;
  const double l2 = l * l;
  const double m = w2 / a2;
  const double n = (z * z) * (1.0-e2)/a2;
  const double p = (m + n - 4.0*l2) / 6.0;
  const double G = m * n * l2;
  const double H = 2.0 * std::pow(p,3) + G;

  const double C = std::pow(H + G + 2.0*std::sqrt(H*G), 1.0/3.0) / std::pow(2,1.0/3.0);
  const double i = -(2*l2 + m + n) * 0.5;
  const double P = p * p;
  const double beta = i / 3.0 - C - P / C;
  const double k = l2*(l2 - m - n);
  const double mn = m - n;
  const double t = std::sqrt(std::sqrt(beta*beta - k) -
                             (beta + i)*0.5) -
                             sgn(mn) * std::sqrt(std::abs(beta-i)*0.5);

  const double F = std::pow(t,4) + 2.0*i*t*t + 2.0*l*mn*t + k;
  const double dFdt = 4.0*std::pow(t,3) + 4.0*i*t + 2.0*l*mn;

  const double deltat = -F / dFdt;
  const double u = t + deltat + l;
  const double v = t + deltat - l;

  const double w = std::sqrt(w2);
  const double deltaw = w * (1.0 - 1.0 / u);
  const double deltaz = z * (1.0 - (1.0 - e2) / v);

  lla(0) = util::RadToDeg(std::atan2(z*u, w*v));
  lla(1) = util::RadToDeg(atan2(y, x));
  lla(2) = sgn(u - 1.0) * std::sqrt(deltaw*deltaw + deltaz*deltaz);
}

// Converts ECEF coordinates to GPS latitude, longitude, and altitude.
Vec3_t gps_converter::ECEFToLLA(const Vec3_t& ecef) {
  double lat, lon, alt;
  const double x = ecef[0];
  const double y = ecef[1];
  const double z = ecef[2];

  const double zp = std::abs(z);
  const double w2 = x * x + y * y;
  const double w = std::sqrt(w2);
  const double r2 = w2 + z * z;
  const double r = std::sqrt(r2);
  lon = std::atan2(y, x);

  const double s2 = z * z / r2;
  const double c2 = w2 / r2;
  double u = a2 / r;
  double v = a3 - a4 / r;
  double s, c, ss;
  if (c2 > 0.3) {
    s = (zp / r) * (1.0 + c2 * (a1 + u + s2 * v) / r);
    lat = std::asin(s);
    ss = s * s;
    c = std::sqrt(1.0 - ss);
  } else {
    c = (w / r) * (1.0 - s2 * (a5 - u - c2 * v) / r);
    lat = std::acos(c);
    ss = 1.0 - c * c;
    s = std::sqrt(ss);
  }

  const double g = 1.0 - e2 * ss;
  const double rg = a / std::sqrt(g);
  const double rf = a6 * rg;
  u = w - rg * c;
  v = zp - rf * s;
  const double f = c * u + s * v;
  const double m = c * v - s * u;
  const double p = m / (rf / g + f);
  lat = lat + p;
  alt = f + m * p / 2.0;
  if (z < 0.0) {
    lat *= -1.0;
  }

  return Vec3_t(util::RadToDeg(lat), util::RadToDeg(lon), alt);
}

// Converts GPS latitude, longitude, and altitude to ECEF coordinates.
Vec3_t gps_converter::LLAToECEF(const Vec3_t& lla) {
  Vec3_t ecef;
  const double lat = util::DegToRad(lla[0]);
  const double lon = util::DegToRad(lla[1]);
  const double alt = lla[2];
  const double n = a / std::sqrt(1.0 - e2 * std::sin(lat) * std::sin(lat));
  // ECEF x
  ecef[0] = (n + alt) * std::cos(lat) * std::cos(lon);
  // ECEF y
  ecef[1] = (n + alt) * std::cos(lat) * std::sin(lon);
  // ECEF z
  ecef[2] = (n * (1.0 - e2) + alt) * std::sin(lat);
  return ecef;
}


} // namespace gps_converter
} // namespace openvslam
