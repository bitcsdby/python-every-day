# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'


class Coordinate:
    def __init__(self, x=0, y=0, z=0, t=0):
        """x y z t :4 dimension coordinate"""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.ts = float(t)


class CoorTimePair:
    def __init__(self, S, to_):
        """coor and receive time in pair"""
        self.localreceivetime_to_ = float(to_)
        self.S = S