# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'


class Rawdatastructure:
    def __init__(self, dataitem):
        ##define useful data domain here
        self.mil_dist = 0.00  # distance after malfunction indicator light on
        self.clr_dist = 0.00  # distance after diagnostic codes cleared
        self.initial_mil = 0.00  # total mil = initial_mil + mildist + clrdist
        self.vss = 0.00  # vehicle speed sensor
        self.load_pct = 0.00  # % load value of the engine
        self.rpm = 0  # round per minute of engine
        self.app_r = 0.00  # % relative accelerator pedal position
        self.dataclean(dataitem)

    def printvalues(self):
        print 'MIL_DIST', self.mil_dist
        print 'CLR_DIST', self.clr_dist
        print 'VSS', self.vss
        print 'LOAD_PCT', self.load_pct
        print 'RPM', self.rpm
        print 'APP_R', self.app_r

    """
    dataclean
    dbitem : a dictionary
    """
    def dataclean(self, dataitem):
        # MIL_DIST km

        if dataitem['MIL_DIST'].isdigit():
            self.mil_dist = float(dataitem['MIL_DIST'])
        else:
            print 'invalid MIL_DIST value', dataitem['MIL_DIST']
            return
        # CLR_DIST km
        if dataitem['CLR_DIST'].isdigit():
            self.clr_dist = float(dataitem['CLR_DIST'])
        else:
            print 'invalid CLR_DIST value', dataitem['CLR_DIST']

        # VSS  km/H
        if dataitem['VSS'].isdigit():
            self.vss = float(dataitem['VSS'])
        else:
            print 'invalid VSS_DIST value', dataitem['VSS']

        # LOAD_PCT  100 / 255 %
        if dataitem['LOAD_PCT'].isdigit():
            self.load_pct = '%.5f' % (float(dataitem['LOAD_PCT']) / 255.0 * 100)
        else:
            print 'invalid LOAD_PCT value', dataitem['LOAD_PCT']

        # RPM  1/4
        if dataitem['RPM'].isdigit():
            self.rpm = int(dataitem['RPM']) / 4
        else:
            print 'invalid RPM value', dataitem['RPM']

        # APP_R 100 / 255%
        if dataitem['APP_R'].isdigit():
            self.app_r = '%.5f' % (float(dataitem['APP_R']) / 255.0 * 100)
        else:
            print 'invalid APP_R value', dataitem['APP_R']

