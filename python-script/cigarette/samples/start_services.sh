#!/usr/bin/env bash

export PYTHONPATH=.:$PYTHONPATH

python cigarette.py --gpu 1 | tee -a logs/server.log 2>&1 &

