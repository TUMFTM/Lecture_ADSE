# coding:utf-8

import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
from torchvision import transforms

import gym
import gym.wrappers


######################################################
def make_Dirs(d):
    for i, p in enumerate(d.split("/")):
        p = "/".join(d.split("/")[:i]) + "/" + p
        if not os.path.isdir(p):
            os.mkdir(p)


######################################################
def save_Result(sdir, name, data):
    plt.clf()
    for key, val in data.items():
        plt.plot(range(len(val)), val, label=key)
    plt.legend()
    plt.savefig(sdir + name + ".pdf")
    pd.DataFrame(data).to_csv(sdir + name + ".csv")


######################################################
def save_Image(sdir, data, name, n_repeat):
    plt.clf()
    array = data[0].to("cpu")
    array = array.data.numpy().astype("f")
    # array = array.transpose(1, 2, 0)
    array = array * 255.0
    # img = Image.fromarray(np.uint8(array))
    # draw = ImageDraw.Draw(img)
    # img.save(sdir + name +".png")
    plt.imshow(array[0], cmap="gray")
    plt.savefig(sdir + name + str(n_repeat) + ".png")


######################################################
def wait_Zoom(env, action, is_view):
    while True:
        # print(env.t)
        if is_view:
            env.render()
        observation, reward, done, info = env.step(action)
        if env.t >= 1.0:
            break
    print("Ready to start!")
    return observation


def get_EnvInfo(env):
    s_dim = (
        env.observation_space.shape[0]
        if len(env.observation_space.shape) == 1
        else (1, 32, 32)
    )
    a_dim = env.action_space.shape[0]
    trans = (
        None
        if isinstance(s_dim, int)
        else transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize((32, 32)),
                transforms.Grayscale(),
                transforms.ToTensor(),
            ]
        )
    )
    return s_dim, a_dim, trans


def init_Policy(
    env, policy, scale_factor=2.0, dataset=None, n_epoch=10, n_sample=256, n_count=100
):
    # prepare prior
    if "laplace" in policy.dist:
        try:
            loc = torch.from_numpy(
                (0.5 * (env.action_space.high + env.action_space.low)).astype(
                    np.float32
                )
            ).to(policy.device)
            scale = torch.from_numpy(
                (0.5 * (env.action_space.high - env.action_space.low)).astype(
                    np.float32
                )
            ).to(policy.device)
        except:
            loc = torch.zeros(policy.a_dim, dtype=np.float32, device=policy.device)
            scale = torch.ones(policy.a_dim, dtype=np.float32, device=policy.device)
        scale /= scale_factor * np.sqrt(2.0)
        prior = torch.distributions.laplace.Laplace(loc, scale)
    else:
        try:
            loc = torch.from_numpy(
                (0.5 * (env.action_space.high + env.action_space.low)).astype(
                    np.float32
                )
            ).to(policy.device)
            scale = torch.from_numpy(
                (0.5 * (env.action_space.high - env.action_space.low)).astype(
                    np.float32
                )
            ).to(policy.device)
        except:
            loc = torch.zeros(policy.a_dim, dtype=np.float32, device=policy.device)
            scale = torch.ones(policy.a_dim, dtype=np.float32, device=policy.device)
        scale /= scale_factor
        prior = torch.distributions.normal.Normal(loc, scale)
    policy.prior = prior

    def _init_policy(so):
        a_ = policy(so)
        loss = policy.criterion_init().mean()
        policy.optimizer.zero_grad()
        loss.backward()
        policy.optimizer.step()
        return loss.data.item()

    if prior is not None:
        print("towards {}, {}".format(prior.mean, prior.variance))
        policy.train()
        for epch in range(1, n_epoch + 1):
            loss_sum = 0.0
            loss_num = 0
            if dataset is not None:
                for batch_idx, (so, a_) in enumerate(dataset):
                    loss_sum += _init_policy(so)
                    loss_num += 1
            else:
                for _ in range(n_count):
                    so = np.array(
                        [
                            env.observation_space.sample().tolist()
                            for _ in range(n_sample)
                        ]
                    )
                    loss_sum += _init_policy(so)
                    loss_num += 1
            print(
                "{}-th epoch to initialize policy was end: \n\tloss = {}".format(
                    epch, loss_sum / loss_num
                )
            )


######################################################
def collect_Data(
    env,
    policy,
    env_name,
    transform,
    n_time,
    is_view,
    sdir_traj=None,
    sdir_reward=None,
    sdir_action=None,
    file_name=None,
):
    trajectory = []
    result = []
    actions = []
    observation = env.reset()
    action = policy.reset()

    # wait until zoom
    if "CarRacing" in env_name:
        observation = wait_Zoom(env, action, is_view)
    # main loop to update trajectory
    for t_ in range(1, n_time + 1):
        if is_view:
            env.render()
        obs = (
            observation
            if transform is None
            else transform(observation.astype(np.uint8))
        )
        # print(obs)
        action = policy(obs)
        if "Tensor" in str(type(action)):
            action = action.cpu().data.numpy().flatten()
        if sdir_traj is not None:
            trajectory.append(
                (
                    np.asarray(observation, dtype=np.float32),
                    np.asarray(action, dtype=np.float32),
                )
            )
        observation, reward, done, info = env.step(action)
        if sdir_reward is not None:
            result.append(reward)
        if sdir_action is not None:
            actions.append(action.tolist())
        if done:
            break

    # record trajectory and return at the end of trajectory
    if file_name is None:
        file_name = datetime.now().strftime("%Y%m%d%H%M%S")
    rtv = []
    print("Finish one episode, and record it to {}".format(file_name))
    if sdir_traj is not None:
        pd.to_pickle(trajectory, sdir_traj + file_name + ".gz")
        rtv.append(sdir_traj + file_name + ".gz")
    if sdir_reward is not None:
        np.savetxt(
            sdir_reward + file_name + ".csv", np.array([result]).T, delimiter=","
        )
        rtv.append(np.sum(result))
    if sdir_action is not None:
        actions = np.array(actions)
        plt.clf()
        for idx in range(len(action)):
            sns.distplot(actions[:, idx], label=str(idx))
        plt.legend()
        plt.tight_layout()
        plt.savefig(sdir_action + file_name + ".pdf")
    return rtv
