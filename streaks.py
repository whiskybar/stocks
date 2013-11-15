import csv
import sys
from collections import namedtuple
import operator


History = namedtuple('History', ['date', 'open', 'high', 'low', 'close', 'volume', 'adj'])

def analyze(records, lookfor):
    hits, misses = 0, 0
    streak = []
    last = None
    for row in records:
        row = History(row[0], *map(float, row[1:]))
        if last is None:
            last = row.close
            continue
        
        if row.high > last:
            streak.append((row.date, last, row.high))
            if len(streak) == lookfor:
                hits += 1
                print streak
        else:
          if len(streak) == lookfor - 1:
              misses += 1
          streak = []
        last = row.close
    return hits, misses


with open(sys.argv[1]) as csvfile:
    records = list(csv.reader(csvfile))[::-1][:-1]
for streak in range(2, 6):
    hits, misses = analyze(records, streak)
    print hits, misses, '%.1f%%' % (float(hits) / (hits + misses) * 100 )
    print
