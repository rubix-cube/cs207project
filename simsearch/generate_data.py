import sys, os
import inspect
import shutil
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])

import numpy as np
import timeseries.ArrayTimeSeries as ts
import util

import pickle
import argparse

'''
Script used to generate n timeseries using tsmaker, where n is a mandatory argument parsed in the command line.

Usage:
------

!python generate_data.py 1000
!python generate_data.py 2000
!python generate_data.py 500
'''

def main(arguments):
    # We first empty the ts_data folder or create it if it is the first time called
    try:
        shutil.rmtree('ts_data')
    except:
        pass
    os.mkdir('ts_data')

    #Parse the number of timeseries
    parser = argparse.ArgumentParser(description='Number of timeseries to generate')
    parser.add_argument('n', help="Number of timeseries", type=int)
    args = parser.parse_args(arguments)
    n = args.n

    #Generate data:
    for i in range(n):
        t = util.tsmaker(0.5, 0.15, 0.9)
        pickle.dump(t, open( "ts_data/ts_{}.p".format(i), "wb" ))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))