import sys, os
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries')

import numpy.fft as nfft
import numpy as np
import ArrayTimeSeries as ts
from scipy.stats import norm

import pickle
import argparse

def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.001)
    v = norm.pdf(t, m, s) + j*np.random.randn(1000)
    return ts.ArrayTimeSeries(t, v)

def main(arguments):
    parser = argparse.ArgumentParser(description='Number of timeseries to generate')
    parser.add_argument('n', help="Number of timeseries", type=int)
    args = parser.parse_args(arguments)
    n = args.n

    for i in range(n):
        t = tsmaker(norm.rvs(0, 15), 5., 0.01)
        pickle.dump(t, open( "ts_data/ts_{}.p".format(i), "wb" ))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))