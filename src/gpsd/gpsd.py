#!/usr/bin/env python
#
# Python GPSD
# Copyright (C) 2008 Tim Savage
#
# Python GPSD is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your option)
# any later version.
#
# Python GPSD is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# python GPSD.  If not, see <http://www.gnu.org/licenses/>.

import dbus
import dbus.service
import gobject
import nmea
import optparse
import sys

from dbus.mainloop.glib import DBusGMainLoop


GPSD_BUS_NAME = 'org.poweredbypenguins.gpsd'
GPS_OBJECT_PATH = '/org/poweredbypenguins/gpsd/GPS%d'
GPS_IFACE_NAME = 'org.poweredbypenguins.gpsd.gps'

class Gps(dbus.service.Object):
    def __init__(self, gps_device, bus, object_path):
        super(Gps, self).__init__(bus, object_path)
        self.gps_device = gps_device
        
    @dbus.service.method(dbus_interface=GPS_IFACE_NAME,
        out_signature='dd')
    def position(self):
        return (0.1, 0.2)

    @dbus.service.signal(dbus_interface=GPS_IFACE_NAME,
        signature='(dd)di')
    def navigate(self, position, track, speed):
        return (position, track, speed)


def create_gps_device(options):
    """ Create instance of a gps device port """
    if options == 'serial':
        from nmea.serialport import SerialPort
        return SerialPort(
            device=options.device,
            baud=options.baud,
            timeout=options.timeout)
    elif options == 'tcp':
        from nmea.tcpport import TcpPort
        return TcpPort(
            host=options.host,
            port=options.port,
            timeout=options.timeout)
    else:
        return None


def get_options():
    """ Setup options structure """
    p = optparse.OptionParser(version='%prog 0.1')
    p.add_option('-t', '--type', default='serial', choices=['serial', 'tcp'],
        help='type of port to use: serial or tcp')
    p.add_option('--timeout', type='int', default=3,
        help='port read timeout (in seconds)')
    p.add_option('--trigger', default='gsv',
        help='message type that triggers position update')
        
    g = optparse.OptionGroup(p, 'Serial Backend')
    g.add_option('--device', default='/dev/gps',
        help='device file of serial port connected to GPS')
    g.add_option('--baud', type='int', default=4800)
    p.add_option_group(g)

    g = optparse.OptionGroup(p, 'TCP Backend')
    g.add_option('--host', default='localhost')
    g.add_option('--port', type='int', default=11000)
    p.add_option_group(g)

    options, arguments = p.parse_args()
    return options


def main():
    options = get_options()

    # Setup main loop
    mainLoop = DBusGMainLoop(set_as_default=True)

    # Attach to bus and register name
    bus = dbus.SessionBus()
    if bus.name_has_owner(GPSD_BUS_NAME):
        print >> sys.stderr, "GPSD name already registered on the BUS"
        return 1
    else:
        bus.request_name(GPSD_BUS_NAME)

    # Create GPS object
    gps0 = Gps(None, bus, GPS_OBJECT_PATH % 0)

    # Start event loop
    loop = gobject.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
