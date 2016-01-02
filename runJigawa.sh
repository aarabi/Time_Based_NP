#!/bin/sh
#run the network planner for varying demand cases
python timeMetric.py networks-existing/jigawa/demographics networks-existing/jigawa/ networks-existing/jigawa/highcost 140 150
python timeMetric.py networks-existing/jigawa/demographics networks-existing/jigawa/ networks-existing/jigawa/lowcost 30 40

