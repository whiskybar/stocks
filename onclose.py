# -*- coding: utf-8 -*-

import csv
import sys
from collections import namedtuple
import operator


History = namedtuple('History', ['date', 'open', 'high', 'low', 'close', 'volume', 'adj'])

def analyze(records, lookfor, compare, direction):
    gains, losses = [], []
    streak = []
    last = None
    for row in records:
        row = History(row[0], *map(float, row[1:]))
        if last is None:
            last = row.close
            continue
        
        extreme = getattr(row, direction)
        diff = row.close - last
        if compare(extreme, last):
            streak.append((row.date, last, extreme))
            if len(streak) == lookfor:
                print '.', streak[0][0], [c for _, c, _ in streak], row.close, diff
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
        else:
            if len(streak) == lookfor - 1:
                print ' ', streak[0][0], [c for _, c, _ in streak], row.close, diff
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
            streak = []
        last = row.close
    return gains, losses


with open(sys.argv[1]) as csvfile:
    records = list(csv.reader(csvfile))[::-1][:-1]
for compare, direction in [(operator.gt, 'high'), (operator.lt, 'low')]:
    for streak in range(2, 6):
        gains, losses = analyze(records, streak, compare, direction)
        hits, misses = len(gains), len(losses)
        gain, loss = sum(gains or [0]), sum(losses or [0])
        if hits + misses == 0:
            print 0, 0, '0.0%'
        else:
            print hits, misses, '%.1f%%' % (float(hits) / (hits + misses) * 100 ), '%.1f' % gain, '(Ø%.1f)' % sorted(gains)[hits/2], '%.1f' % loss, '(Ø%.1f)' % sorted(losses)[misses/2]
        print
