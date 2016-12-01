import sys, os
import inspect
import shutil
import argparse
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 

import timeseries.ArrayTimeSeries as ts
import binarytree
import pickle
from util import kernel_corr, stand
import random

'''
Script used to generate vantage points to facilitate the simsearch and their corresponding indices. The indices contain the negative of the timeseries with each vantage points.

This script takes two optional arguments corresponding to the number of vantage points wanted, with default value 20 and the number of timeseries in the dabases, default 1000. 

NB: for the search to be efficient, one cannot ask more similar point than the number of vantage points

Usage:
------

!python generate_vantagepoints.py 
!python generate_vantagepoints.py --n 50 --nts 500
'''
def main(arguments):
    #Clean the databases or create the directory
    try:
        shutil.rmtree('dbs')
    except:
        pass
    os.mkdir('dbs')

    #Parse the number of vantage points wanted
    parser = argparse.ArgumentParser(description='Number of vantage points to generate')
    parser.add_argument('--n', help='Number of vantage points', type=int, default=20)
    parser.add_argument('--nts', help='Number of vantage points', type=int, default=1000)
    args = parser.parse_args(arguments)
    n=args.n
    nts=args.nts

    #sample the vantage points without replacement
    vantage = random.sample(range(nts), n)
    pickle.dump(vantage, open( "ts_data/vantage_points.p", "wb"))
    print('Vantage Points are: ')
    for i in vantage:
        print('TS '+str(i))

    tss = []

    #load the ts
    print('Loading the TS')
    for i in range(nts):
        tss.append(pickle.load(open( "ts_data/ts_{}.p".format(i), "rb")))

    #Store the negative of the k_corr of each vantage points to the eveyr other timeseries in the DB
    print('Creating the DBS')
    for ct, i in enumerate(vantage):
        print(str(ct+1)+'/'+str(len(vantage))+' Done')
        db = binarytree.connect('dbs/db_'+str(i)+'.dbdb')
        ts_i_stand = stand(tss[i], tss[i].mean(), tss[i].std())
        for j in range(0, nts):
            if j == i:
                continue
            kc = kernel_corr(ts_i_stand, stand(tss[j], tss[j].mean(), tss[j].std()))
            db.set(2*(1-kc), 'ts_'+str(j))
        db.commit()
        db.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))