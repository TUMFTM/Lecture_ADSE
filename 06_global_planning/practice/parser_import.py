import configparser
import os
import json


def parser_import(file_paths, opt_type, mintime_opts):
    # load vehicle parameter file into a "pars" dict
    parser = configparser.ConfigParser()
    pars = {}

    if not parser.read(
        os.path.join(file_paths["module"], "params", file_paths["veh_params_file"])
    ):
        raise ValueError("Specified config file does not exist or is empty!")

    pars["ggv_file"] = json.loads(parser.get("GENERAL_OPTIONS", "ggv_file"))
    pars["ax_max_machines_file"] = json.loads(
        parser.get("GENERAL_OPTIONS", "ax_max_machines_file")
    )
    pars["stepsize_opts"] = json.loads(parser.get("GENERAL_OPTIONS", "stepsize_opts"))
    pars["reg_smooth_opts"] = json.loads(
        parser.get("GENERAL_OPTIONS", "reg_smooth_opts")
    )
    pars["veh_params"] = json.loads(parser.get("GENERAL_OPTIONS", "veh_params"))
    pars["vel_calc_opts"] = json.loads(parser.get("GENERAL_OPTIONS", "vel_calc_opts"))

    if opt_type == "shortest_path":
        pars["optim_opts"] = json.loads(
            parser.get("OPTIMIZATION_OPTIONS", "optim_opts_shortest_path")
        )

    elif opt_type in ["mincurv", "mincurv_iqp"]:
        pars["optim_opts"] = json.loads(
            parser.get("OPTIMIZATION_OPTIONS", "optim_opts_mincurv")
        )

    elif opt_type == "mintime":
        pars["curv_calc_opts"] = json.loads(
            parser.get("GENERAL_OPTIONS", "curv_calc_opts")
        )
        pars["optim_opts"] = json.loads(
            parser.get("OPTIMIZATION_OPTIONS", "optim_opts_mintime")
        )
        pars["vehicle_params_mintime"] = json.loads(
            parser.get("OPTIMIZATION_OPTIONS", "vehicle_params_mintime")
        )
        pars["tire_params_mintime"] = json.loads(
            parser.get("OPTIMIZATION_OPTIONS", "tire_params_mintime")
        )
        pars["pwr_params_mintime"] = json.loads(
            parser.get("OPTIMIZATION_OPTIONS", "pwr_params_mintime")
        )

        # modification of mintime options/parameters
        pars["optim_opts"]["var_friction"] = mintime_opts["var_friction"]
        pars["optim_opts"]["warm_start"] = mintime_opts["warm_start"]
        pars["vehicle_params_mintime"]["wheelbase"] = (
            pars["vehicle_params_mintime"]["wheelbase_front"]
            + pars["vehicle_params_mintime"]["wheelbase_rear"]
        )

    # set import path for ggv diagram and ax_max_machines (if required)
    if not (opt_type == "mintime" and not mintime_opts["recalc_vel_profile_by_tph"]):
        file_paths["ggv_file"] = os.path.join(
            file_paths["module"], "inputs", "veh_dyn_info", pars["ggv_file"]
        )
        file_paths["ax_max_machines_file"] = os.path.join(
            file_paths["module"], "inputs", "veh_dyn_info", pars["ax_max_machines_file"]
        )
    return pars, file_paths


if __name__ == "__main__":
    pass
