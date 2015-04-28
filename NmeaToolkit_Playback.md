## Name ##
nmea\_playback - a tool to record gps output for later playback

## Synopsis ##
`nmea_playback [options]`

## Description ##
Part of the NMEA Toolkit

The playback tool binds to a socket an waits for a connection from a GPS device (using the TcpPort), once connected the tool will begin to replay the recorded output from the GPS device using the time deltas to _simulate_ the original gps output.

## Command Line Options ##
| --version | show program's version number and exit |
|:----------|:---------------------------------------|
| -h, --help | show this help message and exit |
| -a HOST, --host=HOST | host to bind socket |
| -p PORT, --port=PORT | port to bind socket |
| -f FILE, --file=FILE | file to use for input |
| -x, --plain | file does not contain time deltas |
| -d, --delay | delay between plain messages |

## Author ##
Tim Savage

## Licensing ##
The NMEA Toolkit is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or at your option any later version.