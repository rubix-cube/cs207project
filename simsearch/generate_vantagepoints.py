import sys, os
import inspect
import shutil
import argparse
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries') 

import ArrayTimeSeries as ts
import binarytree
import pickle
from util import kernel_corr, stand
import random

def main(arguments):
    try:
        shutil.rmtree('dbs')
    except:
        pass
    os.mkdir('dbs')
    parser = argparse.ArgumentParser(description='Number of vantage points to generate')
    parser.add_argument('--n', help='Number of vantage points', type=int, default=20)
    args = parser.parse_args(arguments)

    n=args.n

    vantage = random.sample(range(1000), n)
    pickle.dump(vantage, open( "ts_data/vantage_points.p", "wb"))
    print('Vantage Points are: ')
    for i in vantage:
        print('TS '+str(i))

    tss = []

    #load the ts
    print('Loading the TS')
    for i in range(1000):
        tss.append(pickle.load(open( "ts_data/ts_{}.p".format(i), "rb")))

    print('Creating the DBS')
    for ct, i in enumerate(vantage):
        print(str(ct+1)+'/'+str(len(vantage))+' Done')
        db = binarytree.connect('dbs/db_'+str(i)+'.dbdb')
        ts_i_stand = stand(tss[i], tss[i].mean(), tss[i].std())
        for j in range(0, 1000):
            if j == i:
                continue
            dist = kernel_corr(ts_i_stand, stand(tss[j], tss[j].mean(), tss[j].std()))
            db.set(-dist, 'ts_'+str(j))
        db.commit()
        db.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))