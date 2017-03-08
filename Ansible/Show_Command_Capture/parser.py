#!/usr/bin/env python

from __future__ import print_function
import re

serial_number = re.compile('Serial Number')

with open('/tmp/a10_output.txt', 'r') as f:
    for line in f.readlines():
        line = eval(line.strip())
        for line in line["Result"].split("\n"):
            if re.search(serial_number, line): 
                print(line.split(":")[1].strip())


