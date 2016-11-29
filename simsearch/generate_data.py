import sys, os
import inspect
import shutil
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries')

import numpy as np
import ArrayTimeSeries as ts
import util

import pickle
import argparse

def main(arguments):
    try:
        shutil.rmtree('ts_data')
    except:
        pass
    os.mkdir('ts_data')
    parser = argparse.ArgumentParser(description='Number of timeseries to generate')
    parser.add_argument('n', help="Number of timeseries", type=int)
    args = parser.parse_args(arguments)
    n = args.n

    for i in range(n):
        t = util.tsmaker(0.5, 0.15, 0.9)
        pickle.dump(t, open( "ts_data/ts_{}.p".format(i), "wb" ))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))