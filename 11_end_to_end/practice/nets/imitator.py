import numpy as np
from torch import nn
from nets.abstract import Abstract
import torch.nn.functional as F

######################################################


class Policy(Abstract):
    def __init__(
        self,
        s_dim,
        a_dim,
        opt_params={
            "lr": 1e-3,
            "eps": 1e-8,
            "weight_decay": 0.0,
            "amsgrad": False,
            "tadam": False,
        },
        use_cuda=True,
    ):
        super(Policy, self).__init__(s_dim, a_dim, use_cuda)

        self.loss = nn.MSELoss(reduction="sum")

        self.conv1 = nn.Conv2d(1, 16, kernel_size=5)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 3)

        self.tanh = nn.Tanh()

        nns = self._modules.items()
        self.init("policy", nns, opt_params)

    ###################
    def forward(self, x):

        h = self.convert(x, self.s_dim)

        x = self.pool(F.relu(self.conv1(h)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.tanh(self.fc3(x))

        return x

    ###################
    def criterion(self, a_imitator, a_exp):
        loss = self.loss(a_imitator, a_exp)
        return loss

    ###################
    def reset(self):
        return np.zeros(self.a_dim)
