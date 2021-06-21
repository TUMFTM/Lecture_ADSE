"""
Global Settings
"""
import configparser
import json
import numpy as np


def get_params() -> dict:
    """Create a dictionary with all parameters specified in params.ini

    :return: dictionary containing all parameters
    :rtype: dict"""

    # initialize config parser
    parser = configparser.ConfigParser()

    # determine file to be read
    parser.read(filenames="params.ini")

    # initialize parameter dictionary
    params = dict()

    # read waypoints from file
    xy_waypoints = json.loads(s=parser.get(section="PARAMS", option="xy_waypoints"))
    params["xy_waypoints"] = np.column_stack((xy_waypoints["x"], xy_waypoints["y"]))

    # read obstacles from file
    sd_obstacles = json.loads(s=parser.get(section="PARAMS", option="sd_obstacles"))
    params["sd_obstacles"] = np.column_stack((sd_obstacles["s"], sd_obstacles["d"]))

    # read initial state from file
    params["initial_state"] = json.loads(
        s=parser.get(section="PARAMS", option="initial_state")
    )

    # read discretization from file
    params["discretization"] = json.loads(
        s=parser.get(section="PARAMS", option="discretization")
    )

    # read limits from file
    params["limits"] = json.loads(s=parser.get(section="PARAMS", option="limits"))

    # read cost coefficients from file
    params["cost_coefficients"] = json.loads(
        s=parser.get(section="PARAMS", option="cost_coefficients")
    )

    return params


# EOF
