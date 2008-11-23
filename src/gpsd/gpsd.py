#!/usr/bin/env python
import dbus
import dbus.service
import gobject
import nmea
import optparse
import sys


class Gpsd(dbus.service.Object):
	def __init__(self, object_path):
		super(Gps, self).__init__(self, dbus.SessionBus(), path)

	@dbus.service.method(dbus_interface='com.poweredbypenguins.gpsd',
		out_signature='(dd)')
	def position(self):
		return (0.1, 0.2)

options = None


def get_options():
	p = optparse.OptionParser(version='%prog 0.1')
	p.add_option('-t', '--type', default='serial', choices=['serial', 'tcp'],
		help='type of port to use: serial or tcp')
	p.add_option('--timeout', type='int', default=3,
		help='port read timeout (in seconds)')

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

	# Set the dbus loop as the default
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


if __name__ == '__main__':
    sys.exit(main())
