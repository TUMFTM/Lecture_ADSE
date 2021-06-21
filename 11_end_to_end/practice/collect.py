# coding:utf-8

import sys
import pandas as pd
import gym
import gym.wrappers
from interfaces.expert import Policy
from utils import make_Dirs, collect_Data
import random
import matplotlib.pyplot as plt
import numpy as np


# hyperparameters
ENV_NAME = "CarRacing-v0"

N_TRAJECTORY = 1
N_TIME = 1000

SAVE_DIR = "./expert/"
IS_VIDEO = True
IS_APPEND = True


def main():
    # make save directories
    make_Dirs(SAVE_DIR + "trajectory/")
    make_Dirs(SAVE_DIR + "reward/")

    # prepare environment and agent (expert)
    env = gym.make(ENV_NAME)
    env = gym.wrappers.Monitor(
        env, SAVE_DIR + "video/", force=True, video_callable=lambda episode_id: True
    )
    policy = Policy(ENV_NAME)

    if IS_APPEND:
        try:
            summary = pd.read_csv(SAVE_DIR + "summary.csv").values.tolist()
        except:
            summary = []
    else:
        summary = []

    for n_traj in range(1, N_TRAJECTORY + 1):
        rtv = collect_Data(
            env,
            policy,
            ENV_NAME,
            None,
            N_TIME,
            True,
            sdir_traj=SAVE_DIR + "trajectory/",
            sdir_reward=SAVE_DIR + "reward/",
        )
        print(rtv)
        summary.append(rtv)
        if IS_VIDEO:
            env.stats_recorder.save_complete()
            env.stats_recorder.done = True
        # record list of data
        pd.DataFrame(summary, columns=["file", "return"]).to_csv(
            SAVE_DIR + "summary.csv", index=False
        )
    # close everything
    env.close()
    policy.release()

    sampled_trajectories = pd.read_csv(SAVE_DIR + "summary.csv")["file"].values.tolist()
    example_trajectorie = pd.DataFrame(
        pd.read_pickle(sampled_trajectories[random.randint(1, len(summary))])
    )

    state = example_trajectorie.iloc[:, 0].values.tolist()
    action = example_trajectorie.iloc[:, 1].values.tolist()

    #%%

    n_rand = random.randint(1, len(state))
    plt.imshow(state[n_rand] / 255)
    plt.show()
    print(action[n_rand])


#%% md


if __name__ == "__main__":
    main()
