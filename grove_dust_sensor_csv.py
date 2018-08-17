#!/usr/bin/env python

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# USAGE
#
# Connect the dust sensor to Port D2 on the GrovePi. The dust sensor only works on that port
# The dust sensor takes 30 seconds to update the new values.
#
# The first byte is 1 for a new value and 0 for old values.
# The second byte is the concentration in pcs/0.01cf

import time
import grovepi
import atexit
import csv
import math

def getSerial():
    # Extract serial from cpuinfo file
    cpu_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6]=='Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = "ERROR00000000000"

    return cpu_serial


atexit.register(grovepi.dust_sensor_dis)

serial = getSerial()

print("Reading from the dust sensor")
grovepi.dust_sensor_en()
while True:
    # Get the datetime for the filename
    t0 = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())

    # Create the csv file for storing the values
    location = '/home/pi/Documents/sensor_data_' + t0 + '.csv'

    # Get 10 readings
    for i in range(10):
        try:
            [new_val,lowpulseoccupancy] = grovepi.dustSensorRead()
            #if new_val:
            print(lowpulseoccupancy)
            x = lowpulseoccupancy / 1000.0
            print x
            prediction = (x) + (0.11436242 * math.pow(x, 2)) - (1.0391601 * x) + 0.05302481
            print(prediction)
            print("Saving the sensor reading to a CSV file...")
            #tc = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            unix_time = int(time.time())
            with open(location, 'a') as file:
                file.write(serial + ','+ unix_time + ',' + str(lowpulseoccupancy))
                file.write('\n')
                file.close()
                print("Saved")

            time.sleep(10)

        except IOError:
            i = i - 1 # Missed a reading
            print ("Error")
