"""
Util
"""
import numpy as np
from trajectory import Trajectory
from reference_path import ReferencePath


def ideal_tracking(trajectory: Trajectory, time: float) -> dict:
    """Project along trajectory according to desired time (ideal tracking).

    :param trajectory: trajectory object to project along
    :type: Trajectory
    :param time: desired time
    :type: float
    :return: dictionary of new state in frenét coordinates
    :rtype: dict"""

    # initialize dictionary for state in frenét coordinates
    frenet_state = {}

    # project along trajectory
    frenet_state["s"] = np.interp(x=time, xp=trajectory.t, fp=trajectory.s)
    frenet_state["d"] = np.interp(x=time, xp=trajectory.t, fp=trajectory.d)
    frenet_state["s_dot"] = np.interp(x=time, xp=trajectory.t, fp=trajectory.s_dot)
    frenet_state["d_dot"] = np.interp(x=time, xp=trajectory.t, fp=trajectory.d_dot)
    frenet_state["s_ddot"] = np.interp(x=time, xp=trajectory.t, fp=trajectory.s_ddot)
    frenet_state["d_ddot"] = np.interp(x=time, xp=trajectory.t, fp=trajectory.d_ddot)

    return frenet_state


def check_trajectories(trajectories: list, parameters: dict) -> dict:
    """Check trajectories for validity and sort into valid and invalid

    :param trajectories: list of all generated trajectories at this time step
    :type: list
    :param parameters: dictionary containing all parameters
    :type: dict
    :return: dictionary containing all generated trajectories of this time step sorted into valid and invalid
    :rtype: dict"""

    # lists for valid and invalid trajectories
    valid_trajectories = []
    invalid_trajectories = []

    # iterate through trajectories and add to invalid trajectories if not valid
    for trajectory in trajectories:

        # check maximum velocity
        if np.amax(a=trajectory.v) > parameters["limits"]["v_max"]:
            invalid_trajectories.append(trajectory)

        # check longitudinal acceleration
        elif np.amax(a=trajectory.a) > parameters["limits"]["a_max"]:
            invalid_trajectories.append(trajectory)

        # check curvature
        elif np.amax(a=np.abs(trajectory.kappa)) > parameters["limits"]["kappa_max"]:
            invalid_trajectories.append(trajectory)

        # check collisions
        elif check_collision(trajectory=trajectory, parameters=parameters):
            invalid_trajectories.append(trajectory)

        # add to valid trajectories
        else:
            valid_trajectories.append(trajectory)

    # store valid and invalid trajectories in dictionary
    trajectories = {"valid": valid_trajectories, "invalid": invalid_trajectories}

    return trajectories


def check_collision(trajectory: Trajectory, parameters: dict) -> bool:
    """Check trajectory for collision with obstacles

    :param trajectory: a trajectory object
    :type: Trajectory
    :param parameters: dictionary containing all parameters
    :type: dict
    :return: determination whether trajectory collides with any obstacle
    :rtype: bool"""

    # iterate through obstacles
    for xy_obstacle in parameters["xy_obstacles"]:

        # calculate the distance for each trajectory point to the current object
        d = np.sqrt(
            (trajectory.xy[:, 0] - xy_obstacle[0]) ** 2
            + (trajectory.xy[:, 1] - xy_obstacle[1]) ** 2
        )

        # calculate safety factor
        safety_factor = parameters["discretization"]["max_safety_factor"] * np.ones(
            shape=np.size(d)
        )

        # increase safety factor linearly by time
        slope = (
            parameters["discretization"]["max_safety_factor"]
            - parameters["discretization"]["min_safety_factor"]
        ) / parameters["discretization"]["safety_factor_time"]

        safety_factor[
            trajectory.t <= parameters["discretization"]["safety_factor_time"]
        ] = (
            slope
            * trajectory.t[
                trajectory.t <= parameters["discretization"]["safety_factor_time"]
            ]
            + parameters["discretization"]["min_safety_factor"]
        )

        # check if any trajectory point is too close to the object using the car's MBC radius
        collision = np.any(
            a=d
            <= safety_factor
            * np.sqrt(
                (parameters["discretization"]["car_length"] / 2) ** 2
                + (parameters["discretization"]["car_width"] / 2) ** 2
            )
        )

        if collision:
            return True

    return False


def transform_obstacles_frenet_to_cartesian(
    reference_path: ReferencePath, sd_obstacles: np.array
) -> np.array:
    """Transform obstacles from frenét to cartesian coordinate system

    :param reference_path: reference path
    :type: ReferencePath
    :param sd_obstacles: array containing obstacles in frenét coordinates
    :type: np.array
    :return: cartesian xy-coordinates of obstacles
    :rtype: np.array"""

    # get position along reference path corresponding to s-values
    xy_rp = np.column_stack(
        (
            np.interp(
                x=sd_obstacles[:, 0],
                xp=reference_path.s_rp,
                fp=reference_path.xy_rp[:, 0],
            ),
            np.interp(
                x=sd_obstacles[:, 0],
                xp=reference_path.s_rp,
                fp=reference_path.xy_rp[:, 1],
            ),
        )
    )

    # get heading along reference path corresponding to s-values
    theta_rp = np.interp(
        x=sd_obstacles[:, 0], xp=reference_path.s_rp, fp=reference_path.theta_rp
    )

    # transform position of obstacles into cartesian coordinate system
    xy_obstacles = np.column_stack(
        (
            xy_rp[:, 0] - sd_obstacles[:, 1] * np.sin(theta_rp),
            xy_rp[:, 1] + sd_obstacles[:, 1] * np.cos(theta_rp),
        )
    )

    return xy_obstacles


def transform_state_cartesian_to_frenet(
    cartesian_state: dict, reference_path: ReferencePath
) -> dict:
    """Transform state from cartesian to frenét coordinate system

    :param cartesian_state: dictionary of state in cartesian coordinates
    :type: dict
    :param reference_path: reference path
    :type: ReferencePath
    :return: dictionary of state in frenét coordinates
    :rtype: dict"""

    # initialize dictionary for state in frenét coordinates
    frenet_state = {}

    # calculate distance between current state and reference path
    dist = np.sqrt(
        (cartesian_state["x"] - reference_path.xy_rp[:, 0]) ** 2
        + (cartesian_state["y"] - reference_path.xy_rp[:, 1]) ** 2
    )

    # get index
    idx = np.argmin(a=dist)

    # get x- and y-position along reference path
    xy_rp = reference_path.xy_rp[idx, :]

    # get s-coordinate along reference path
    s_rp = reference_path.s_rp[idx]

    # get heading along reference path
    theta_rp = reference_path.theta_rp[idx]

    # get curvature along reference path
    kappa_rp = reference_path.kappa_rp[idx]

    # get first derivative of curvature along reference path
    dkappa_rp = reference_path.dkappa_rp[idx]

    # calculate difference in heading between trajectory and reference path
    delta_theta = cartesian_state["theta"] - theta_rp

    # current position of the car
    xy_state = np.array([cartesian_state["x"], cartesian_state["y"]])

    # calculate distance vector
    d_vector = xy_state - xy_rp

    # calculate tangential vector
    tangential_vector = np.array([np.cos(theta_rp), np.sin(theta_rp)])

    # calculate sign of lateral position
    d_sign = np.sign(np.cross(a=tangential_vector, b=d_vector))

    # calculate quantities in frenèt coordinate system
    frenet_state["s"] = s_rp

    frenet_state["d"] = d_sign * dist[idx]

    frenet_state["s_dot"] = (cartesian_state["v"] * np.cos(delta_theta)) / (
        1 - kappa_rp * frenet_state["d"]
    )

    d_prime = (1 - kappa_rp * frenet_state["d"]) * np.tan(delta_theta)
    frenet_state["d_dot"] = frenet_state["s_dot"] * d_prime

    frenet_state["s_ddot"] = (
        np.cos(delta_theta)
        / (1 - kappa_rp * frenet_state["d"])
        * (
            cartesian_state["a"]
            - (frenet_state["s_dot"] ** 2)
            / np.cos(delta_theta)
            * (
                (1 - kappa_rp * frenet_state["d"])
                * np.tan(delta_theta)
                * (
                    cartesian_state["kappa"]
                    * (1 - kappa_rp * frenet_state["d"])
                    / np.cos(delta_theta)
                    - kappa_rp
                )
                - (dkappa_rp * frenet_state["d"] + kappa_rp * d_prime)
            )
        )
    )

    d_pprime = -(dkappa_rp * frenet_state["d"] + kappa_rp * d_prime) * np.tan(
        delta_theta
    ) + (1 - kappa_rp * frenet_state["d"]) / (np.cos(delta_theta) ** 2) * (
        cartesian_state["kappa"]
        * (1 - kappa_rp * frenet_state["d"])
        / np.cos(delta_theta)
        - kappa_rp
    )
    frenet_state["d_ddot"] = (
        d_pprime * frenet_state["s_dot"] ** 2 + d_prime * frenet_state["s_ddot"]
    )

    return frenet_state


# EOF
