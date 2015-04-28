# Introduction #

The NMEA protocol for GPS's is relatively loose in many areas regarding accuracy of precision of values in a NMEA Sentence. Because of this various GPS receivers have variations in their output. If you are receiving ParseError exceptions it is most likely due to your receiver outputting sentences that are different to that of the receiver I am using for development (or those being used by others testing).

# Details #

It would be greatly appreciated that if when testing your receiver you receive ParseError exceptions (or you can trace ValueError exceptions that are occurring during the parsing phase) with the use of the supplied record tool, record sample output from your receiver, submit a bug report and attach the recorded output. Note that ParseError exceptions may only occur once the GPS has actually got a fix.