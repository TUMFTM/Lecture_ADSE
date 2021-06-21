# coding:utf-8

import numpy as np

import torch
from torch import nn, optim

#######################################################


class Abstract(nn.Module):
    def __init__(
        self, s_dim, a_dim, dist, use_cuda=True,
    ):
        super(Abstract, self).__init__()
        #
        self.name = ""
        self.device = torch.device(
            "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
        )
        # store config of state action space
        self.s_dim = s_dim
        self.a_dim = a_dim

    ###################
    def forward(self, x):
        return x

    ###################
    def init(self, name, nns, opt_params):
        self.name = name
        self.nets = nn.ModuleDict(nns)
        ops = opt_params.copy()
        tadam = ops.pop("tadam", False)

        self.optimizer = optim.Adam(self.nets.parameters(), **ops)

        # send to gpu
        self.to(self.device)
        #
        print(self)
        print(self.optimizer)

    ###################
    def release(self, sdir):
        # save models
        torch.save(self.state_dict(), sdir + self.name + "_model.pth")
        torch.save(self.optimizer.state_dict(), sdir + self.name + "_optim.pth")

    ###################
    def load(self, ldir):
        try:
            self.load_state_dict(torch.load(ldir + self.name + "_model.pth"))
            self.optimizer.load_state_dict(torch.load(ldir + self.name + "_optim.pth"))
            print("load parameters are in" + ldir)
            return True
        except:
            print("parameters are not loaded")
            return False

    ###################
    def convert(self, x, dim):
        rtv = None
        if "Tensor" in str(type(x)):
            # assume: one or three dimensional, and if three, x is already CxHxW
            rtv = (
                x.view(-1, dim)
                if isinstance(dim, int)
                else x.view(-1, dim[0], dim[1], dim[2])
            )
        else:
            # assume: one or three dimensional, and if three, x is HxWxC
            tmp = (
                np.array(x).reshape((-1, dim))
                if isinstance(dim, int)
                else np.array(x)
                .reshape((-1, dim[1], dim[2], dim[0]))
                .transpose(0, 3, 1, 2)
            )
            rtv = torch.from_numpy(tmp.astype("float32"))
        return rtv.to(self.device)
