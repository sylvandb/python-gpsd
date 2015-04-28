## Name ##
nmea\_record - a tool to record gps output for later playback

## Synopsis ##
`nmea_record [options]`

## Description ##
Part of the NMEA Toolkit

The recording tool writes the output of your gps to stdout and applies a time-stamp. The output can be redirected to a file so that the GPS output can be simulated at a later point or used for testing purposes.

The output is also useful if a bug is found in the gps parsing code.

## Command Line Options ##
| --version | show program's version number and exit |
|:----------|:---------------------------------------|
| -h, --help | show this help message and exit |
| -x, --plain | don't decorate output with a time delta |
| -t TIMEOUT, --timeout=TIMEOUT | port read timeout (in seconds) |

### Serial Backend ###
| --device=DEVICE | device file of serial port connected to GPS |
|:----------------|:--------------------------------------------|
| --baud=BAUD |  |

## Author ##
Tim Savage

## Licensing ##
The NMEA Toolkit is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or at your option any later version.