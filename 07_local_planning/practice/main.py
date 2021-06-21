import numpy as np
from global_settings import get_params
from util import (
    transform_state_cartesian_to_frenet,
    transform_obstacles_frenet_to_cartesian,
    check_trajectories,
    ideal_tracking,
)
from frenet_vizualization import visualize
from trajectory import Trajectory, LateralCurve, LongitudinalCurve
from reference_path import ReferencePath
import operator


def step(state: dict, reference_path: ReferencePath, params: dict) -> tuple:
    """Generation of a trajectory

    :param state: current state of vehicle in frénet coordinates
    :type: dict
    :param reference_path: reference path
    :type: ReferencePath
    :param params: dictionary containing all parameters
    :type: dict
    :return: optimal trajectory, i.e. trajectory with lowest cost
    :rtype: Trajectory
    :return: dictionary containing all generated trajectories of this time step
    :rtype: dict"""

    # lists of curves and trajectories
    longitudinal_curves = []
    lateral_curves = []
    trajectories = []

    # loop over several end times
    for t_end in np.linspace(
        start=params["discretization"]["t_min"],
        stop=params["discretization"]["t_max"],
        num=params["discretization"]["num_t"],
    ):

        # sample time
        t_array = np.linspace(
            start=0, stop=t_end, num=params["discretization"]["sampling_points"]
        )

        # loop over several longitudinal end velocities
        for s_dot_end in np.linspace(
            start=params["discretization"]["s_dot_min"],
            stop=params["discretization"]["s_dot_max"],
            num=params["discretization"]["num_s_dot"],
        ):

            # calculate longitudinal curve
            longitudinal_curve = LongitudinalCurve(
                s_start=state["s"],
                s_dot_start=state["s_dot"],
                s_ddot_start=state["s_ddot"],
                s_dot_end=s_dot_end,
                s_ddot_end=0,
                t_array=t_array,
            )

            # add longitudinal curve to longitudinal curves list
            longitudinal_curves.append(longitudinal_curve)

        # loop over several lateral end positions
        for d_end in np.linspace(
            start=params["discretization"]["d_min"],
            stop=params["discretization"]["d_max"],
            num=params["discretization"]["num_d"],
        ):

            # calculate lateral curve
            lateral_curve = LateralCurve(
                d_start=state["d"],
                d_dot_start=state["d_dot"],
                d_ddot_start=state["d_ddot"],
                d_end=d_end,
                d_dot_end=0,
                d_ddot_end=0,
                t_array=t_array,
            )

            # add lateral curve to lateral curves list
            lateral_curves.append(lateral_curve)

        # combine set of longitudinal and lateral curves
        for longitudinal_curve in longitudinal_curves:
            for lateral_curve in lateral_curves:

                # calculate trajectory
                trajectory = Trajectory(
                    longitudinal_curve=longitudinal_curve,
                    lateral_curve=lateral_curve,
                    t_array=t_array,
                    cost_coefficients=params["cost_coefficients"],
                    s_dot_desired=params["discretization"]["s_dot_desired"],
                )

                # transform trajectory from frenét to cartesian coordinate system
                trajectory.transform_frenet_to_cartesian(reference_path=reference_path)

                # add trajectory to trajectories list
                trajectories.append(trajectory)

    # sort trajectories according to the cost associated with each trajectory
    trajectories = sorted(trajectories, key=operator.attrgetter("cost"))

    # check trajectories for validity and sort into valid and invalid
    trajectories = check_trajectories(trajectories=trajectories, parameters=params)

    # extract best trajectory (valid trajectory with lowest cost)
    optimal_trajectory = trajectories["valid"][0]

    return optimal_trajectory, trajectories


if __name__ == "__main__":

    # get parameters from params.ini as dictionary
    params = get_params()

    # generate reference path
    reference_path = ReferencePath(xy_waypoints=params["xy_waypoints"])

    # calculate cartesian coordinates of obstacles and add to parameter dictionary
    xy_obstacles = transform_obstacles_frenet_to_cartesian(
        reference_path=reference_path, sd_obstacles=params["sd_obstacles"]
    )
    params["xy_obstacles"] = xy_obstacles

    # get initial cartesian state from parameter file
    initial_cartesian_state = params["initial_state"]

    # transform initial state from cartesian to frenét coordinate system
    frenet_state = transform_state_cartesian_to_frenet(
        cartesian_state=initial_cartesian_state, reference_path=reference_path
    )

    # number of steps
    step_counter = 0

    # dictionary to store all trajectories of every time step for the visualization
    trajectories_over_time = dict()

    # maximum progress s per step
    max_s_progress_per_step = (
        params["discretization"]["t_max"] * params["limits"]["v_max"]
    )

    # main loop
    while frenet_state["s"] < reference_path.s_rp[-1] - max_s_progress_per_step:

        # do one planning step
        optimal_trajectory, trajectories = step(
            state=frenet_state, reference_path=reference_path, params=params
        )

        # project along optimal trajectory according to calculation time (ideal tracking)
        frenet_state = ideal_tracking(
            trajectory=optimal_trajectory,
            time=params["discretization"]["fixed_calc_time"],
        )

        # store trajectories of this time step in dictionary containing trajectories of all time steps for visualization
        trajectories_over_time[step_counter] = trajectories

        # print current progress every 20 steps
        if not step_counter % 20:
            progress = min(
                100
                * frenet_state["s"]
                / (reference_path.s_rp[-1] - max_s_progress_per_step),
                100,
            )
            print(f"Current progress {int(progress)} %")

        step_counter += 1

    # visualize trajectories of all steps
    visualize(
        trajectories_over_time=trajectories_over_time,
        reference_path=reference_path,
        params=params,
    )

# EOF
