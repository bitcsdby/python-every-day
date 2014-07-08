# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'
"""
本文实现了 underwater gps 算法的节点类基本理论
水下节点的主要成员变量
self.coor 本地坐标估值
self.now  本地当前时间
self.ctlist 本地收到GPS数据对的列表（coor，recetime）
self.tu  本地时间误差初值

每次收到一个GPS数据的时候，加入到self.ctlist中
self.ctlist的长度为3以上后

调用self.localization()函数进行位置矫正和时间同步
其中，self.coor的估值为三个卫星坐标的均值，（z除外，z是确定值，可通过传感器得到）
进行多次迭代后，可得到收敛后的x，y，z和t
"""

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

    def __init__(self, x, y, z, timenow, a = 1):
        self.coor = Coordinate(x,y,z,timenow)
        self.now = timenow
        self.tu = 0
        self.ctlist = []
        self.ca = a

#get a line of cofficient matrix
    def getcofficient(self, coor):
        if coor == None:
            print 'Invalid argument in getCoefficient'

        ri = self.getri(coor)

 #       print 'coor', coor.x, coor.y
 #       print 'self.coor', self.coor.x,self.coor.y
        ax = (coor.x - self.coor.x) / ri
        ay = (coor.y - self.coor.y) / ri

 #       print ax, ay, ri

        return [ax, ay, -acoustic_velocity]

    #get ^rou - rou ,in which ^rou is sqrt()+c*self.now - c(to_ - ts)
    def getdeltarou(self, ctpair):
#Ri + C ^tu - c(to' - ts)
#^tu = receivetime - (ts + E / acoustic_velocity)
        _rou = self.getri(ctpair.S.coor) + \
               acoustic_velocity * self.tu
        rou = acoustic_velocity * (ctpair.localreceivetime_to_ - ctpair.S.coor.ts)

   #     print ' '
   #     print '_rou',_rou
   #     print 'rou',rou
   #     print ' '
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

#        print 'H matrix'
#        for x in H:
#            print x

        rou1 = self.getdeltarou(self.ctlist[0])
        rou2 = self.getdeltarou(self.ctlist[1])
        rou3 = self.getdeltarou(self.ctlist[2])

        deltarou = [rou1, rou2, rou3]

        invH = np.linalg.inv(H)

        for x in invH:
            print x
            print ''

        rlt = np.dot(invH, deltarou)

        #print 'rlt', rlt

        self.coor.x += rlt[0]
        self.coor.y += rlt[1]
        self.tu += rlt[2]

        #node1.now = rlt[2]
        #node1.ctlist[0].localreceivetime_to_ = rlt[2]
        #node1.ctlist[1].localreceivetime_to_ = rlt[2]
        #node1.ctlist[2].localreceivetime_to_ = rlt[2]


        #print 'x y z'
        print self.coor.x, self.coor.y, self.coor.z
        print 'tu',self.tu
        #print 't'
        #print self.now + self.tu


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

        node1 = Underwaternode((500+250+100) / 3, (400+150+200) / 3, 100, timenow = 0, a = 1.012)

        targetcoor = Coordinate(250, 200, 100, 1.23547)

#caculate original value of tu
#        tu = ((node1.now + propagationtime(S1.coor, targetcoor) - node1.coor.z / acoustic_velocity) +\
#              (node1.now + propagationtime(S2.coor, targetcoor) - node1.coor.z / acoustic_velocity) +\
#              (node1.now + propagationtime(S3.coor, targetcoor) - node1.coor.z / acoustic_velocity)) / 3
#        tu = (S1.coor.ts - node1.now + S2.coor.ts - node1.now + S3.coor.ts - node1.now) / 3

        node1.tu = 0

        node1.ctlist.append(CoorTimePair(S1, node1.now + propagationtime(S1.coor, targetcoor)))
        node1.ctlist.append(CoorTimePair(S2, node1.now + propagationtime(S2.coor, targetcoor)))
        node1.ctlist.append(CoorTimePair(S3, node1.now + propagationtime(S3.coor, targetcoor)))

        #print 'node1.ctlist', node1.ctlist

        for i in range(3):
            node1.localization()

"""
        node1.ctlist.append(CoorTimePair(S1, node1.now + propagationtime(S1.coor, targetcoor), \
                                         node1.now + propagationtime(S1.coor, targetcoor) - node1.coor.z / acoustic_velocity))
        node1.ctlist.append(CoorTimePair(S2, node1.now + propagationtime(S2.coor, targetcoor), \
                                         node1.now + propagationtime(S2.coor, targetcoor) - node1.coor.z / acoustic_velocity))
        node1.ctlist.append(CoorTimePair(S3, node1.now + propagationtime(S3.coor, targetcoor), \
                                         node1.now + propagationtime(S3.coor, targetcoor) - node1.coor.z / acoustic_velocity))
"""