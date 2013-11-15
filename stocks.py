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
    enter = None
    for row in records:
        row = History(row[0], *map(float, row[1:]))
        if not row.date.startswith('2013'):
            continue
        if last is None:
            last = row.close
            continue
        
        extreme = getattr(row, direction)
        if enter:
            diff = (extreme - enter) * sign
            if profit:
                if diff >= profit:
                    diff = profit
                else:
                    diff = (row.close - enter) * sign
        if compare(extreme, last):
            if not enter and not streak:
               enter = row.close
            streak.append((row.date, last, extreme))
            if len(streak) == lookfor:
                details.append('+ %s %.1f' % (streak[0][0], diff))
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
                enter = None
        else:
            if enter and len(streak) < lookfor:
                details.append('  %s %.1f' % (streak[0][0], diff))
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
                enter = None
            streak = []
        last = row.close
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
        avggain, avgloss = sorted(gains)[hits/2] if hits else 0, sorted(losses)[misses/2] if losses else 0
#        avggain, avgloss = gain / hits if hits else 0, loss / misses if misses else 0
        averages[direction][streak] = avggain
        if hits + misses == 0:
            print 0, 0, '0.0%'
        else:
            print '%s %dx %d %d %.1f%% %.1f (Ø%.1f) %.1f (Ø%.1f) = %.1f' % (
                direction, 
                streak, 
                hits, 
                misses, 
                float(hits) / (hits + misses) * 100, 
                gain, 
                avggain, 
                loss, 
                avgloss,
                gain + loss,
            )
print

for compare, direction in [(operator.gt, 'high'), (operator.lt, 'low')]:
    for streak in range(2, 6):
        profit = averages[direction][streak] * stop
        gains, losses, details = analyze(records, streak, profit, compare, direction)
        hits, misses = len(gains), len(losses)
        gain, loss = sum(gains or [0]), sum(losses or [0])
#        print '\n', '\n'.join(details)
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


