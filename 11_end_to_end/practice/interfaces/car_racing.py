# coding:utf-8

from pygame.locals import *
import pygame
import time

import sys
import numpy as np

######################################################
class IFCarRacing(object):
    def __init__(self, ab_max=0.15, increment=0.05, auto_brake=0.01, dt=1.0 / 50.0):
        self.AB_MAX = ab_max
        self.INCREMENT = increment
        self.AUTO_BRAKE = auto_brake
        self.DT = dt

    def __call__(self, x):
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            pass
        keys = pygame.key.get_pressed()

        ### acceleration ###
        if keys[pygame.K_a]:
            self.brake -= self.INCREMENT
            self.accel += self.INCREMENT
        else:
            # auto brake
            self.brake += self.AUTO_BRAKE
            self.accel -= self.AUTO_BRAKE
        self.accel = np.clip(self.accel, 0.0, self.AB_MAX)

        ### brake ###
        if keys[pygame.K_s]:
            self.brake += self.INCREMENT
        self.brake = np.clip(self.brake, 0.0, 1.0)

        ### steer ###
        # turn right
        if keys[pygame.K_RIGHT]:
            self.steer += self.INCREMENT
        elif keys[pygame.K_RIGHT] == 0 and self.steer > 0.0:
            self.steer -= np.minimum(self.INCREMENT, self.steer)

        # turn left
        if keys[pygame.K_LEFT]:
            self.steer -= self.INCREMENT
        elif keys[pygame.K_LEFT] == 0 and self.steer < 0.0:
            self.steer += np.minimum(self.INCREMENT, -self.steer)
        self.steer = np.clip(self.steer, -1.0, 1.0)
        #
        time.sleep(self.DT)
        pygame.display.update()
        return np.array([self.steer, self.accel, self.brake])

    def reset(self):
        pygame.init()
        self.screen = pygame.display.set_mode((5, 5))
        pygame.display.set_caption("keyboard event")
        time.sleep(1)
        self.steer = 0.0
        self.accel = 0.0
        self.brake = 0.0
        return np.array([self.steer, self.accel, self.brake])

    def release(self):
        pygame.display.quit()
        pygame.quit()
