import os
import numpy as np


def settings(file_paths, opt_type):
    # set import options ---------------------------------------------------------------------------------------------------
    imp_opts = {
        "flip_imp_track": False,  # flip imported track to reverse direction
        "set_new_start": False,  # set new starting point (changes order, not coordinates)
        "new_start": np.array([0.0, -47.0]),  # [x_m, y_m]
        "min_track_width": None,  # [m] minimum enforced track width (set None to deactivate)
        "num_laps": 1,
    }  # number of laps to be driven (significant with powertrain-option),
    # only relevant in mintime-optimization
    mintime_opts = {
        "tpadata": None,
        "warm_start": False,
        "var_friction": None,
        "reopt_mintime_solution": False,
        "recalc_vel_profile_by_tph": False,
    }
    # lap time calculation table -------------------------------------------------------------------------------------------
    lap_time_mat_opts = {
        "use_lap_time_mat": False,  # calculate a lap time matrix (diff. top speeds and scales)
        "gg_scale_range": [0.3, 1.0],  # range of gg scales to be covered
        "gg_scale_stepsize": 0.05,  # step size to be applied
        "top_speed_range": [
            100.0,
            150.0,
        ],  # range of top speeds to be simulated [in km/h]
        "top_speed_stepsize": 5.0,  # step size to be applied
        "file": "lap_time_matrix.csv",
    }  # file name of the lap time matrix (stored in "outputs")
    # ----------------------------------------------------------------------------------------------------------------------
    # INITIALIZATION OF PATHS ----------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # get current path
    file_paths["module"] = os.path.abspath("")
    # assemble track import path
    file_paths["track_file"] = os.path.join(
        file_paths["module"], "inputs", "tracks", file_paths["track_name"] + ".csv"
    )

    # assemble friction map import paths
    file_paths["tpamap"] = os.path.join(
        file_paths["module"],
        "inputs",
        "frictionmaps",
        file_paths["track_name"] + "_tpamap.csv",
    )
    file_paths["tpadata"] = os.path.join(
        file_paths["module"],
        "inputs",
        "frictionmaps",
        file_paths["track_name"] + "_tpadata.json",
    )

    # create outputs folder(s)
    os.makedirs(file_paths["module"] + "/outputs", exist_ok=True)

    if opt_type == "mintime":
        os.makedirs(file_paths["module"] + "/outputs/mintime", exist_ok=True)

    # assemble export paths
    file_paths["mintime_export"] = os.path.join(
        file_paths["module"], "outputs", "mintime"
    )
    file_paths["traj_race_export"] = os.path.join(
        file_paths["module"], "outputs", "traj_race_cl.csv"
    )
    file_paths["lap_time_mat_export"] = os.path.join(
        file_paths["module"], "outputs", lap_time_mat_opts["file"]
    )

    return imp_opts, mintime_opts, lap_time_mat_opts, file_paths


if __name__ == "__main__":
    pass
