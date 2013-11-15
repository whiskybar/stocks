import csv
import sys
from collections import namedtuple
import operator


History = namedtuple('History', ['open', 'high', 'low', 'close', 'volume', 'adj'])

def analyze(records, lookfor):
    hits, misses = 0, 0
    streak = 0
    last = None
    for row in records:
        row = History._make(map(float, row[1:]))
        if last is None:
            last = row.close
            continue
        
        if row.high > last:
            streak += 1
            if streak == lookfor:
                hits += 1
        else:
          if streak == lookfor - 1:
              misses += 1
          streak = 0
        last = row.close
    return hits, misses


with open(sys.argv[1]) as csvfile:
    records = list(csv.reader(csvfile))[::-1][:-1]
for streak in range(2, 6):
    hits, misses = analyze(records, streak)
    print hits, misses, '%.1f%%' % (float(hits) / (hits + misses) * 100 )
