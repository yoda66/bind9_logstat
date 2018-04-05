#!/usr/bin/env python

import re
import collections
import argparse


class logstats():

    def __init__(self, filename, qtype=[], exclude=[],
                 client=None, domain=None, topn=5, debug=False):

        self.filename = filename
        self.exclude = exclude
        self.qtype = qtype
        self.client = client
        self.domain = domain
        self.topn = topn
        self.debug = debug
        self.cnt_client = collections.Counter()
        self.cnt_domain = collections.Counter()
        self.cnt_qtype = collections.Counter()
        self.re = re.compile(
            r'(?P<timestamp>\d{1,2}-\w{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d{3}) client ' +
            '(?P<client>(?:\d{1,3}\.){3}\d{1,3}).+query: ' +
            '(?P<domain>.+) IN (?P<qtype>[A-Z]+) \+.+\({2}' +
            '(?P<server>(?:\d{1,3}\.){3}\d{1,3})\){2}'
        )

    def run(self):
        fd = open(self.filename, 'r')
        for line in fd:
            m = self.re.match(line)
            if not m:
                continue
            if self.exclude and m.group('qtype') in self.exclude:
                continue
            if self.qtype and m.group('qtype') not in self.qtype:
                continue
            if self.client and m.group('client') not in self.client:
                continue
            if self.domain and m.group('domain') not in self.domain:
                continue

            self.cnt_client.update([m.group('client')])
            self.cnt_domain.update([m.group('domain')])
            self.cnt_qtype.update([m.group('qtype')])

            if self.debug:
                print 'client: %s, domain: %s, qtype: %s' % (
                    m.group('client'),
                    m.group('domain'),
                    m.group('qtype')
                )

        fd.close()
        self.print_summary()

    def print_summary(self):
        if not self.client:
            self.print_counts(self.cnt_client, 'clients')
        if not self.domain:
            self.print_counts(self.cnt_domain, 'domains')
        if not self.qtype:
            self.print_counts(self.cnt_qtype, 'query types')

    def print_counts(self, cdict, title):
        print 60 * '-'
        print ' << Top #%2d %s >>' % (self.topn, title)
        print 60 * '-'
        for i, t in enumerate(cdict.most_common(self.topn)):
            if 'domains' in title:
                print '%2d) %40s: %8d' % (i + 1, t[0][:40], t[1])
            elif 'clients' in title:
                print '%2d) %15s: %8d' % (i + 1, t[0], t[1])
            else:
                print '%2d) %6s: %8d' % (i + 1, t[0], t[1])
        print 60 * '-'
        print '\r\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='bind9 log filename')
    parser.add_argument(
        '--exclude', nargs='*',
        help='query types to exclude'
    )
    parser.add_argument(
        '--qtype', nargs='*', default=[],
        help='query types to include'
    )
    parser.add_argument(
        '--client',
        help='specify client IP to filter by'
    )
    parser.add_argument(
        '--domain',
        help='specify domain to filter by'
    )
    parser.add_argument(
        '--topn', type=int,
        default=5, help='print top N stats'
    )
    parser.add_argument(
        '--debug', action='store_true',
        default=False,
        help='enable debugging'
    )
    args = parser.parse_args()

    l = logstats(
        args.filename,
        qtype=args.qtype,
        exclude=args.exclude,
        client=args.client,
        domain=args.domain,
        topn=args.topn,
        debug=args.debug
    )
    l.run()
