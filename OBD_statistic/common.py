# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'


class Rawdatastructure:
    def __init__(self, dataitem):
        ##define useful data domain here
        self.mil_dist = 0.  # distance after malfunction indicator light on
        self.clr_dist = 0.  # distance after diagnostic codes cleared
        self.initial_mil = 0.  # total mil = initial_mil + mildist + clrdist
        self.vss = 0.  # vehicle speed sensor
        self.load_pct = 0.  # % load value of the engine
        self.rpm = 0  # round per minute of engine
        self.app_r = 0  # % relative accelerator pedal position
        self.dataclean(dataitem)

    """
    dataclean
    dbitem : a dictionary
    """
    def dataclean(self, dataitem):
        # MIL_DIST km
        if dataitem['MIL_DIST'].isdigit():
            self.mil_dist = dataitem['MIL_DIST']
        else:
            print 'invalid MIL_DIST value', dataitem['MIL_DIST']
            return
        # CLR_DIST km
        if dataitem['CLR_DIST'].isdigit():
            self.clr_dist = dataitem['CLR_DIST']
        else:
            print 'invalid CLR_DIST value', dataitem['CLR_DIST']

        # VSS  km/H
        if dataitem['VSS'].isdigit():
            self.vss = int(dataitem['VSS'])
        else:
            print 'invalid VSS_DIST value', dataitem['VSS']

        # LOAD_PCT  100 / 255 %
        if dataitem['LOAD_PCT'].isdigit():
            self.load_pct = int(dataitem['LOAD_PCT']) / 255.0
        else:
            print 'invalid LOAD_PCT value', dataitem['LOAD_PCT']

        # RPM  1/4
        if dataitem['RPM'].isdigit():
            self.rpm = int(dataitem['RPM']) * 0.25
        else:
            print 'invalid RPM value', dataitem['RPM']

        # APP_R 100 / 255%
        if dataitem['APP_R'].isdigit():
            self.load_pct = int(dataitem['APP_R']) / 255.0
        else:
            print 'invalid APP_R value', dataitem['APP_R']

