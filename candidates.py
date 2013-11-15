import requests
import datetime
import collections
import csv
import sys
import os
import os.path


History = collections.namedtuple('History', ['open', 'high', 'low', 'close', 'volume', 'adjustment'])

def history(symbol, since, until):
    response = requests.get('http://ichart.finance.yahoo.com/table.csv?s=%s&d=%d&e=%d&f=%d&g=d&a=%d&b=%d&c=%d&ignore=.csv' % (
        symbol,
        until.month - 1,
        until.day,
        until.year,
        since.month - 1,
        since.day,
        since.year,
    ))
    for row in csv.reader(response.text.split('\n')[::-1][1:-1]):
        yield History._make(map(float, row[1:]))

def last(symbol, start, number):
    until = start - datetime.timedelta(days=1)
    if until.weekday() == 6:
        until -= datetime.timedelta(days=2)
    elif until.weekday() == 0:
        until -= datetime.timedelta(days=1)
    since = until - datetime.timedelta(days=number - 1)
    if since.weekday() in [0, 6]:
        since -= datetime.timedelta(days=2)
    return history(symbol, since, until)
    
def recent(symbol):
    response = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=d1ohgpvp&e=.csv' % symbol)
    return History._make(map(float, csv.reader(response.text.split('\n', 1)).next()[1:]))

def qualify(symbol):
    today = datetime.date.today()
    data = dict(zip(['yy', 'y'], last(symbol, today, 2)))
    try:
        data['t'] = recent(symbol)
    except ValueError:
        return False
    return data['yy'].close < data['y'].low and data['y'].close > data['t'].low

def process():
    if len(sys.argv) > 1:
        symbols = sys.argv[1:]
    else:
        symbols = []
        for entry in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')):
            symbols.append(entry.rsplit('.', 1)[0])
    for symbol in symbols:
        symbol = symbol.upper()
        if symbol.strip() and qualify(symbol):
            print symbol

if __name__ == '__main__':
    process()
