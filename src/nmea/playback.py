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

import socket
import sys
import time
import optparse


def workLoop(s, f, plain):
    while True:
        # Wait for connections
        print 'Waiting for connection...'
        s.listen(1)

        conn, addr = s.accept()
        print 'Connected to', addr

        # Stream data to client
        while True:
            data = f.readline()
            if not data:
                f.seek(0)
            else:
                if not plain:
                    data = data.split(':', 1)
                    time.sleep(float(data[0]))
                try:
                    conn.send(data[1])
                except socket.error:
                    break;


def get_options():
	p = optparse.OptionParser()
	p.add_option('--host', default='localhost',
		help='host to bind socket')
	p.add_option('-p', '--port', type='int', default=11000,
		help='port read timeout (in seconds)')
	p.add_option('--plain', action='store_true', default=False,
		help="file does not contain time deltas")
	p.add_option('-f', '--file', default='dump.gps',
		help='file to use for input')

	options, arguments = p.parse_args()
	return options


def main():
    options = get_options()

    # Open record file
    try: f = open(options.file, 'r')
    except IOError: print >> sys.stderr, "File not found: ", options.file
    else:
        print 'GPS record opened'

        # Open Port
        try:
            # Create listening socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((options.host, options.port))
            print 'Socket bound to %s:%d' % (options.host, options.port)
        except socket.error, sex:
            print sys.stderr, "Unable to open socket:", sex
            return -1

        # Start work loop
        try: workLoop(s, f, options.plain)
        except KeyboardInterrupt: pass
        except: print >> sys.stderr, "Unknown error occured"

        # Clean up
        s.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
