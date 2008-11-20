# NMEA Toolkit
# Copyright (C) 2008 Tim Savage
#
# This file is part of the NMEA Toolkit.
#
# The NMEA Toolkit is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your option)
# any later version.
#
# The NMEA Toolkit is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with the NMEA Toolkit.  If not, see <http://www.gnu.org/licenses/>.

import sys

from parse import *


FIXMODE_UNKNOWN = ''
FIXMODE_AUTO   = 'A'
FIXMODE_MANUAL = 'M'

FIXTYPE_NA = 1  # Fix not available
FIXTYPE_2D = 2  # 2D Fix
FIXTYPE_3D = 3  # 3D Fix

FIXQUALITY_NA   = 0  # Not available/invalid
FIXQUALITY_GPS  = 1  # GPS Fix
FIXQUALITY_DIFF = 2  # Differential GPS fix


def excepted(f, *param):
    try: f(*param)
    except KeyboardInterrupt: raise
    except: return True
    return False


class GPS(object):

    def __init__(self, port, callbacks=None):
        self.port = port

        if isinstance(callbacks, dict):
            self.fix_update = callbacks.get('fix_update', None)
            self.transit_update = callbacks.get('transit_update', None)
            self.satellite_update = callbacks.get('satellite_update', None)
            self.satellite_status_update = callbacks.get('satellite_status_update', None)

        # GPS information
        self.position = latlng((0.0, 0.0))
        self.fixTime = None
        self.fixDate = None
        self.speed = 0.0
        self.track = 0.0
        self.trackVariation = 0.0
        self.fixMode = FIXMODE_UNKNOWN
        self.fixType = FIXTYPE_NA
        self.fixQuality = FIXQUALITY_NA
        self.dop = (0, 0, 0) # (P, H, V)DOP
        self.altitude = 0.0
        self.altitudeUnits = 'm' # meters

        self.satellitesInUse = []
        self.satellites = {}
        self.__satellites = {} # Internal satellite buffer

    def error_message(self, message):
        """ Print out an error message to stderr """
        print >> sys.stderr, "ERROR:", message

    def handle_io(self, soureFd=None, cb_condition=0):
        """ Call on loop to perform io operation

        Can be assigned to a idle callback in the case
        of GTK use gobject.io_add_watch and trigger
        on gobject.IO_IN.

        """
        # External method that can be assigned to a idle loop callback
        # in the case of GTK use a gobject.io_add_watch
        try:
            self.parse_data()
        except KeyboardInterrupt:
            raise
        except: # Use instead of finally as we want to handle keyboard interrupts
            self.error_message("Unknown error")
        return True

    def parse_data(self):
        """ Parse data off port

        Can be called directly instead of using
        handle_io. If calling from an idle loop it is
        recommended to use handle_io as it will
        return a positive result and handle any
        exceptions that may be raised.

        """
        lines = self.port.read_buffered()
        for line in lines:
            try:
                sentence = Sentence(line)
            except ParseError, ex:
                self.error_message(str(ex))
            else:
                if sentence.source != "GP":
                    self.error_message("Invalid source")
                else:
                    # Dispatch to message parser
                    mname = '_parse_' + sentence.message
                    if hasattr(self, mname):
                        method = getattr(self, mname)
                        if excepted(method, sentence): print "Parse Error:", line
                    else: self.error_message("Unknown message")

    def _on_fix_update(self):
        if self.fix_update:
            if excepted(self.fix_update, self):
                self.error_message('"fix_update" raised an exception')

    def _on_transit_update(self):
        if self.transit_update:
            if excepted(self.transit_update, self):
                self.error_message('"transit_update" raised an exception')

    def _on_satellite_update(self):
        if self.satellite_update:
            if excepted(self.satellite_update, self):
                self.error_message('"satellite_update" raised an exception')

    def _on_satellite_status_update(self):
        if self.satellite_status_update:
            if excepted(self.satellite_status_update, self):
                self.error_message('"satellite_status_update" raised an exception')

    def _parse_GGA(self, sentence):
        """ Parse "Global Positioning System Fix Data" sentence """
        fixQuality = self.fixQuality

        # Ignore position update in GGA message as RMC is regular enough
        self.fixQuality = sentence.get_int(5)
        self.altitude = sentence.get_float(8, 0)

        # Call updated method
        if fixQuality != self.fixQuality:
            self._on_fix_update()

    def _parse_GSA(self, sentence):
        """ Parse "GPS DOP and Active Satellites" sentence """
        fixType = self.fixType

        self.fixMode = sentence.get(0)
        self.fixType = sentence.get_int(1, 1)
        pdop = sentence.get_float(14, 0.0)
        hdop = sentence.get_float(15, 0.0)
        vdop = sentence.get_float(16, 0.0)
        self.dop = (pdop, hdop, vdop)

        # Update sats in use
        self.satellitesInUse = sentence.get_list(2, 12)
        for prn, sat in self.satellites.iteritems():
            sat.in_use = prn in self.satellitesInUse

        # Raise events
        if fixType != self.fixType: self._on_fix_update()
        if len(self.satellites): self._on_satellite_status_update()

    def _parse_GSV(self, sentence):
        """ Parse "GPS Satellites in View" sentence """
        totalMsgs = sentence.get_int(0)
        msgNumber = sentence.get_int(1)
        totalSats = sentence.get_int(2)
        if msgNumber < totalMsgs:
            satRange = 4
        else:
            satRange = totalSats - ((msgNumber - 1) * 4)

        # Empty satellite buffer
        if msgNumber == 1:
            self.__satellites = {}

        # Add/Update satellites
        for idx in xrange(satRange):
            sat = sentence.get_satellite(3 + (idx*4))
            sat.in_use = sat.prn in self.satellitesInUse
            #self.__satellites.setdefault(sat.prn, satellite()).update(sat)
            self.__satellites.setdefault(sat.prn, sat)

        # Raise update satellite cache and raise events
        if msgNumber == totalMsgs:
            self.satellites = self.__satellites
            self._on_satellite_status_update()

    def _parse_RMC(self, sentence):
        """ Parse "Recommended Minimum Specific GPS/TRANSIT Data" sentence """
        position = self.position

        self.fixTime = sentence.get_time(0)
        self.position = sentence.get_latlng(2)
        self.speed = sentence.get_float(6, 0.0)
        self.track = sentence.get_float(7, 0.0)
        self.fixDate = sentence.get_date(8)
        self.trackVariation = sentence.get_float(9, 0.0)
        if sentence.get(10) == 'E':
            self.trackVariation *= -1

        # Call updated method
        if self.fixType > 1:
            self._on_transit_update()



if __debug__ and __name__ == '__main__':
    import tcpport
    port = tcpport.TcpPort(port=11000, timeout=0)
    #import serialport
    #port = serialport.SerialPort(port='/dev/ttyUSB0')

    def position_callback(gps):
        print gps.position

    def fix_callback(gps):
        print "Fix Quality:", gps.fixQuality, "Type", gps.fixType

    gpsCallbacks = {
        'fix_update': fix_callback,
        'transit_update': position_callback
    }

    try:
        gps = GPS(port, gpsCallbacks)
        while True:
            gps.parse_data()
    finally:
        port.close()
