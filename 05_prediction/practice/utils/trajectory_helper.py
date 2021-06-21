import os
import pandas as pd
import sqlite3
import numpy as np


def angle_between(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'::

    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    if np.linalg.norm(v1) == 0:
        return 0.0
    else:
        return np.unwrap(
            np.array(
                [
                    0.0,
                    np.arccos(np.dot(v1 / np.linalg.norm(v1), np.array(v2)))
                    * np.sign(v1[1]),
                ]
            )
        )[1]


def get_heading(xy):

    heading_list = [
        angle_between(xy[u + 1] - xy[u], [1, 0]) for u in range(len(xy) - 1)
    ]
    heading_list.append(heading_list[-1])
    return heading_list


def get_heading_hist(xy):

    if not isinstance(xy, list):
        xy = list(xy)
    heading_list = [
        angle_between(xy[u] - xy[u + 1], [1, 0]) for u in range(len(xy) - 1)
    ]
    heading_list.append(heading_list[-1])

    return np.array(heading_list)


def get_abs_anglediff(angle1, angle2):
    return np.abs(np.unwrap(np.array([0, angle1 - angle2]), discont=np.pi)[1])


def transform_trajectory(trajectory, translation, rotation):

    rot_mat = np.array(
        [[np.cos(rotation), -np.sin(rotation)], [np.sin(rotation), np.cos(rotation)]]
    )
    transformed_trajectory = []

    for point in trajectory:
        point -= translation
        point = point @ rot_mat
        transformed_trajectory.append(point)

    return transformed_trajectory


def write_to_SQL(filename, dataframe):
    target_path = os.path.join(os.path.dirname(os.path.dirname(filename)), "target")
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    target_file = os.path.join(
        target_path, os.path.basename(filename).replace(".dat", ".sqlite")
    )
    if os.path.exists(target_file):
        print(f"SQL lib for {filename} already exists --> return")
        return

    table_name = "SQ_" + os.path.splitext(os.path.basename(filename))[0]

    conn = sqlite3.connect(target_file)
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE {} (TimeStamp text, TrackID number, X number, Y number,  Vx number, Vy number, \
            Ax number, Ay number,  Yaw number, YawRate number,  Length number, Width number,  Height number, \
            ObjectType text, ObjectProp number, CityName text)".format(
            table_name
        )
    )
    dataframe.to_sql(table_name, conn, if_exists="replace", index=False)

    cursor.execute("SELECT * FROM {}".format(table_name))
    conn.commit()
    conn.close()


def read_from_SQL(filename, rdb=None, data_list1=None, data_list2=None):
    if not os.path.exists(filename):
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
        if not os.path.exists(filename):
            raise ValueError("invalid filepath")

    conn = sqlite3.connect(filename)
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_list = [name[0] for name in res]

    if data_list1 is not None:
        len_data1 = len([d for d in data_list1 if d.find(rdb) == 0])
        data_frame_list1 = [None] * len_data1

        if data_list2 is None:
            j1 = 0
            for table_name in tables_list:
                if table_name in data_list1:
                    data_frame_list1[j1] = pd.read_sql_query(
                        "SELECT * FROM {}".format(table_name), conn
                    )
                    j1 += 1
        else:
            len_data2 = len([d for d in data_list2 if d.find(rdb) == 0])
            data_frame_list2 = [None] * len_data2

            j1 = 0
            j2 = 0
            for table_name in tables_list:
                if table_name in data_list1:
                    data_frame_list1[j1] = pd.read_sql_query(
                        "SELECT * FROM {}".format(table_name), conn
                    )
                    j1 += 1
                if table_name in data_list2:
                    data_frame_list2[j2] = pd.read_sql_query(
                        "SELECT * FROM {}".format(table_name), conn
                    )
                    j2 += 1
    else:
        data_frame_list1 = []
        for table_name in tables_list:
            data_frame_list1.append(
                (pd.read_sql_query("SELECT * FROM {}".format(table_name), conn))
            )

    conn.close()

    if data_list1 is None:
        if len(data_frame_list1) == 1:
            return data_frame_list1[0]
        else:
            data_frame_list1
    else:
        if data_list2 is None:
            return data_frame_list1, None
        else:
            return data_frame_list1, data_frame_list2
