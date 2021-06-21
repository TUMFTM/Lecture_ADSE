# coding:utf-8

import numpy as np

import torch
from torch import nn, optim
from torch.nn import functional as F


######################################################
class PolicyNormal(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(PolicyNormal, self).__init__()
        self.loc = nn.Linear(s_dim, a_dim)
        self.scale = nn.Linear(s_dim, a_dim)

    def forward(self, x):
        return torch.distributions.normal.Normal(self.loc(x), torch.exp(self.scale(x)))


######################################################
class PolicyLaplace(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(PolicyLaplace, self).__init__()
        self.loc = nn.Linear(s_dim, a_dim)
        self.scale = nn.Linear(s_dim, a_dim)

    def forward(self, x):
        return torch.distributions.laplace.Laplace(
            self.loc(x), torch.exp(self.scale(x))
        )


######################################################
class PolicyBeta(nn.Module):
    def __init__(self, s_dim, a_dim, offset=0.0):
        super(PolicyBeta, self).__init__()
        self.c1 = nn.Linear(s_dim, a_dim)
        self.c0 = nn.Linear(s_dim, a_dim)
        #
        self.offset = offset

    def forward(self, x):
        return torch.distributions.beta.Beta(
            F.softplus(self.c1(x)) + self.offset, F.softplus(self.c0(x)) + self.offset
        )
