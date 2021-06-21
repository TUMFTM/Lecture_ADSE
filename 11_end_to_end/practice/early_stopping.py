# coding:utf-8

import numpy as np

###############################################################################
class EarlyStopping(object):
    def __init__(self, mode="patience", min=True, length=10):
        self.mode = mode
        self.is_min = min
        self.length = length
        self.is_active = length > 0
        if self.is_active:
            self.count = 0
            if "patience" in self.mode:
                self.optval = None
                self.optidx = None
            else:
                self.vals = np.zeros(length)
                self.oldval = 0.0
                if "mean" in self.mode:
                    self.fnc = np.mean
                elif "median" in self.mode:
                    self.fnc = np.median

    def __call__(self, res):
        rtv = False
        if self.is_active:
            if "patience" in self.mode:
                if (
                    (self.optval is None)
                    or (self.is_min and res < self.optval)
                    or (not self.is_min and res > self.optval)
                ):
                    self.optval = res
                    self.optidx = self.count
                elif self.count - self.optidx >= self.length:
                    rtv = True
            else:
                self.vals = np.roll(self.vals, 1)
                self.vals[0] = res
                val = self.fnc(self.vals)
                if self.count >= self.length:
                    if (self.is_min and val > self.oldval) or (
                        not self.is_min and val < self.oldval
                    ):
                        rtv = True
                self.oldval = val
            self.count += 1
        return rtv
