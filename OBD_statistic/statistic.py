# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'

from common import Rawdatastructure
import urllib2
import json


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

    def getdatafromweb(self, start, count, url):
        ## get data from a web sql. items from id start to id end
        url += 'from=' + str(start) + '&' + 'count=' + str(count)
        print url
        # from=113230&count=210

        request = urllib2.Request(url)
        html = urllib2.urlopen(request)

        self.dbitems = json.loads(html.read())['msg']['data']

        self.dbitems.reverse()

        for item in self.dbitems:
            if int(item['VSS']) == 0x88:
                print 'invalid dbitem'
                continue;
            dsitem = Rawdatastructure(item)
            self.dsitems.append(dsitem)

        print len(self.dsitems)

        # print self.dbitems
        # print type(self.dbitems['data'])
        # self.dbitems['data']

    def runstatistic(self):
        print len(self.dsitems)
        for item in self.dsitems:
            item.printvalues()
            print ''
        ## statistic with dsitems
        # print self.dbitems


if __name__ == '__main__':
    s = Statistic()
    url = 'http://www.ecloudan.com/api.php?p=vanet.obd.getdata.obd&access_token=f313e38dfb990557b49f475d42e89237ddda905a34a086fa48e7f26d9894242b&'

    s.getdatafromweb(113230, 210, url)
    s.runstatistic()