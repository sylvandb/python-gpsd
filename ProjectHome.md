A Python based GPS Daemon and NMEA toolkit.

The NMEA toolkit can be used as a standalone library for accessing an NMEA device, it is currently readonly and does not support two way communication with a NMEA device. The current implementation only handles nmea sentences that relate to GPS.

The daemon itself uses dbus for publishing information and allowing multiple applications access to GPS data.

This is a component of a larger [Car PC](http://carpc.poweredbypenguins.org/) project.