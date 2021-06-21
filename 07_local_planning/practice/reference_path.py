"""
Reference Path
"""
import numpy as np
from scipy.interpolate import CubicSpline


class ReferencePath:
    """Reference path class"""

    def __init__(self, xy_waypoints: np.array):
        """
        :param xy_waypoints: xy-positions of waypoints of reference path
        :type: np.array
        """

        # determine piecewise cubic spline interpolation going through waypoints
        cubic_spline = CubicSpline(x=xy_waypoints[:, 0], y=xy_waypoints[:, 1])

        # calculate s-, x-, y- coordinates of reference path
        self.__calc_sxy_rp(cubic_spline=cubic_spline)

        # calculate heading of reference path
        self.__calc_theta_rp(cubic_spline=cubic_spline)

        # calculate curvature of reference path
        self.__calc_kappa_rp(cubic_spline=cubic_spline)

        # calculate first derivative of reference path
        self.__calc_dkappa_rp(cubic_spline=cubic_spline)

    def __calc_sxy_rp(self, cubic_spline: CubicSpline):
        """Calculate arc length and xy-positions of reference path

        :param cubic_spline: cubic spline going through waypoints
        :type: CubicSpline
        """

        # sampling step size along reference path, i.e. 0.1 m between two samples along s-coordinate
        s_sampling_size = 0.1

        # define sampling size in x
        x_sampling_size = s_sampling_size / 2

        # calculate number of samples in x
        n_x = (
            np.ceil((cubic_spline.x[-1] - cubic_spline.x[0]) / x_sampling_size) + 1
        ).astype(int)

        # calculate samples along x-direction
        x = np.linspace(start=cubic_spline.x[0], stop=cubic_spline.x[-1], num=n_x)

        # initialize arc length vector
        s_x = np.zeros(shape=n_x)

        # calculate arc length using Simpson's rule
        for idx in range(n_x - 1):

            a = x[idx]
            b = x[idx + 1]
            m = (a + b) / 2

            f_a = np.sqrt(1 + cubic_spline(x=a, nu=1) ** 2)
            f_b = np.sqrt(1 + cubic_spline(x=b, nu=1) ** 2)
            f_m = np.sqrt(1 + cubic_spline(x=m, nu=1) ** 2)

            s_x[idx + 1] = s_x[idx] + (b - a) / 6 * (f_a + 4 * f_m + f_b)

        # calculate number of samples in s
        n_s = (np.ceil(s_x[-1] / s_sampling_size) + 1).astype(int)

        # calculate samples along s-direction
        self.__s_rp = np.linspace(start=0, stop=s_x[-1], num=n_s)

        # calculate x- and y-coordinates corresponding to the samples along s-direction
        self.__xy_rp = np.column_stack(
            (
                np.interp(x=self.__s_rp, xp=s_x, fp=x),
                cubic_spline(x=np.interp(x=self.__s_rp, xp=s_x, fp=x)),
            )
        )

    def __calc_theta_rp(self, cubic_spline: CubicSpline):
        """Calculate heading angle of reference path

        :param cubic_spline: cubic spline going through waypoints
        :type: CubicSpline"""

        # first derivative of y-coordinate in terms of x-coordinate
        dy_rp = cubic_spline(x=self.__xy_rp[:, 0], nu=1)

        # calculate heading
        self.__theta_rp = np.arctan(dy_rp)

    def __calc_kappa_rp(self, cubic_spline: CubicSpline):
        """Calculate curvature of reference path

        :param cubic_spline: cubic spline going through waypoints
        :type: CubicSpline"""

        # first derivative of y-coordinate in terms of x-coordinate
        dy_rp = cubic_spline(x=self.__xy_rp[:, 0], nu=1)

        # second derivative of y-coordinate in terms of x-coordinate
        ddy_rp = cubic_spline(x=self.__xy_rp[:, 0], nu=2)

        # calculate curvature
        self.__kappa_rp = ddy_rp / (1 + dy_rp ** 2) ** 1.5

    def __calc_dkappa_rp(self, cubic_spline: CubicSpline):
        """Calculate first derivative of curvature of reference path

        :param cubic_spline: cubic spline going through waypoints
        :type: CubicSpline"""

        # first derivative of y-coordinate in terms of x-coordinate
        dy_rp = cubic_spline(x=self.__xy_rp[:, 0], nu=1)

        # second derivative of y-coordinate in terms of x-coordinate
        ddy_rp = cubic_spline(x=self.__xy_rp[:, 0], nu=2)

        # third derivative of y-coordinate in terms of x-coordinate
        dddy_rp = cubic_spline(x=self.__xy_rp[:, 0], nu=3)

        # calculate first derivative of curvature
        self.__dkappa_rp = ((1 + dy_rp ** 2) * dddy_rp - 3 * dy_rp * ddy_rp ** 2) / (
            (1 + dy_rp ** 2) ** 3
        )

    @property
    def s_rp(self) -> np.array:
        """Sampled arc length of reference path

        :return: sampled arc length of reference path
        :rtype: np.array"""
        return self.__s_rp

    @property
    def xy_rp(self) -> np.array:
        """Sampled xy-position of reference path

        :return: sampled xy-position of reference path
        :rtype: np.array"""
        return self.__xy_rp

    @property
    def theta_rp(self) -> np.array:
        """Sampled heading angle of reference path

        :return: sampled heading angle of reference path
        :rtype: np.array"""
        return self.__theta_rp

    @property
    def kappa_rp(self) -> np.array:
        """Sampled curvature of reference path

        :return: sampled curvature of reference path
        :rtype: np.array"""
        return self.__kappa_rp

    @property
    def dkappa_rp(self) -> np.array:
        """Sampled first derivative of reference path

        :return: sampled first derivative of reference path
        :rtype: np.array"""
        return self.__dkappa_rp

# EOF
