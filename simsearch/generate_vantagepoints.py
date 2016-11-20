import sys, os
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries') 

import ArrayTimeSeries as ts
import binarytree
import pickle
from proj6script import kernel_corr
import random

#generate 20 vantage points:

vantage = random.sample(range(1000), 20)
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
	for j in range(0, 1000):
		if j == i:
			continue
		dist = kernel_corr(tss[i], tss[j])
		db.set(-dist, 'ts_'+str(j))
	db.commit()
	db.close()