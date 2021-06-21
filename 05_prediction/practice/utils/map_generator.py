import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import shapely.wkt
import json

repo_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(repo_path)

from utils.trajectory_helper import (
    get_heading,
    transform_trajectory,
    get_abs_anglediff,
    read_from_SQL,
)
#  https://github.com/Mjrovai/Python4DS/blob/master/Vector_Mapping_Python/Vectorial_Maps.ipynb


class LaneGenerator:
    def __init__(self, path, config):
        self.sample_distance = config["sample_distance"]
        self.trajectory_candidates = config["num_trajectory_candidates"]
        self.numel_lane_candidates = config["num_lane_candidates"]
        self.num_candidates_per_lane = config["num_candidates_per_lane"]
        self.len_lane_candidates = config["len_lane_candidates"]
        self.max_angle_diff = config["max_angle_diff"]

        self.path = path
        if self.path.find(".xml") > 0:
            self.lane_root = self.get_root(path)
        else:
            self.lane_root = read_from_SQL(path)
        self.lane_frame = self.create_lane_frame()
        self.border_frame = self.create_border_frame()

    def get_root(self, path):
        root = ET.parse(path).getroot()
        return root

    def get_closestIDs(self, translation):
        dist_list = []
        for _, item in self.lane_frame.iterrows():
            for x, y in zip(item.x, item.y):
                dist_list.append(
                    (np.linalg.norm(np.array([x, y]) - translation), item.ID)
                )
        dist_list = sorted(dist_list, key=lambda x: x[0])

        IDlist = []
        for _, key in dist_list:
            if key not in IDlist:
                IDlist.append(key)
                if len(IDlist) == self.numel_lane_candidates:
                    break
        if not len(IDlist):
            print("no close IDs found")
        return IDlist

    def get_next(self, ID, graph, graph_chain, chain_list):
        if len(graph[ID]) == 0:
            chain_list.append(graph_chain)
            return chain_list
        else:
            for j, lk in enumerate(graph[ID]):
                if j > 0:
                    graph_chain = graph_chain[
                        : graph_chain.index(list(graph[ID])[j - 1])
                    ]
                if lk not in graph_chain:
                    graph_chain.append(lk)
                    chain_list = self.get_next(lk, graph, graph_chain, chain_list)
            return chain_list

    def get_lane_chain(
        self, closeIDs, translation, ref_heading, len_lane_canditate, debug, hist=None
    ):
        traj_list = []
        head_sup_list = []

        rotation = ref_heading[0]
        temp_list = []
        for initID in closeIDs:
            graph = self.create_search_graph()

            graph_chain = [initID]
            chain_list = []
            chain_list = self.get_next(initID, graph, graph_chain, chain_list)
            chain_list = sorted(chain_list, key=lambda x: -len(x))
            c = chain_list.pop(0)
            lane_list = [c]

            # get most divergent lanes
            if bool(chain_list):
                mind_ind = []
                for k in range(0, len(chain_list)):
                    mind_ind.append(
                        (
                            k,
                            next(
                                iter(
                                    (
                                        [
                                            j
                                            for j, (x, y) in enumerate(
                                                zip(
                                                    c[: len(chain_list[k])],
                                                    chain_list[k],
                                                )
                                            )
                                            if x != y
                                        ]
                                    )
                                )
                            ),
                        )
                    )
                mind_ind = sorted(mind_ind, key=lambda x: x[1])
                for j in range(min(len(chain_list), self.num_candidates_per_lane - 1)):
                    lane_list.append(chain_list[mind_ind[j][0]])

            temp_list.append(lane_list)

        lane_sup_list = []
        kk = 0
        while True:
            no_new_lanes = True
            for u in range(len(temp_list)):
                if len(temp_list[u]) > kk:
                    lane_sup_list.append(temp_list[u][kk])
                    no_new_lanes = False
            kk += 1
            if no_new_lanes:
                break

        for lanes in lane_sup_list:
            x_list = []
            y_list = []
            s_list = []
            heading_list = []
            for IDs in lanes:
                x_list += list(self.lane_frame[self.lane_frame.ID == IDs].x.tolist()[0])
                y_list += list(self.lane_frame[self.lane_frame.ID == IDs].y.tolist()[0])
                s_list += list(self.lane_frame[self.lane_frame.ID == IDs].s.tolist()[0])
            s_resample, xy = self.resample_trajectory(
                np.array(list(zip(x_list, y_list)))
            )
            if len(s_resample) < 2:
                continue
            x_list = list(xy[:len_lane_canditate, 0])
            y_list = list(xy[:len_lane_canditate, 1])
            s_list = list(s_resample[:len_lane_canditate])
            xy = np.array(list(zip(x_list, y_list)))
            heading_list = get_heading(xy)

            transformed = transform_trajectory(list(xy), translation, rotation)
            if (
                get_abs_anglediff(heading_list[0], np.mean(np.unwrap(ref_heading)))
                > self.max_angle_diff
            ):
                continue

            relative_heading = [get_abs_anglediff(hd, rotation) for hd in heading_list]

            # fill up lanes
            if len(transformed) > self.len_lane_candidates:
                transformed = transformed[: self.len_lane_candidates]
                relative_heading = heading_list[: self.len_lane_candidates]
            else:
                transformed += [np.zeros(2)] * (
                    self.len_lane_candidates - len(transformed)
                )
                relative_heading += [0] * (self.len_lane_candidates - len(heading_list))

            traj_list.append(transformed)
            head_sup_list.append(relative_heading)

        # fill up trajectory candidates
        if len(traj_list) < self.trajectory_candidates:
            traj_list += [list(np.zeros([self.len_lane_candidates, 2]))] * (
                self.trajectory_candidates - len(traj_list)
            )
            head_sup_list += [list(np.zeros([self.len_lane_candidates]))] * (
                self.trajectory_candidates - len(traj_list)
            )
            lane_sup_list += [[None]] * (
                self.trajectory_candidates - len(lane_sup_list)
            )

        if (
            np.linalg.norm(traj_list) == 0
            and debug
            or len(lane_sup_list) == 0
            and debug
        ):
            print("lane_sup_list is:")
            print(lane_sup_list)
            print(np.linalg.norm(traj_list))

        return (
            traj_list[: self.trajectory_candidates],
            head_sup_list[: self.trajectory_candidates],
            lane_sup_list[: self.trajectory_candidates],
        )

    def create_search_graph(self):
        lane_list = []
        successor_list = []
        for _, items in self.lane_frame.iterrows():
            lane_list.append(items.ID)
            successor_list.append(set(items.sucessors))
        return dict(zip(lane_list, successor_list))

    def create_lane_frame(self):

        keys = ["ID", "x", "y", "s", "heading", "type", "sucessors"]
        x_list = []
        y_list = []
        s_list = []
        heading_list = []
        ID_list = []
        successor_list = []
        type_list = []

        element_tag = "trafficLane"

        if isinstance(self.lane_root, pd.core.frame.DataFrame):
            trafficLanes = self.lane_root[self.lane_root.type == element_tag]
            allID = trafficLanes.id.unique()
            # allID = list(map(int, list(allID[~ np.isnan(allID)])))
            iter_tl = trafficLanes.iterrows()
            pd_series_bool = True
        else:
            allID = [
                int(item.find("identifier").text)
                for item in self.lane_root.iter(element_tag)
            ]
            iter_tl = self.lane_root.iter(element_tag)
            pd_series_bool = False

        for item in iter_tl:
            if pd_series_bool:
                item = item[1]
                if np.isnan(item.id):
                    continue
                ID_list.append(int(item.id))
                if item.successors is None:
                    successor_list.append([])
                else:
                    suc = [
                        int(float(k))
                        for k in item.successors.split("[")[1:][0]
                        .split("]")[0]
                        .split(", ")
                    ]
                    successor_list.append(suc)
            else:
                ID_list.append(int(item.find("identifier").text))
                suc = item.find("successors")
                if suc is not None:
                    successor_list.append(
                        [int(s.text) for s in suc if int(s.text) in allID]
                    )
                else:
                    successor_list.append([])
            s_ref, xy = self.get_lane_sample(item, lspace=True)
            heading_list.append(get_heading(xy))
            x_list.append(xy[:, 0])
            y_list.append(xy[:, 1])
            s_list.append(s_ref)
            type_list.append(element_tag)

        df = pd.DataFrame(
            dict(
                zip(
                    keys,
                    [
                        ID_list,
                        x_list,
                        y_list,
                        s_list,
                        heading_list,
                        type_list,
                        successor_list,
                    ],
                )
            )
        )

        return df

    def create_border_frame(self):

        keys = ["ID", "x", "y", "s", "heading", "type"]
        x_list = []
        y_list = []
        s_list = []
        heading_list = []
        ID_list = []
        type_list = []

        if isinstance(self.lane_root, pd.core.frame.DataFrame):
            element_tag = "boundary"
            borderLines = self.lane_root[self.lane_root.type == element_tag]
            allID = list(range(len(borderLines)))
            iter_bl = borderLines.iterrows()
            pd_series_bool = True
        else:
            element_tag = "borderLine"
            iter_bl = self.lane_root.iter(element_tag)
            allID = [int(j) for j, _ in enumerate(self.lane_root.iter(element_tag))]
            pd_series_bool = False

        id_iter = iter(allID)

        for item in iter_bl:
            item_id = next(id_iter)
            if pd_series_bool:
                item = item[1]
                item_geo = item.geometry
            else:
                item_geo = item.findtext("geometry")
            if item_geo is None:
                continue
            ID_list.append(item_id)
            s_ref, xy = self.get_lane_sample(item, lspace=True)
            heading_list.append(get_heading(xy))
            x_list.append(xy[:, 0])
            y_list.append(xy[:, 1])
            s_list.append(s_ref)
            type_list.append("borderLine")

        df = pd.DataFrame(
            dict(zip(keys, [ID_list, x_list, y_list, s_list, heading_list, type_list]))
        )

        return df

    def get_lane_arc(self, xy):
        vec = np.diff(xy, axis=0)
        s = np.concatenate([np.zeros(1), np.cumsum(np.linalg.norm(vec, axis=1))])
        return s

    def get_sucessorlist(self, index):
        lane = self.lane_root.shape(index)
        if len(lane) > 3:
            return [suc for suc in lane[3]]
        else:
            return []

    def get_lane_sample(self, lane, s0=0.0, lspace=False):
        if isinstance(lane, pd.core.series.Series):
            xy = np.array(shapely.wkt.loads(lane.geometry).xy).T
        else:
            xy = np.array(shapely.wkt.loads(lane.find("geometry").text).xy).T
        return self.resample_trajectory(xy, s0, lspace=lspace)

    def resample_trajectory(self, xy, s0=0.0, lspace=False):
        s_ref = self.get_lane_arc(xy)
        if lspace:
            s_temp = np.linspace(s_ref[0], s_ref[-1], 100)
        else:
            s_temp = np.arange(s_ref[0], s_ref[-1], self.sample_distance)
        xy_resample = np.zeros([len(s_temp), 2])
        s_resample = s_temp + s0
        xy_resample[:, 0] = np.interp(s_temp, s_ref, xy[:, 0])
        xy_resample[:, 1] = np.interp(s_temp, s_ref, xy[:, 1])
        return s_resample, xy_resample


if __name__ == "__main__":
    with open("configs/data_config.json", "r") as f:
        data = f.read()
    config = json.loads(data)
    # xml_path = './data/openDD/source/example/map_rdb1/map_rdb1_UTM32N.xml'
    xml_path = r"C:\Daten\Karle\source\repos\iup_opendd\data\openDD\source\rdb4\map_rdb4\map_rdb4.sqlite"
    LaneGenerator(xml_path, config)
