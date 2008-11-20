#!/usr/bin/env python
#
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

__version__ = (0, 10)
__author__ = 'tim@poweredbypenguins.org (Tim Savage)'

import select
import sys
import time
import optparse

import serialport


def workLoop(ser, plain):
    last = time.time()

    while True:
        r, w, x = select.select([ser], [], [ser])
        if len(x) > 0: return
        if len(r) > 0:
            sentences = ser.read_buffered(30)
            for sentence in sentences:
                if plain:
                    print "%s\r\n" % sentence,
                else:
                    now = time.time()
                    delta = now - last
                    last = now
                    print "%f:%s\r\n" % (delta, sentence),


def get_options():
	p = optparse.OptionParser()
	#p.add_option('-t', '--type', default='serial', choices=['serial', 'tcp'],
	#	help='type of port backend to use: serial or tcp')
	p.add_option('-p','--plain', action='store_true', default=False,
		help="Don't decorate output with a time delta")
	p.add_option('--timeout', type='int', default=10,
		help='port read timeout (in seconds)')

	g = optparse.OptionGroup(p, 'Serial Backend')
	g.add_option('--device', default='/dev/gps',
		help='device file of serial port connected to GPS')
	g.add_option('--baud', type='int', default=4800)
	p.add_option_group(g)

	#g = optparse.OptionGroup(p, 'TCP Backend')
	#g.add_option('--address', default='localhost')
	#g.add_option('--port', type='int', default=11000)
	#p.add_option_group(g)

	options, arguments = p.parse_args()
	return options


def main():
    options = get_options()

    # Open Port
    try:
        ser = serialport.SerialPort(
            device=options.device,
            baud=options.baud,
            timeout=options.timeout) # Select handles this
    except serialport.PortError:
        print >> sys.stderr, "ERR: Unable to open device:", options.device
        return -1

    # Start workloop
    try: workLoop(ser, options.plain)
    except KeyboardInterrupt: pass
    except: print >> sys.stderr, "ERR: Unknown error"

    # Clean up
    ser.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
