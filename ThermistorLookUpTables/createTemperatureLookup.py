#!/usr/bin/python
#
# Creates a C code lookup table for doing ADC to temperature conversion
# on a microcontroller
# based on:
# http://hydraraptor.blogspot.com/2007/10/measuring-temperature-easy-way.html

"""Thermistor Value Lookup Table Generator
Generates lookup to temperature values for use in a microcontroller in C format based on:
http://hydraraptor.blogspot.com/2007/10/measuring-temperature-easy-way.html
The main use is for Arduino programs that read data from the circuit board described here:
http://make.rrrf.org/ts-1.0
Usage: python createTemperatureLookup.py [options]
Options:
    -h, --help          show this help
    # is the ohm rating of the thermistor at t0 (eg: 10K = 10000)
    --r0=...            thermistor rating where
    # is the temperature in Celsuis to get r0 (from your datasheet)
    --t0=...            thermistor temp rating where
    --beta=...          thermistor beta rating. see http://reprap.org/bin/view/Main/MeasuringThermistorBeta
    # is the ohm rating of R1 (eg: 10K = 10000)
    --r1=...            R1 rating where
    # is the ohm rating of R2 (eg: 10K = 10000)
    --r2=...            R2 rating where
    --rseries=...       Rseries is the value of the series resistor Used for ADC Protection (eg: 10K = 10000)
    --num-temps=...     the number of temperature points to calculate (default: 20)
    --max-adc=...       the max ADC reading to use.  if you use R1, it limits the top value for the thermistor circuit, and thus the possible range of ADC values
"""

from math import *
import sys
import getopt


class Thermistor:
    "Class to do the thermistor maths"

    def __init__(self, r0, t0, beta, r1, r2, rseries):
        self.r0 = r0                        # stated resistance, e.g. 10K
        self.t0 = t0 + 273.15               # temperature at stated resistance, e.g. 25C
        self.rseries = rseries              #Series resistor added
        self.beta = beta                    # stated beta, e.g. 3500
        self.vadc = 5.0                     # ADC reference
        self.vcc = 5.0                      # supply voltage to potential divider
        self.k = r0 * exp(-beta / self.t0)   # constant part of calculation
        #print self.k

        if r1 > 0:
            self.vs = r1 * self.vcc / (r1 + r2)  # effective bias voltage
            self.rs = r1 * r2 / (r1 + r2)       # effective bias impedance
        elif rseries > 0:
            self.minv = self.vcc * self.rseries / (self.rseries + r2)
            print "minimum voltage is: %s" % (self.minv)
            self.rs = r2
            self.vs = self.vcc
        else:
            self.vs = self.vcc                   # effective bias voltage
            self.rs = r2                         # effective bias impedance

    def temp(self, adc):
        "Convert ADC reading into a temperature in Celcius"
        v = adc * self.vadc / 1024              # convert the 10 bit ADC value to a voltage
        if self.rseries > 0:
            if v >= self.minv:
                returnResistance = True
                # Compute new resistance of the thermistor
                r = (v * (self.rs + self.rseries)) - (self.vs * self.rseries)
                r = r / (self.vs - v)
                #print r
            else:
                returnResistance = False
        else:
            # resistance of thermistor
            r = self.rs * v / (self.vs - v)
        if returnResistance:
            return (self.beta / log(r / self.k)) - 273.15        # temperature
        else:
            return 0

    def setting(self, t):
        "Convert a temperature into a ADC value"
        # resistance of the thermistor
        r = self.r0 * exp(self.beta * (1 / (t + 273.15) - 1 / self.t0))
        # the voltage at the potential divider
        if self.rseries > 0:
            v = self.vs * ((r + self.rseries) / (r + self.rseries + self.rs))
        else:
            v = self.vs * r / (self.rs + r)    
        return round(v / self.vadc * 1024)  # the ADC reading


def main(argv):

    r0 = 10000
    t0 = 25
    beta = 3947
    r1 = 680
    r2 = 1600
    rseries = 0
    num_temps = int(60)
    max_adc = int(1023)

    marlin = False

    try:
        opts, args = getopt.getopt(argv, "h", ["help", "r0=", "t0=", "beta=", "r1=", "r2=", "rseries=", "num-temps=", "max-adc=", "marlin="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--r0":
            r0 = int(arg)
        elif opt == "--t0":
            t0 = int(arg)
        elif opt == "--beta":
            beta = int(arg)
        elif opt == "--r1":
            r1 = int(arg)
        elif opt == "--r2":
            r2 = int(arg)
        elif opt == "--rseries":
            rseries = int(arg)
        elif opt == "--num-temps":
            num_temps = int(arg)
        elif opt == "--max-adc":
            max_adc = int(arg)
        elif opt == "--marlin":
            marlin = True
    increment = int(max_adc / (num_temps - 1))

    t = Thermistor(r0, t0, beta, r1, r2, rseries)

    #adcs = range(1, max_adc, increment)
    adcs = [1, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320]
    first = 1

    print "// Thermistor lookup table for RepRap Temperature Sensor Boards (http://make.rrrf.org/ts)"
    print "// Made with createTemperatureLookup.py (http://svn.reprap.org/trunk/reprap/firmware/Arduino/utilities/createTemperatureLookup.py)"
    print "// ./createTemperatureLookup.py --r0=%s --t0=%s --r1=%s --r2=%s --rseries=%s --beta=%s --num-temps=%s --max-adc=%s --marlin=%s" % (r0, t0, r1, r2, rseries, beta, num_temps, max_adc, marlin)
    print "// r0: %s" % (r0)
    print "// t0: %s" % (t0)
    print "// r1: %s" % (r1)
    print "// r2: %s" % (r2)
    print "// rseries: %s" % (rseries)
    print "// beta: %s" % (beta)
    print "// max adc: %s" % (max_adc)
    print "// marlin: %s" % (marlin)
    print "#define NUMTEMPS %s" % (len(adcs))
    print "short temptable[NUMTEMPS][2] = {"

    counter = 0
    for adc in reversed(adcs):
        counter = counter +1
        if counter == len(adcs):
            # print "   {%s*OVERSAMPLENR, %s}" % (adc, int(t.setting(adc)))
            print "   {%s*OVERSAMPLENR, %s}" % (int(t.setting(adc)), adc)
        else:
            # print "   {%s*OVERSAMPLENR, %s}," % (adc, int(t.setting(adc)))
            print "   {%s*OVERSAMPLENR, %s}," % (int(t.setting(adc)), adc)
    print "};"

def usage():
        print __doc__

if __name__ == "__main__":
    main(sys.argv[1:])
