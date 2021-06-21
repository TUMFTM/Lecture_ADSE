# coding:utf-8

from pygame.locals import *
import pygame

import sys
import numpy as np

from interfaces.car_racing import IFCarRacing


######################################################
class Policy(object):
    def __init__(self, env_name, **kwargs):
        if "CarRacing" in env_name:
            self.interface = IFCarRacing()

    def __call__(self, x):
        return self.interface(x)

    def reset(self):
        return self.interface.reset()

    def release(self):
        return self.interface.release()
