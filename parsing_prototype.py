#!/usr/bin/env python

import re
import sys

# define and compile
# a regular expression
regexp = re.compile(
    r'(?P<date>\d{1,2}-[A-Z][a-z]{2}-\d{4}) ' +
    '(?P<timestamp>(?:\d{2}:){2}\d{2}\.\d{3}) client ' +
    '(?P<client>(?:\d{1,3}\.){3}\d{1,3}).+view ' +
    '(?P<view>[a-z]+): query: ' +
    '(?P<domain>.+) IN ' +
    '(?P<qtype>[A-Z]+)'
)

# open the file
fd = open(sys.argv[1], 'r')

# for each line in the file
for line in fd:
    # perform regular expression match
    m = regexp.match(line)

    # if we don't match then next line
    if not m:
        continue

    # print the regex matched groups
    print 'date/time: %s %s, client: %s, view: %s, domain: %s, qtype: %s' % (
            m.group('date'),
            m.group('timestamp'),
            m.group('client'),
            m.group('view'),
            m.group('domain'),
            m.group('qtype')
    )

# close the file
fd.close()
