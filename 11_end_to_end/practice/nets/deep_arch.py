# coding:utf-8

import sys
import numpy as np

import torch
from torch import nn
from torch.nn import functional as F

###############################################################################
def get_ActivationFunc(name):
    # parameters are default
    lists = {
        # relu relatives
        "relu": F.relu,
        "celu": F.celu,
        "softplus": F.softplus,
        # sigmoid relatives
        "sigmoid": torch.sigmoid,
        "softsign": F.softsign,
        "tanh": torch.tanh,
        # shrink relatives
        "hardshrink": F.hardshrink,
        "softshrink": F.softshrink,
        "tanhshrink": F.tanhshrink,
        # handmade
        "swish": lambda x: x * torch.sigmoid(x),
        "mish": lambda x: x * (torch.tanh(F.softplus(x))),
        "linsin": lambda x: 0.5 * (x - 1.0 / np.pi * torch.sin(np.pi * x)),
    }
    if name in lists:
        return lists[name]
    else:
        print("{} is not implemented: {}".format(name, lists))
        sys.exit()


###############################################################################
def check_OutputSize(model, x_dim):
    model.zero_grad()
    x = torch.zeros(x_dim).unsqueeze_(0)
    x = model(x)
    o_dim = tuple(x.size())[1:]
    model.zero_grad()
    return o_dim


###############################################################################
class Xception(nn.Module):
    def __init__(self, i_dim, out_channels, kernel_size, stride, transpose):
        super(Xception, self).__init__()
        #
        in_channels = i_dim[0]
        pointfirst = not (transpose)
        # modules
        cnn = nn.ConvTranspose2d if transpose else nn.Conv2d
        cnns = []
        if pointfirst:
            # pointwise -> depthwise
            cnns.append(cnn(in_channels, out_channels, kernel_size=1, stride=1))
            cnns.append(
                cnn(
                    out_channels,
                    out_channels,
                    kernel_size=kernel_size,
                    stride=stride,
                    groups=out_channels,
                )
            )
        else:
            # depthwise -> pointwise
            cnns.append(
                cnn(
                    in_channels,
                    in_channels,
                    kernel_size=kernel_size,
                    stride=stride,
                    groups=in_channels,
                )
            )
            cnns.append(cnn(in_channels, out_channels, kernel_size=1, stride=1))
        self.cnns = nn.ModuleList(cnns)
        self.o_dim = check_OutputSize(self, i_dim)

    def forward(self, x):
        h = x
        for f in self.cnns:
            h = f(h)
        return h


######################################################
class CNNs(nn.Module):
    def __init__(
        self, s_dim, channels=[8, 16, 32, 64, 128], kernel=5, stride=2, a_name="relu"
    ):
        super(CNNs, self).__init__()
        self.stride = stride
        self.kernels = []
        layers = []
        norms = []
        for c in channels:
            i_dim = layers[-1].o_dim if len(layers) > 0 else s_dim
            self.kernels.append(
                kernel - ((i_dim[1] - kernel) % stride)
            )  # assume: H and W are the same size
            layers.append(Xception(i_dim, c, self.kernels[-1], stride, False))
            norms.append(nn.LayerNorm(layers[-1].o_dim, elementwise_affine=False))
        self.deep_net = nn.ModuleList(layers)
        self.deep_norm = nn.ModuleList(norms)
        self.o_dim = np.prod(layers[-1].o_dim)
        #
        self.fnc_activation = get_ActivationFunc(a_name)

    def forward(self, x):
        h = x
        for f, n in zip(self.deep_net, self.deep_norm):
            h = self.fnc_activation(n(f(h)))
        return h.view(len(h), -1)


######################################################
class DCNNs(nn.Module):
    def __init__(self, i_dim, o_dim, cnn):
        super(DCNNs, self).__init__()
        self.i_dim = cnn.deep_net[-1].o_dim
        if i_dim != np.prod(self.i_dim):
            print(
                "the input size maybe wrong! in: {}, expect: {}".format(
                    i_dim, np.prod(self.i_dim)
                )
            )
            sys.exit()
        layers = []
        norms = []
        for i in range(len(cnn.kernels) - 1, 0, -1):
            layers.append(
                Xception(
                    cnn.deep_net[i].o_dim,
                    cnn.deep_net[i - 1].o_dim[0],
                    cnn.kernels[i],
                    cnn.stride,
                    True,
                )
            )
            norms.append(nn.LayerNorm(layers[-1].o_dim, elementwise_affine=False))
        self.deep_net = nn.ModuleList(layers)
        self.deep_norm = nn.ModuleList(norms)
        self.recon = Xception(
            cnn.deep_net[0].o_dim, o_dim[0], cnn.kernels[0], cnn.stride, True
        )
        self.o_dim = self.recon.o_dim
        if np.prod(o_dim) != np.prod(self.o_dim):
            print(
                "the output size maybe wrong! out: {}, expect: {}".format(
                    self.o_dim, o_dim
                )
            )
            sys.exit()
        #
        self.fnc_activation = cnn.fnc_activation

    def forward(self, x):
        h = x.view(-1, *self.i_dim)
        for f, n in zip(self.deep_net, self.deep_norm):
            h = self.fnc_activation(n(f(h)))
        return torch.sigmoid(self.recon(h))


######################################################
class FCNs(nn.Module):
    def __init__(self, s_dim, h_dims=[100] * 5, a_name="relu"):
        super(FCNs, self).__init__()
        # network structure
        hs_dims = [s_dim] + h_dims
        self.o_dim = hs_dims[-1]
        layers = []
        norms = []
        for i in range(len(hs_dims) - 1):
            layers.append(nn.Linear(hs_dims[i], hs_dims[i + 1]))
            norms.append(nn.LayerNorm(hs_dims[i + 1], elementwise_affine=False))
        self.deep_net = nn.ModuleList(layers)
        self.deep_norm = nn.ModuleList(norms)
        #
        self.fnc_activation = get_ActivationFunc(a_name)

    def forward(self, x):
        h = x
        for f, n in zip(self.deep_net, self.deep_norm):
            h = self.fnc_activation(n(f(h)))
        return h
