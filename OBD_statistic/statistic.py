# -*- coding: utf-8 -*-
__author__ = 'bitcsdby

from common import Rawdatastructure

class Statistic:
    def __init__(self):
        self.dbitems = []
        self.dsitems = []
        self.tobrakes = 0 ## time of brakes
        self.tostepongas = 0 ## time of step on the gas
        self.tohighspeed = 0. ## time of high speed working time
        self.toidling = 0. ## time of idling
        self.tripdistance = 0. ## total trip distance
        self.oilconsumption = 0. ## total energy consumption
        self.drivingscore = 0. ## driving score 
        
        
    def getdatafromweb(self,start,end,url):
        ##get data from a web sql. items from id start to id end
        pass

    def dataclean(self):
        ##get useful items from every dbitem, convert raw data to data with real physical meanings
        pass

    def runstatistic(self):
        ##statistic with dsitems
        pass
