# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'

from common import Coordinate
from common import CoorTimePair
from satellite import Satellite
import math
import numpy as np

acoustic_velocity = 1500.0

class Underwaternode:
    def __init__(self, coordinate, time, a = 1):
        self.coor = coordinate
        self.now = time
        self.ctlist = []
        self.ca = a

    def __init__(self, x, y, z, time, a = 1):
        self.coor = Coordinate(x,y,z,time)
        self.now = time
        self.ctlist = []
        self.ca = a

#get a line of cofficient matrix
    def getcofficient(self, coor):
        if coor == None:
            print 'Invalid argument in getCoefficient'

        ri = self.getri(coor)

        print 'coor', coor.x,coor.y
        print 'self.coor', self.coor.x,self.coor.y
        ax = (coor.x - self.coor.x) / ri
        ay = (coor.y - self.coor.y) / ri

        print ax, ay, ri

        return [ax, ay, -acoustic_velocity]

    #get ^rou - rou ,in which ^rou is sqrt()+c*self.now - c(to_ - ts)
    def getdeltarou(self, ctpair):
        _rou = self.getri(ctpair.S.coor) + acoustic_velocity * self.now
        rou = acoustic_velocity * (ctpair.receivetime - ctpair.S.coor.ts)

        return _rou - rou

#get sqrt(xi-xu)^2 ...
    def getri(self, coor1):
        return math.sqrt((coor1.x - self.coor.x) * (coor1.x - self.coor.x) + \
   			             (coor1.y - self.coor.y) * (coor1.y - self.coor.y) + \
   			             (coor1.z - self.coor.z) * (coor1.z - self.coor.z))

#localization and synchronization
    def localization(self):
        if len(self.ctlist) < 3:
            print 'at least 3 ct pairs'
        a1 = self.getcofficient(self.ctlist[0].S.coor)
        a2 = self.getcofficient(self.ctlist[1].S.coor)
        a3 = self.getcofficient(self.ctlist[2].S.coor)

        H = [a1, a2, a3]

        rou1 = self.getdeltarou(self.ctlist[0])
        rou2 = self.getdeltarou(self.ctlist[1])
        rou3 = self.getdeltarou(self.ctlist[2])

        deltarou = [rou1, rou2, rou3]

        invH = np.linalg.inv(H)

        rlt = np.dot(invH, deltarou)

        print 'rlt', rlt


def edistance(coor1, coor2):
    return math.sqrt((coor1.x-coor2.x)*(coor1.x-coor2.x) \
                     + (coor1.y-coor2.y) * (coor1.y-coor2.y) \
                     + (coor1.z - coor2.z) * (coor1.z - coor2.z) )


def propagationtime(coor1, coor2):
    distance = edistance(coor1, coor2)
    return distance / acoustic_velocity

if __name__ == '__main__':
        S1 = Satellite(500., 400., 0., 1.23547)
        S2 = Satellite(250., 150., 0., 1.23547)
        S3 = Satellite(100., 200., 0., 1.23547)

        node1 = Underwaternode(0, 0, 0, 0, a = 1.012)

        targetcoor = Coordinate(250, 200, 100, 1.23547)

        node1.ctlist.append(CoorTimePair(S1, node1.now + propagationtime(S1.coor, targetcoor)))
        node1.ctlist.append(CoorTimePair(S2, node1.now + propagationtime(S2.coor, targetcoor)))
        node1.ctlist.append(CoorTimePair(S3, node1.now + propagationtime(S3.coor, targetcoor)))

        print 'node1.ctlist', node1.ctlist

        print node1.localization()