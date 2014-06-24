# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'

from common import Coordinate


class Satellite:
    """docstring for suface satellite"""

    def __init__(self, coordinate, time):
        self.coor = coordinate

    def __init__(self, x, y, z, time):
        self.coor = Coordinate(x, y , z, time)

    def getCoor(self):
        return self.coor