import sys, os
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries') 

import argparse
import pickle

import binarytree
import numpy.fft as nfft
import numpy as np
import util

def main(arguments):
    parser = argparse.ArgumentParser(description='Number of timeseries to generate')
    parser.add_argument('ts', help="TimeSeries of interest", type=str)
    args = parser.parse_args(arguments)
    ts_name = args.ts
    print(ts_name)

    print('Loading the timeseries of interest...\n')
    ts = pickle.load(open(ts_name+".p", "rb" ))
    ts_stand = util.stand(ts, ts.mean(), ts.std())

    print('Loading the vantage points...\n')
    vantage = pickle.load(open( "ts_data/vantage_points.p", "rb"))

    print('Evaluating distances to the vantage points...')
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
    print('Loading the corresponding database index...\n')
    db = binarytree.connect('dbs/db_{}.dbdb'.format(closest_vantage[0]))

    print('Evaluating the vantage point\'s neighborhood...\n')
    closest_in_vantage = db.get_closer_than(-(1-2*(1-closest_distance)))

    print('Calculating 10 closest timeseries...\n')
    top_ten = []
    for d in closest_in_vantage:
        k = db.get(d)
        v = pickle.load(open( "ts_data/{}.p".format(k), "rb"))
        v_stand = util.stand(v, v.mean(), v.std())
        curr_distance = util.kernel_corr(ts_stand, v_stand)
        if len(top_ten)<10:
            top_ten.append((k, curr_distance))
        else:
            val = [x[1] for x in top_ten]
            i = val.index(min(val))
            if val[i] > curr_distance:
                continue
            else:
                top_ten[i] = (k, curr_distance)
    top_ten.sort(key=lambda x: -x[1])
    # return top_ten
    print('Results: \n')
    for k,v in top_ten:
        print(k+':', v)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))