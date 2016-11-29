import sys, os
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries') 

import argparse
import pickle

import binarytree
import numpy.fft as nfft
import numpy as np
import util

def sanity(ts_stand):
    ds = []
    for i in range(1000):
        v = pickle.load(open( "ts_data/ts_{}.p".format(i), "rb"))
        v_stand = util.stand(v, v.mean(), v.std())
        ds.append(('ts_'+str(i), util.kernel_corr(ts_stand, v_stand)))
    return sorted(ds, key=lambda d: d[1])[-10:]
def eval_closest_vantage(ts_stand, vantage):
    closest_vantage = None
    closest_distance = float("inf")
    for i in vantage:
        v = pickle.load(open( "ts_data/ts_{}.p".format(i), "rb"))
        v_stand = util.stand(v, v.mean(), v.std())
        curr_distance = util.kernel_corr(ts_stand, v_stand)
        if curr_distance < closest_distance:
            closest_vantage = (i, "ts_data/ts_{}.p".format(i))
            closest_distance = curr_distance
    print('Closest Vantage point: ', closest_vantage)
    print('Distance to vintage: ', closest_distance)
    print()
    return closest_vantage, closest_distance

def in_radius_from_vantage(ts_stand, v_str):
    v = pickle.load(open( "ts_data/ts_{}.p".format(v_str), "rb"))
    v_stand = util.stand(v, v.mean(), v.std())
    d = util.kernel_corr(ts_stand, v_stand)
    db = binarytree.connect('dbs/db_{}.dbdb'.format(v_str))
    closest_in_vantage = [x[1] for x in db.get_closer_than(-(1-2*(1-d)))]
    db.close()
    return closest_in_vantage

def return_top(ts_stand, oglist, n):
    if n>1:
        topn = []
        for k in oglist:
            v = pickle.load(open( "ts_data/{}.p".format(k), "rb"))
            v_stand = util.stand(v, v.mean(), v.std())
            curr_distance = util.kernel_corr(ts_stand, v_stand)
            if len(topn)<n:
                topn.append((k, curr_distance))
            else:
                val = [x[1] for x in topn]
                i = val.index(min(val))
                if val[i] > curr_distance:
                    continue
                else:
                    topn[i] = (k, curr_distance)
        topn.sort(key=lambda x: -x[1])
        # return topn
        print('Results: \n')
        for k,v in topn:
            print(k+':', v)
    else:
        m = 0
        best = None
        for k in oglist:
            v = pickle.load(open( "ts_data/{}.p".format(k), "rb"))
            v_stand = util.stand(v, v.mean(), v.std())
            curr_distance = util.kernel_corr(ts_stand, v_stand)
            if m<= curr_distance:
                m = curr_distance
                best = k
        print('Closest: '+ best +', Distance: '+ str(m))



def main(arguments):
    parser = argparse.ArgumentParser(description='Number of timeseries to generate')
    parser.add_argument('ts', help="TimeSeries of interest", type=str)
    parser.add_argument('--n', help='Top N similar', type=int, default=1)
    args = parser.parse_args(arguments)
    ts_name = args.ts
    n = args.n
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
    
    return_top(ts_stand, closest_in_all, n)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))