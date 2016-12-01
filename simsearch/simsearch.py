import sys, os
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 

import argparse
import pickle

import timeseries.ArrayTimeSeries as ts
import binarytree
import numpy.fft as nfft
import numpy as np
import util

'''
This script is the main script of this directory. It is used to find the most similar timeseries in a database to a given timeseries parsed as compulsory argument
in the command line. The command line also takes the number of timeseries desired, the default being the closest. 

The method to find the n closest is described below.

*** CLOSEST ***
-Evaluate the closest vantage point i.e. the vantage point such that 2*(1-kernel_corr(ts, vp)) is closest to 0
-Search all timeseries with distance smaller than twice the distance between the ts and the vp
-Evaluate the distances from the ts to all these timeseries and return the min distances.

*** N Closest ***
-Evaluate the distances to all vantage points
-For each vp, select points in the circle of radius 2*d(ts, vp)
-Evaluate the distances form the ts to the compound list of all timeseries and return the top n

**** NB *****
Some of the methods below have a test argument to them. This argument should not be taken into consideration, it is only to point
to the testing databases. 

Also the return_topn method has a ret argument currently set to False. This means that it will print the top n results and not return them.
One could change this to True and have the results being saved as a list, which is pickled in the folder.

Usage:
------

!python simsearch.py ts_data\ts_0 --n 10
!python simsearch.py ts_interesting --save True --f Results/

'''


def sanity(ts_stand, n):
    "This function is a sanity check used in the testing file: brute force n closest"
    ds = []
    for i in range(1000):
        v = pickle.load(open( "../ts_data/ts_{}.p".format(i), "rb"))
        v_stand = util.stand(v, v.mean(), v.std())
        ds.append(('ts_data/ts_'+str(i)+'.p', 2*(1-util.kernel_corr(ts_stand, v_stand))))
    return sorted(ds, key=lambda d: d[1])[:n]
def eval_closest_vantage(ts_stand, vantage, test=False):
    '''
    Return the index of the closest vantage point
    Args:
    -----
    - ts_stand: standardised ArrayTimeSeries
    - vantage point: list of indices of vantage points
    '''
    closest_vantage = None
    closest_distance = float("inf")
    for i in vantage:
        if test:
            v = pickle.load(open( "../ts_data/ts_{}.p".format(i), "rb"))
        else:
            v = pickle.load(open( "ts_data/ts_{}.p".format(i), "rb"))
        v_stand = util.stand(v, v.mean(), v.std())
        curr_distance = 2*(1-util.kernel_corr(ts_stand, v_stand))
        if curr_distance < closest_distance:
            if test:
                closest_vantage = (i, "../ts_data/ts_{}.p".format(i))
            else:
                closest_vantage = (i, "ts_data/ts_{}.p".format(i))
            closest_distance = curr_distance
    return closest_vantage, closest_distance

def in_radius_from_vantage(ts_stand, v_str, test=False):
    '''
    Return the points in the circle of radius 2*k_corr(ts_stand, vantage_stand)
    Args:
    -----
    - ts_stand: standardised ArrayTimeSeries
    - v_str: index of the vantage point as a string
    '''
    if test:
        v = pickle.load(open( "../ts_data/ts_{}.p".format(v_str), "rb"))
    else:
        v = pickle.load(open( "ts_data/ts_{}.p".format(v_str), "rb"))
    v_stand = util.stand(v, v.mean(), v.std())
    d = 2*(1-util.kernel_corr(ts_stand, v_stand))
    if not test:
        db = binarytree.connect('dbs/db_{}.dbdb'.format(v_str))
    else:
        db = binarytree.connect('../dbs/db_{}.dbdb'.format(v_str))
    closest_in_vantage = [x[1] for x in db.get_closer_than(2*d)]
    db.close()
    return closest_in_vantage

def return_top(ts_stand, oglist, n, ret=False, file='', test=False):
    '''
    Prints or saves the n closest timeseries to ts_stand from a list of timeseries names (i.e. as string)
    '''
    if n>1:
        topn = []
        for k in oglist:
            if test:
                v = pickle.load(open( "../ts_data/{}.p".format(k), "rb"))
            else:
                v = pickle.load(open( "ts_data/{}.p".format(k), "rb"))
            v_stand = util.stand(v, v.mean(), v.std())
            curr_distance = 2*(1-util.kernel_corr(ts_stand, v_stand))
            if len(topn)<n:
                topn.append((k, curr_distance))
            else:
                val = [x[1] for x in topn]
                i = val.index(max(val))
                if val[i] < curr_distance:
                    continue
                else:
                    topn[i] = (k, curr_distance)
        topn.sort(key=lambda x: x[1])
        # return topn
        if not ret:
            print('Results: \n')
            for k,v in topn:
                print(k+':', v)
        else:
            pickle.dump(topn, open(file, "wb"))
    else:
        m = float("inf")
        best = None
        for k in oglist:
            if test:
                v = pickle.load(open( "../ts_data/{}.p".format(k), "rb"))
            else:
                v = pickle.load(open( "ts_data/{}.p".format(k), "rb"))
            v_stand = util.stand(v, v.mean(), v.std())
            curr_distance = 2*(1-util.kernel_corr(ts_stand, v_stand))
            if m> curr_distance:
                m = curr_distance
                best = k
        if not ret:
            print('Closest: '+ best +', Distance: '+ str(m))
        else:
            pickle.dump([m, best], open(file, "wb"))



def main(arguments):
    parser = argparse.ArgumentParser(description='Number of timeseries to generate')
    parser.add_argument('ts', help="TimeSeries of interest", type=str)
    parser.add_argument('--n', help='Top N similar', type=int, default=1)
    parser.add_argument('--save', help='Save Results', type=bool, default=False)
    parser.add_argument('--f', help='Path to results folder', type=str, default='results.p')
    args = parser.parse_args(arguments)
    ts_name = args.ts
    n = args.n
    f = args.f
    save = args.save
    ts = pickle.load(open(ts_name+".p", "rb" ))
    ts_stand = util.stand(ts, ts.mean(), ts.std())
    vantage = pickle.load(open( "ts_data/vantage_points.p", "rb"))
    if n == 1:
        closest_vantage, closest_distance  = eval_closest_vantage(ts_stand, vantage)
        closest_in_all = in_radius_from_vantage(ts_stand, closest_vantage[0])
    else:
        closest_in_all = []
        for v in vantage:
            closest_in_all += in_radius_from_vantage(ts_stand, v)
        closest_in_all = list(set(closest_in_all))
    
    return_top(ts_stand, closest_in_all, n, save, f)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))