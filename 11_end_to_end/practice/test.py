import os
import numpy as np
import pandas as pd
import torch
import gym.wrappers
from nets.imitator import Policy
from utils import make_Dirs, get_EnvInfo

N_TRAJECTORY = 2
N_TIME = 1000
ENV_NAME = "CarRacing-v0"


METHOD = "PracticeSession_BC"
sdir = "./result/" + METHOD + "/"

# prepare save directories
make_Dirs(sdir + "reward/")

env = gym.wrappers.Monitor(gym.make(ENV_NAME), sdir + "video/", force=True)
env.seed(0)
torch.manual_seed(0)
np.random.seed(0)
s_dim, a_dim, transform = get_EnvInfo(env)

policy = Policy(s_dim, a_dim)
policy.load(sdir)
policy.eval()

summary = []
rewards = []

for n_traj in range(1, N_TRAJECTORY + 1):

    result = []
    observation = env.reset()
    action = policy.reset()

    while env.t <= 1.0:
        env.render()
        observation, reward, done, info = env.step(action)

    print("Ready to start run #{}".format(n_traj))

    for t_ in range(1, N_TIME + 1):
        env.render()
        obs = (
            observation
            if transform is None
            else transform(observation.astype(np.uint8))
        )
        action = policy(obs)
        if "Tensor" in str(type(action)):
            action = action.cpu().data.numpy().flatten()
        observation, reward, done, info = env.step(action)
        result.append(reward)
        if done:
            break

    # close everything
    env.close()

    # record trajectory and return at the end of trajectory
    file_name = str(n_traj)
    print("Finish run #{}".format(file_name))
    np.savetxt(
        sdir + "reward/" + file_name + ".csv", np.array([result]).T, delimiter=","
    )
    rewards.append(np.sum(result))
    print("Collected a reward of {}".format(rewards[-1]))
    summary.append([file_name, rewards[-1]])
    pd.DataFrame(summary, columns=["test", "return"]).to_csv(
        sdir + "reward/" + "summary.csv", index=False
    )

print(
    "statistics of total reward:\n\t max: {}\t min: {}"
    "\n\t median: {}\t mean: {}\t std: {}".format(
        np.max(rewards),
        np.min(rewards),
        np.median(rewards),
        np.mean(rewards),
        np.std(rewards),
    )
)
