# -*- coding: utf-8 -*-
import unittest

from __types import *


class latitudeTestCase(unittest.TestCase):
    def testEmpty(self):
        self.failUnlessEqual(latitude(), 0.0)

    def testOutOfRange(self):
        self.failUnlessRaises(ValueError, latitude, 91.0)
        self.failUnlessRaises(ValueError, latitude, -91.0)

    def testInvalidType(self):
        self.failUnlessRaises(ValueError, latitude, 91)
        self.failUnlessRaises(ValueError, latitude, "91")
        
    def testStrPositive(self):      
        l = latitude(27 + 27.9487 / 60)
        self.failUnlessEqual(str(l), "27°27'56.922000\"N")

    def testStrNegative(self):      
        l = latitude(-(27 + 27.9487 / 60))
        self.failUnlessEqual(str(l), "27°27'56.922000\"S")


class longitudeTestCase(unittest.TestCase):
    def testEmpty(self):
        self.failUnlessEqual(longitude(), 0.0)

    def testOutOfRange(self):
        self.failUnlessRaises(ValueError, longitude, 191.0)
        self.failUnlessRaises(ValueError, longitude, -191.0)

    def testInvalidType(self):
        self.failUnlessRaises(ValueError, longitude, 91)
        self.failUnlessRaises(ValueError, longitude, "91")
        
    def testStrPositive(self):      
        l = longitude(153 + 05.3408 / 60)
        self.failUnlessEqual(str(l), "153°05'20.448000\"E")

    def testStrNegative(self):      
        l = longitude(-(153 + 05.3408 / 60))
        self.failUnlessEqual(str(l), "153°05'20.448000\"W")


class velocityTestCase(unittest.TestCase):
    def setUp(self):
        self.v = velocity(8.5)

    def testKnots(self):
        self.failUnlessEqual(self.v, 8.5)
        self.failUnlessEqual(self.v.knots(), 8.5)

    def testKmph(self):
        self.failUnlessEqual(self.v.kmph(), 15.742)
        self.failUnlessEqual(self.v.kilometers_per_hour(), 15.742)
        
    def testMps(self):
        self.failUnlessEqual(self.v.meters_per_second(), 4.372777774)

    def testMph(self):
        self.failUnlessEqual(self.v.mph(), 9.781625325)
        self.failUnlessEqual(self.v.miles_per_hour(), 9.781625325)

    
unittest.main()
