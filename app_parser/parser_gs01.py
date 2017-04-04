#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
import struct

def hexstr_unixtime_to_iso8601(src):
    return time.strftime("%Y-%m-%dT%H:%M:%S+0000",
        time.gmtime(int(src, 16)))

def hexstr_ieee754_to_float(src):
    v = struct.pack(">l", int(src, 16))
    return struct.unpack(">f", v)[0]

'''
payload: application data in hex string.
Globalsat sensor message format:
    byte: description
    1: device_type
    1: (7-6) GPS Fix Status (5-0) Report Type
    1: Battery Capacity
    4: latitude (IEEE 754)
    4: longitude (IEEE 754)
'''
def parse(payload):

    if len(payload) != 22:
        print("ERROR: the payload length is not 22.")
        return {}

    return {
        "device_type": "%d" % int(payload[0:2], 16),
        "gps_fix_status": "%s" % bin(int(payload[2:4], 16))[2:4],
        "report_type": "%d" % int(bin(int(payload[2:4], 16))[4:], 2),
        "battery_capacity": "%d" % int(payload[4:6], 16),
        "latitude": "%.6f" % (float(int(payload[6:14], 16)) * 0.000001),
        "longitude": "%.6f" % (float(int(payload[14:22], 16)) * 0.000001)
        }

'''
test code
'''
if __name__ == '__main__' :
    v = parse("008263022034b60854231c");
    print("DEBUG: ")
    print("  device_type = %s" % v["device_type"])
    print("  gps_fix_status = %s" % v["gps_fix_status"])
    print("  report_type = %s" % v["report_type"])
    print("  battery_capacity = %s %%" % v["battery_capacity"])
    print("  latitude = %s" % v["latitude"])
    print("  longitude = %s" % v["longitude"])
