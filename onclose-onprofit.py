# -*- coding: utf-8 -*-

import csv
import sys
from collections import namedtuple, defaultdict
import operator


History = namedtuple('History', ['date', 'open', 'high', 'low', 'close', 'volume', 'adj'])

def analyze(records, lookfor, profit, compare, direction):
    gains, losses = [], []
    streak = []
    last = None
    details = []
    sign = {'high': 1, 'low': -1}[direction]
    for row in records:
        row = History(row[0], *map(float, row[1:]))
        if last is None:
            last = row.close
            last_extreme = getattr(row, direction)
            continue
        
        extreme = getattr(row, direction)
        diff = (extreme - last) * sign
        if profit:
            if diff >= profit:
                diff = profit
            else:
                diff = (row.close - last) * sign
        if compare(extreme, last):
            streak.append((row.date, last, extreme))
            if len(streak) == lookfor:
                details.append('+ %s %.1f' % (streak[0][0], diff))
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
        else:
            if len(streak) == lookfor - 1:
                details.append('  %s %.1f' % (streak[0][0], diff))
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
            streak = []
        last = row.close
        last_extreme = extreme
    return gains, losses, details


with open(sys.argv[1]) as csvfile:
    records = list(csv.reader(csvfile))[::-1][:-1]
stop = len(sys.argv) > 2 and float(sys.argv[2]) or 1

averages = defaultdict(dict)
for compare, direction in [(operator.gt, 'high'), (operator.lt, 'low')]:
    for streak in range(2, 6):
        gains, losses, details = analyze(records, streak, None, compare, direction)
        hits, misses = len(gains), len(losses)
        gain, loss = sum(gains or [0]), sum(losses or [0])
        avggain, avgloss = sorted(gains)[hits/2], sorted(losses)[misses/2]
#        avggain, avgloss = gain / hits if hits else 0, loss / misses if misses else 0
        averages[direction][streak] = avggain
        if hits + misses == 0:
            print 0, 0, '0.0%'
        else:
            print direction, streak, hits, misses, '%.1f%%' % (float(hits) / (hits + misses) * 100 ), '%.1f' % gain, '(Ø%.1f)' % avggain, '%.1f' % loss, '(Ø%.1f)' % avgloss
print

for compare, direction in [(operator.gt, 'high'), (operator.lt, 'low')]:
    for streak in range(2, 6):
        profit = averages[direction][streak] * stop
        gains, losses, details = analyze(records, streak, profit, compare, direction)
        hits, misses = len(gains), len(losses)
        gain, loss = sum(gains or [0]), sum(losses or [0])
        if hits + misses == 0:
            print 0, 0, '0.0%'
        else:
            print '%s %dx at %.1f %d %d %.1f%% %.1f (Ø%.1f) %.1f (Ø%.1f) = %.1f (%d trans)' % (
                direction,
                streak,
                profit, 
                hits, 
                misses,
                float(hits) / (hits + misses) * 100,
                gain,
                avggain,
                loss,
                avgloss,
                gain + loss,
                hits + misses,
            )


