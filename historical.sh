#!/bin/bash

SYMBOL=${1^^}
wget -q -O $(dirname $0)/data/$SYMBOL.csv 'http://ichart.finance.yahoo.com/table.csv?s='$SYMBOL'&g=d&a=0&b=1&c=2013&ignore=.csv'
python $(dirname $0)/stocks.py $(dirname $0)/data/$SYMBOL.csv

echo
echo -n 'Keep? [Y/n] '
read REPLY
[ "${REPLY^^}" = N ] && rm $(dirname $0)/data/$SYMBOL.csv
