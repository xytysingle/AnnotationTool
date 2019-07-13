#!/bin/bash

PROC='cigarette'

echo "$PROC" | while read line
do
    pid=`ps -ef | grep 'python' | grep $line | grep -v 'grep' | awk '{print $2}'`
    if [ ! "$pid" = "" ]; then
        kill $pid
    fi
done
