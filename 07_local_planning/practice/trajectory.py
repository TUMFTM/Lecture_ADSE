"""
Trajectory
"""
import numpy as np
import scipy.integrate as integrate
from reference_path import ReferencePath


class LongitudinalCurve:
    """Longitudinal curve class (Quartic polynomial)"""

    def __init__(
        self,
        s_start: float,
        s_dot_start: float,
        s_ddot_start: float,
        s_dot_end: float,
        s_ddot_end: float,
        t_array: np.array,
    ):
        """
        :param s_start: start position of longitudinal curve at t=0
        :type s_start: float
        :param s_dot_start: start velocity of longitudinal curve at t=0
        :type s_dot_start: float
        :param s_ddot_start: start acceleration of longitudinal curve at t=0
        :type s_ddot_start: float
        :param s_dot_end: end velocity of longitudinal curve at t_end
        :type s_dot_end: float
        :param s_ddot_end: end acceleration of longitudinal curve at t_end
        :type s_ddot_end: float
        :param t_array: time array of longitudinal curve
        :type t_array: np.array"""

        t_end = t_array[-1]

        a = np.array(
            [
                [1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 2, 0, 0],
                [0, 1, 2 * t_end, 3 * t_end ** 2, 4 * t_end ** 3],
                [0, 0, 2, 6 * t_end, 12 * t_end ** 2],
            ]
        )
        b = np.array([s_start, s_dot_start, s_ddot_start, s_dot_end, s_ddot_end])

        # calculate coefficients of quartic polynomial
        c = np.linalg.solve(a=a, b=b)

        # s and temporal derivatives
        self.__s = (
            c[0]
            + c[1] * t_array
            + c[2] * t_array ** 2
            + c[3] * t_array ** 3
            + c[4] * t_array ** 4
        )
        self.__s_dot = (
            c[1]
            + 2 * c[2] * t_array
            + 3 * c[3] * t_array ** 2
            + 4 * c[4] * t_array ** 3
        )
        self.__s_ddot = 2 * c[2] + 6 * c[3] * t_array + 12 * c[4] * t_array ** 2
        self.__s_dddot = 6 * c[3] + 24 * c[4] * t_array

    @property
    def s(self):
        return self.__s

    @property
    def s_dot(self):
        return self.__s_dot

    @property
    def s_ddot(self):
        return self.__s_ddot

    @property
    def s_dddot(self):
        return self.__s_dddot


class LateralCurve:
    """Lateral curve class (Quintic polynomial)"""

    def __init__(
        self,
        d_start: float,
        d_dot_start: float,
        d_ddot_start: float,
        d_end: float,
        d_dot_end: float,
        d_ddot_end: float,
        t_array: np.array,
    ):
        """
        :param d_start: start position of lateral curve at t=0
        :type d_start: float
        :param d_dot_start: start velocity of lateral curve at t=0
        :type d_dot_start: float
        :param d_ddot_start: start acceleration of lateral curve at t=0
        :type d_ddot_start: float
        :param d_end: end position of lateral curve at t_end
        :type d_end: float
        :param d_dot_end: end velocity of lateral curve at t_end
        :type d_dot_end: float
        :param d_ddot_end: end acceleration of lateral curve at t_end
        :type d_ddot_end: float
        :param t_array: time array of lateral curve
        :type t_array: np.array"""

        t_end = t_array[-1]

        a = np.array(
            [
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 2, 0, 0, 0],
                [1, t_end, t_end ** 2, t_end ** 3, t_end ** 4, t_end ** 5],
                [0, 1, 2 * t_end, 3 * t_end ** 2, 4 * t_end ** 3, 5 * t_end ** 4],
                [0, 0, 2, 6 * t_end, 12 * t_end ** 2, 20 * t_end ** 3],
            ]
        )
        b = np.array([d_start, d_dot_start, d_ddot_start, d_end, d_dot_end, d_ddot_end])

        # calculate coefficients of quintic polynomial
        c = np.linalg.solve(a=a, b=b)

        # d and temporal derivatives
        self.__d = (
            c[0]
            + c[1] * t_array
            + c[2] * t_array ** 2
            + c[3] * t_array ** 3
            + c[4] * t_array ** 4
            + c[5] * t_array ** 5
        )
        self.__d_dot = (
            c[1]
            + 2 * c[2] * t_array
            + 3 * c[3] * t_array ** 2
            + 4 * c[4] * t_array ** 3
            + 5 * c[5] * t_array ** 4
        )
        self.__d_ddot = (
            2 * c[2]
            + 6 * c[3] * t_array
            + 12 * c[4] * t_array ** 2
            + 20 * c[5] * t_array ** 3
        )
        self.__d_dddot = 6 * c[3] + 24 * c[4] * t_array + 60 * c[5] * t_array ** 2

    @property
    def d(self):
        return self.__d

    @property
    def d_dot(self):
        return self.__d_dot

    @property
    def d_ddot(self):
        return self.__d_ddot

    @property
    def d_dddot(self):
        return self.__d_dddot


class Trajectory:
    """Trajectory class"""

    def __init__(
        self,
        longitudinal_curve: LongitudinalCurve,
        lateral_curve: LateralCurve,
        t_array: np.array,
        cost_coefficients: dict,
        s_dot_desired: float,
    ):
        """
        :param longitudinal_curve: longitudinal curve of trajectory
        :type longitudinal_curve: LongitudinalCurve
        :param lateral_curve: lateral curve of trajectory
        :type lateral_curve: LateralCurve
        :param t_array: time array of trajectory
        :type t_array: np.array
        :param cost_coefficients: cost coefficients to calculate total cost of trajectory
        :type cost_coefficients: dict
        :param s_dot_desired: desired longitudinal end velocity
        :type s_dot_desired: dict"""

        self.__t = t_array

        self.__s = longitudinal_curve.s
        self.__s_dot = longitudinal_curve.s_dot
        self.__s_ddot = longitudinal_curve.s_ddot
        self.__s_dddot = longitudinal_curve.s_dddot

        self.__d = lateral_curve.d
        self.__d_dot = lateral_curve.d_dot
        self.__d_ddot = lateral_curve.d_ddot
        self.__d_dddot = lateral_curve.d_dddot

        t_end = self.__t[-1]
        s_dot_end = self.__s_dot[-1]
        d_end = self.__d[-1]

        # calculate integral of jerk using trapezoidal rule
        jerk_integral_lateral_trajectory = integrate.trapezoid(
            y=self.__d_dddot ** 2, x=self.__t
        )
        jerk_integral_longitudinal_trajectory = integrate.trapezoid(
            y=self.__s_dddot ** 2, x=self.__t
        )

        # calculate lateral cost
        lateral_cost = (
            cost_coefficients["k_jerk"] * jerk_integral_lateral_trajectory
            + cost_coefficients["k_time"] * t_end
            + cost_coefficients["k_d"] * d_end ** 2
        )

        # calculate longitudinal cost
        longitudinal_cost = (
            cost_coefficients["k_jerk"] * jerk_integral_longitudinal_trajectory
            + cost_coefficients["k_time"] * t_end
            + cost_coefficients["k_s_dot"] * (s_dot_end - s_dot_desired) ** 2
        )

        # calculate total cost
        self.__cost = (
            cost_coefficients["k_lateral"] * lateral_cost
            + cost_coefficients["k_longitudinal"] * longitudinal_cost
        )

    def transform_frenet_to_cartesian(self, reference_path: ReferencePath):
        """Transform trajectory from frenét to cartesian coordinate system

        :param reference_path: reference path
        :type reference_path: ReferencePath"""

        # get position along reference path corresponding to s-values
        xy_rp = np.column_stack(
            (
                np.interp(
                    x=self.__s, xp=reference_path.s_rp, fp=reference_path.xy_rp[:, 0]
                ),
                np.interp(
                    x=self.__s, xp=reference_path.s_rp, fp=reference_path.xy_rp[:, 1]
                ),
            )
        )

        # get heading along reference path corresponding to s-values
        theta_rp = np.interp(
            x=self.__s, xp=reference_path.s_rp, fp=reference_path.theta_rp
        )

        # get curvature along reference path corresponding to s-values
        kappa_rp = np.interp(
            x=self.__s, xp=reference_path.s_rp, fp=reference_path.kappa_rp
        )

        # get first derivative of curvature along reference path corresponding to s-values
        dkappa_rp = np.interp(
            x=self.__s, xp=reference_path.s_rp, fp=reference_path.dkappa_rp
        )

        # calculate first derivative of d(s)
        d_prime = self.__d_dot / self.__s_dot

        # calculate second derivative of d(s)
        d_pprime = (self.__d_ddot - d_prime * self.__s_ddot) / (self.__s_dot ** 2)

        # calculate global position
        self.__xy = np.column_stack(
            (
                xy_rp[:, 0] - self.__d * np.sin(theta_rp),
                xy_rp[:, 1] + self.__d * np.cos(theta_rp),
            )
        )

        # calculate difference in heading between trajectory and reference path
        delta_theta = np.arctan(d_prime / (1 - kappa_rp * self.__d))

        # calculate global heading
        self.__theta = delta_theta + theta_rp

        # calculate global longitudinal velocity
        self.__v = self.__s_dot * (1 - kappa_rp * self.__d) / np.cos(delta_theta)

        # calculate global curvature
        self.__kappa = (
            (
                (
                    d_pprime
                    + (dkappa_rp * self.__d + kappa_rp * d_prime) * np.tan(delta_theta)
                )
                * (np.cos(delta_theta) ** 2)
                / (1 - kappa_rp * self.__d)
                + kappa_rp
            )
            * np.cos(delta_theta)
            / (1 - kappa_rp * self.__d)
        )

        # calculate global longitudinal acceleration
        self.__a = self.__s_ddot * (1 - kappa_rp * self.__d) / np.cos(delta_theta) + (
            self.__s_dot ** 2
        ) / np.cos(delta_theta) * (
            (1 - kappa_rp * self.__d)
            * np.tan(delta_theta)
            * (
                self.__kappa * (1 - kappa_rp * self.__d) / np.cos(delta_theta)
                - kappa_rp
            )
            - (dkappa_rp * self.__d + kappa_rp * d_prime)
        )

    @property
    def t(self) -> np.array:
        """Sampled times of trajectory

        :return: sampled times of trajectory
        :rtype: np.array"""
        return self.__t

    @property
    def s(self) -> np.array:
        """Sampled longitudinal positions of trajectory

        :return: sampled longitudinal positions of trajectory
        :rtype: np.array"""
        return self.__s

    @property
    def s_dot(self) -> np.array:
        """Sampled longitudinal velocities of trajectory

        :return: sampled longitudinal velocities of trajectory
        :rtype: np.array"""
        return self.__s_dot

    @property
    def s_ddot(self) -> np.array:
        """Sampled longitudinal accelerations of trajectory

        :return: sampled longitudinal accelerations of trajectory
        :rtype: np.array"""
        return self.__s_ddot

    @property
    def d(self) -> np.array:
        """Sampled lateral positions of trajectory

        :return: sampled lateral positions of trajectory
        :rtype: np.array"""
        return self.__d

    @property
    def d_dot(self) -> np.array:
        """Sampled lateral velocities of trajectory

        :return: sampled lateral velocities of trajectory
        :rtype: np.array"""
        return self.__d_dot

    @property
    def d_ddot(self) -> np.array:
        """Sampled lateral accelerations of trajectory

        :return: sampled lateral velocities of trajectory
        :rtype: np.array"""
        return self.__d_ddot

    @property
    def xy(self) -> np.array:
        """Sampled cartesian positions of trajectory

        :return: sampled cartesian positions of trajectory
        :rtype: np.array"""
        return self.__xy

    @property
    def v(self) -> np.array:
        """Sampled cartesian velocity of trajectory

        :return: sampled cartesian velocity of trajectory
        :rtype: np.array"""
        return self.__v

    @property
    def theta(self) -> np.array:
        """Sampled heading angle of trajectory

        :return: sampled heading angle of trajectory
        :rtype: np.array"""
        return self.__theta

    @property
    def a(self) -> np.array:
        """Sampled longitudinal, cartesian acceleration of trajectory

        :return: sampled longitudinal, cartesian acceleration of trajectory
        :rtype: np.array"""
        return self.__a

    @property
    def kappa(self) -> np.array:
        """Sampled curvature of trajectory

        :return: sampled curvature of trajectory
        :rtype: np.array"""
        return self.__kappa

    @property
    def cost(self) -> float:
        """Cost of trajectory

        :return: sampled curvature of trajectory
        :rtype: np.array"""
        return self.__cost


# EOF
