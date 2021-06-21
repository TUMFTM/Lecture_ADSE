import sys
import os
import copy
import pickle
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(repo_path)

from utils.trajectory_helper import (
    angle_between,
    get_heading_hist,
    transform_trajectory,
    read_from_SQL,
)
from utils.visualization_helper import visualize
from utils.map_generator import LaneGenerator

cf2 = {
    "ignorepedestrians": "true",
    "ignorecyclists": "true",
    "min_movement": 5.0,
    "rdb": "rdb1",
    "input_time": 3,
    "output_time": 5,
    "sample_frequency": 10,
    "num_lane_candidates": 2,
    "num_trajectory_candidates": 5,
    "num_candidates_per_lane": 3,
    "sample_distance": 4.0,
    "max_angle_diff": 2.356,
    "len_lane_candidates": 50,
    "save_path": "data",
    "data_set": "example",
    "dataset_name": "openDD",
    "data_source": "data/openDD/source",
    "n_neighbours": 5,
    "split": [60, 20, 20],
}


def preprocess_data(config={}):
    # some additional parameters
    for key, value in cf2.items():
        if key not in config.keys():
            config[key] = value

    data_set = config["data_set"]

    print("\nReading SQLites ...")

    rdb_path = os.path.join(
        repo_path, os.path.join(os.path.join(config["data_source"], data_set))
    )

    data_list1 = next(
        iter(
            [
                f.split(".")[0]
                for f in os.listdir(rdb_path)
                if os.path.isfile(os.path.join(rdb_path, f))
                if f.find(".sqlite") > 0
            ]
        )
    )
    rdb_file = os.path.join(rdb_path, data_list1 + ".sqlite")
    sql_data, _ = read_from_SQL(rdb_file, config["rdb"], [data_list1])

    map_dict = {config["rdb"]: LaneGenerator_fn(config, rdb_path)}

    data_setlist = config["data_set"]
    data_frames = sql_data[0]

    print(
        "Extracted {:d} data frames form {:s}".format(len(sql_data[0]), config["rdb"])
    )
    return data_setlist, data_frames, map_dict


def LaneGenerator_fn(config, rdb_path):
    rdb_number = config["rdb"]
    xml_path = os.path.join(
        os.path.join(rdb_path, "map_" + rdb_number), "map_" + rdb_number + "_UTM32N.xml"
    )
    if not os.path.exists(xml_path):
        xml_path = os.path.join(
            os.path.join(rdb_path, "map_" + rdb_number), "map_" + rdb_number + ".sqlite"
        )
    return LaneGenerator(xml_path, config)


def data_frame_fn(
    data_frame, map_dict, config, visz=False, smpl_plt_ID=-1, n_visz=None
):

    if visz and n_visz is None:
        plt.figure()
        ax = plt.gca()
    # some additional parameters
    for key, value in cf2.items():
        if key not in config.keys():
            config[key] = value
    laneGen = map_dict[config["rdb"]]

    ignorepedestrians = config["ignorepedestrians"]
    ignorecyclists = config["ignorecyclists"]
    input_time = config["input_time"]
    output_time = config["output_time"]
    sample_frequency = config["sample_frequency"]
    len_lane_candidates = config["len_lane_candidates"]
    n_neighbours = config["n_neighbours"]

    objIDs = data_frame.OBJID.unique()
    hist_list = []
    u = 0

    if smpl_plt_ID < 0:
        print("\nProcessing {} objects".format(len(objIDs)))

    for objID in tqdm(objIDs):
        obj_frame = data_frame[data_frame.OBJID == objID]
        if obj_frame.CLASS.iloc[0] == "Pedestrian" and ignorepedestrians:
            continue
        if obj_frame.CLASS.iloc[0] == "Bicycle" and ignorecyclists:
            continue

        # resample data to sample_frequency:
        t0 = obj_frame.TIMESTAMP.iloc[0]
        tend = obj_frame.TIMESTAMP.iloc[-1]

        if np.max(np.abs(np.diff(np.diff(obj_frame.TIMESTAMP)))) > 1e-4:
            print(np.diff(obj_frame.TIMESTAMP))

        tinp = np.arange(t0, tend + 1 / sample_frequency / 2, 1 / sample_frequency)
        x = np.interp(tinp, obj_frame.TIMESTAMP, obj_frame.UTM_X)
        y = np.interp(tinp, obj_frame.TIMESTAMP, obj_frame.UTM_Y)

        pos_list = list(np.stack([x, y], axis=1))
        if max([np.isnan(p.any()) for p in pos_list]):
            raise ValueError("NAN pos")

        input_length = int(input_time * sample_frequency)
        output_length = int(output_time * sample_frequency)
        iter_list = np.arange(input_length, len(pos_list) - output_length)

        static_object_count = 0
        not_moving_count = 0
        empty_trajectories_count = 0

        h_temp = [None] * len(iter_list)
        f_temp = [None] * len(iter_list)
        lane_temp = [None] * len(iter_list)
        class_temp = [None] * len(iter_list)
        j = 0

        for ts in iter_list:
            # Cut hist and fut list out of the data array
            hist = np.squeeze(
                np.flip(copy.deepcopy([pos_list[ts - input_length : ts]]), axis=1)
            )
            fut = copy.deepcopy(pos_list[ts : ts + output_length])

            if np.linalg.norm(hist[0] - hist[-1]) < config["min_movement"]:
                _ = h_temp.pop(j)
                _ = f_temp.pop(j)
                _ = lane_temp.pop(j)
                _ = class_temp.pop(j)
                static_object_count += 1
                continue

            # Get translation and rotation
            translation = copy.deepcopy(hist[0])
            not_moving = False
            k = 0
            while True:
                delta = hist[k] - hist[k + 1]
                if np.linalg.norm(delta):
                    break
                k += 1
                if k == len(hist) - 1:
                    not_moving = True
                    break

            if not_moving:
                _ = h_temp.pop(j)
                _ = f_temp.pop(j)
                _ = lane_temp.pop(j)
                _ = class_temp.pop(j)
                not_moving_count += 1
                continue

            rotation = angle_between(delta, [1, 0])

            if np.isnan(rotation) or np.isnan(translation.any()):
                raise ValueError("NAN")

            # Transform hist and fut
            ref_heading = get_heading_hist(hist[: min(len(hist), k + 3)])

            hist = transform_trajectory(hist, translation, rotation)
            fut = transform_trajectory(fut, translation, rotation)
            class_label = obj_frame.CLASS.iloc[
                np.argmin(np.abs(np.array(obj_frame.TIMESTAMP) - tinp[ts]))
            ]

            if abs(hist[1][1]) > 0.1:
                raise ValueError("invalid trajectory transformation")

            # get neigbours
            tmin = tinp[ts - input_length]
            t0 = tinp[ts]
            tmax = tinp[ts + output_length - 1]

            t_past = tinp[ts - input_length : ts]
            t_fut = tinp[ts : ts + output_length]

            frame_temp = data_frame[data_frame.TIMESTAMP >= tmin]
            neighbour_hists = frame_temp[frame_temp.TIMESTAMP < tinp[ts]]
            frame_temp = data_frame[data_frame.TIMESTAMP >= t0]
            neighbour_futs = frame_temp[frame_temp.TIMESTAMP <= tmax]

            present_neighbours_IDs = list(
                neighbour_hists[neighbour_hists.TIMESTAMP > t0 - 0.3].OBJID.unique()
            )
            present_neighbours_IDs.remove(objID)

            hist_neigh_dict = {}
            type_neigh_dict = {}
            fut_neigh_dict = {}

            for ID in present_neighbours_IDs:
                neigh_obj = neighbour_hists[neighbour_hists.OBJID == ID]
                x = np.interp(t_past, neigh_obj.TIMESTAMP, neigh_obj.UTM_X)
                y = np.interp(t_past, neigh_obj.TIMESTAMP, neigh_obj.UTM_Y)
                hist_neigh_dict[ID] = np.stack([x, y], axis=1)
                type_neigh_dict[ID] = neigh_obj.CLASS.iloc[0]

            hist_neigh_dict = dict(
                sorted(
                    hist_neigh_dict.items(),
                    key=lambda item: np.linalg.norm(item[1][-1] - translation),
                )[:n_neighbours]
            )

            closest_neighbour_IDs = list(hist_neigh_dict.keys())

            type_neigh_dict = {k: type_neigh_dict[k] for k in closest_neighbour_IDs}

            for ID in closest_neighbour_IDs:
                neigh_obj = neighbour_futs[neighbour_futs.OBJID == ID]
                if len(neigh_obj) > 0:
                    x = np.interp(t_fut, neigh_obj.TIMESTAMP, neigh_obj.UTM_X)
                    y = np.interp(t_fut, neigh_obj.TIMESTAMP, neigh_obj.UTM_Y)
                    fut_neigh_dict[ID] = transform_trajectory(
                        np.stack([x, y], axis=1), translation, rotation
                    )
                else:
                    fut_neigh_dict[ID] = []

                hist_neigh_dict[ID] = transform_trajectory(
                    hist_neigh_dict[ID], translation, rotation
                )

            # get closest IDs
            closeIDs = laneGen.get_closestIDs(translation)
            traj_list, _, _ = laneGen.get_lane_chain(
                closeIDs, translation, ref_heading, len_lane_candidates, debug=False
            )

            allbounds = [None] * len(laneGen.border_frame)
            for jki, (_, bd) in enumerate(laneGen.border_frame.iterrows()):
                bound_array = np.vstack([bd.x, bd.y]).T
                allbounds[jki] = np.array(
                    transform_trajectory(bound_array, translation, rotation)
                )

            if visz and u == smpl_plt_ID:
                allbounds = [None] * len(laneGen.border_frame)
                for jki, (_, bd) in enumerate(laneGen.border_frame.iterrows()):
                    bound_array = np.vstack([bd.x, bd.y]).T
                    allbounds[jki] = np.array(
                        transform_trajectory(bound_array, translation, rotation)
                    )
                neigh_zip = list(
                    zip(
                        hist_neigh_dict.values(),
                        fut_neigh_dict.values(),
                        type_neigh_dict.values(),
                        closest_neighbour_IDs,
                    )
                )

                for nn in range(n_visz):
                    plt.figure(nn + 1)
                    ax = plt.gca()
                    _ = visualize(
                        ax,
                        hist,
                        fut,
                        traj_list,
                        class_label,
                        objID,
                        allbounds,
                        neigh_zip,
                        n_visz=nn,
                    )
                return 0

            if np.linalg.norm(traj_list) == 0:
                _ = h_temp.pop(j)
                _ = f_temp.pop(j)
                _ = lane_temp.pop(j)
                _ = class_temp.pop(j)
                empty_trajectories_count += 1
                continue

            h_temp[j] = np.array(hist)
            f_temp[j] = np.array(fut)
            lane_temp[j] = np.array(traj_list)
            class_temp[j] = class_label
            j += 1
            u += 1

        if bool(h_temp):
            u += 1
            if not bool(hist_list):
                hist_list = h_temp
                fut_list = f_temp
                lane_list = lane_temp
                class_list = class_temp
                objID_list = [objID] * len(class_temp)
            else:
                hist_list += h_temp
                fut_list += f_temp
                lane_list += lane_temp
                class_list += class_temp
                objID_list += [objID] * len(class_temp)

    sample_num = len(hist_list)

    output = {
        "sampleID": list(range(sample_num)),
        "hist": hist_list,
        "fut": fut_list,
        "lanes": lane_list,
        "classes": class_list,
        "objID": objID_list,
    }

    print("Created dataset with {} trajectories".format(len(output["sampleID"])))

    return output, sample_num


def save_to_file(output, dataset_name):
    if dataset_name == "test":
        dataset_name = "test/openDD_" + cf2["data_set"] + "_" + dataset_name
    elif dataset_name == "validation":
        dataset_name = "validation/openDD_" + cf2["data_set"] + "_" + dataset_name
    elif "train" in dataset_name:
        dataset_name = "training/openDD_" + cf2["data_set"] + "_" + dataset_name

    data_directory = os.path.join(repo_path, "data")
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    dest_dir = os.path.dirname(
        os.path.abspath(os.path.join(data_directory, dataset_name + ".txt"))
    )
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    store_name = os.path.join(data_directory, dataset_name + ".txt")
    with open(store_name, "wb") as fp:
        pickle.dump(output, fp)

    print("Stored data to {}".format(store_name))
    return store_name
