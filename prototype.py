#!/usr/bin/env python3

import re
from collections import Counter

# regular expression
rexp = r'(?P<timestamp>\d{1,2}-\w{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d{3}) client (?P<client>(?:\d{1,3}\.){3}\d{1,3}).+query: (?P<domain>.+) IN (?P<qtype>[A-Z]+) \+.+\({2}(?P<server>(?:\d{1,3}\.){3}\d{1,3})\){2}'

# create counter dictionary
cnt_domains = Counter()

# read file / gather data
f = open('bind9.log', 'r')
matched = 0
failed = 0
for line in f:
    m = re.match(rexp, line)
    if m:
        cnt_domains.update([m.group('domain')])
        matched += 1
    else:
        failed += 1

#    print("""\
#timestamp ...: %s
#client ......: %s
#domain ......: %s
#qtype .......: %s
#dns server ..: %s
#""" % ( m.group('timestamp'),
#        m.group('client'),
#        m.group('domain'),
#        m.group('qtype'),
#        m.group('server'),
#    ))

# Output Results
print('[*] %d lines matched the regular expression' % (matched))
print('[*] %d lines failed to match the regular expression' % (failed), end='\n\n')
print('[*] ============================================')
print('[*] 10 Most Frequently Occurring Domains Queried')
print('[*] ============================================')
for domain, count in cnt_domains.most_common(10):
    print('[*] %30s: %d' % (domain, count))
print('[*] ============================================')

