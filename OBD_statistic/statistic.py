# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'

from common import Rawdatastructure
import urllib2
import json
import pickle


class Statistic:
    def __init__(self):
        self.dbitems = []
        self.dsitems = []
        self.tobrakes = 0 ## time of brakes
        self.tostepongas = 0 ## time of step on the gas
        self.tohighspeed = 0. ## time of high speed working time
        self.toidling = 0. ## time of idling
        self.mildistance = 0. ## total Malfunction Indicator Light trip distance
        self.clrdistance = 0. ## total Malfunction Indicator Clear trip distance
        self.oilconsumption = 0. ## total energy consumption
        self.drivingscore = 0. ## driving score 

    def getdatafromweb(self, start, count, url, dspath, dbpath):
        ## get data from a web sql. items from id start to id end
        url += 'from=' + str(start) + '&' + 'count=' + str(count)
        print url
        # from=113230&count=210

        request = urllib2.Request(url)
        html = urllib2.urlopen(request)
        self.dbitems = json.loads(html.read())['msg']['data']

        self.dbitems.reverse()

        print len(self.dbitems)
        for item in self.dbitems:
            #print int(item['VSS'])
            if int(item['VSS']) != 0x88:
                dsitem = Rawdatastructure(item)
                self.dsitems.append(dsitem)
            #else:
               #print 'invalid dbitem'
        print len(self.dsitems)

        with open(dspath, 'wb') as latesdstdata:
            pickle.dump(self.dsitems, latesdstdata)

        with open(dbpath, 'wb') as latestdbdata:
            pickle.dump(self.dbitems, latestdbdata)

        print len(self.dsitems), len(self.dbitems)
        #print len(self.dsitems)


        # print self.dbitems
        # print type(self.dbitems['data'])
        # self.dbitems['data']


    def getdatafromlocal(self, dspath, dbpath):
        with open(dspath, 'rb') as dsfile:
            self.dsitems = pickle.load(dsfile)
        with open(dbpath, 'rb') as dbfile:
            self.dbitems = pickle.load(dbfile)

        print len(self.dsitems), len(self.dbitems)

    def runstatistic(self):
        l = len(self.dsitems)

        for i in range(l-1):
            #self.dsitems[i].printvalues()
            # print self.dsitems[i].vss
            #print type(self.dsitems[i].load_pct)
            #print 'MAF', self.dsitems[i].maf
            maxspeed = 0.0
            averagespped = 0.0


            ## load_pct
            if self.dsitems[i].load_pct > 40 and self.dsitems[i].vss > self.dsitems[i+1].vss:
                #print 'load_pct', self.dsitems[i].load_pct
                #print 'vss', self.dsitems[i].vss, self.dsitems[i+1].vss
                #print ''
                self.tobrakes += 1

            if self.dsitems[i].load_pct < 14 and self.dsitems[i].vss <= self.dsitems[i+1].vss:
                #print 'load_pct', self.dsitems[i].load_pct
                #print 'vss', self.dsitems[i].vss, self.dsitems[i+1].vss
                #print ''
                self.tostepongas += 1

            ## speed
            if self.dsitems[i].vss > maxspeed:
                maxspeed = self.dsitems[i].vss
            if self.dsitems[i].vss > 70:
                print 'vss', self.dsitems[i].vss

            ##idling
            if self.dsitems[i].rpm == 0 and self.dsitems[i].app_r != 0:
                print self.dsitems[i].rpm, self.dsitems[i].app_r
                self.toidling += 1

            ##energy consumption
            #print 'MAF', self.dsitems[i].maf

            # DIST
            if self.dsitems[i].mil_dist > maxmil_dist:
                self.mildistance = self.dsitems[i].mil_dist
            if self.dsitems[i].clr_dist > maxclr_dist:
                self.clrdistance = self.dsitems[i].clr_dist
            #print 'MIL_DIST cLRDIST', self.dsitems[i].mil_dist, self.dsitems[i].clr_dist

        print '急刹车次数', self.tobrakes
        print '急踩油门次数', self.tostepongas
        print '高速巡航时间', self.tohighspeed * 7
        print '怠速时间', self.toidling * 7
        print '行驶里程', '总里程', self.mildistance + self.clrdistance, \
                          '故障', self.mildistance, '正常', self.clrdistance
        print ''
        #print '行驶里程', self
        ## statistic with dsitems
        # print self.dbitems


if __name__ == '__main__':
    s = Statistic()
    url = 'http://www.ecloudan.com/api.php?p=vanet.obd.getdata.obd&access_token=f313e38dfb990557b49f475d42e89237ddda905a34a086fa48e7f26d9894242b&'
    dsfilepath = 'latest_dsdata.pickle'
    dbfilepath = 'latest_dbdata.pickle'

    #s.getdatafromweb(2400, 301, url, dsfilepath, dbfilepath)
    s.getdatafromlocal(dsfilepath, dbfilepath)

    s.runstatistic()