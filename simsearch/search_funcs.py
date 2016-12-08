"""Commandline tool for finding the closest timeseries points to a given timeseries
"""
import sys
sys.path.append('../')

import os
import pickle
import heapq

from tsbtreedb import *
from calculateDistance import calcDist, standardize
import click


NUM_TS_DATA = 1000

def simsearch_non_exist(input_ts, n):
	"""search for n closest points to input ts, results are stored as .dat file in search_res/
	"""

	input_ts = standardize(input_ts)
	# load vantage points
	vantage_pts = []
	vantage_ids = pickle.load(open('vantage_pts.dat', 'rb'))
	# calc dist from input_ts to vantage points
	dist = []
	for i in vantage_ids:
		vt = pickle.load(open('ts_data/ts_' + str(i) + '.dat', 'rb'))
		dist.append((calcDist(vt, input_ts), str(i)))
	# sort vantage points by distance
	dist.sort(key=lambda kv: kv[0])

	# print(dist)
	id_set = set()
	similar_ts_pQ = []
	for i in range(n):
		cur_dist = dist[i][0]
		cur_vt_id = dist[i][1]
		cur_db = connect('ts_db_index/ts_' + cur_vt_id + '.db')
		# find ts in current circle
		radius = 2 * cur_dist
		dist_ids = cur_db.get_smaller_than(radius)
		cur_db.close()
		# calc distance from input ts to ts in current circle
		for (ds, Id) in dist_ids:
			if Id not in id_set:
				id_set.add(Id)
				cur_ts = pickle.load(open('ts_data/ts_' + Id + '.dat', 'rb'))
				ds_to_input = calcDist(input_ts, cur_ts)
				heapq.heappush(similar_ts_pQ, (-ds_to_input, cur_ts))
				if len(similar_ts_pQ) > n:
						heapq.heappop(similar_ts_pQ)

	return similar_ts_pQ


def simsearch_existed(id, n):
	if id >= NUM_TS_DATA:
		return None
	
	input_ts = pickle.load(open('ts_data/ts_' + id + '.dat', 'rb'))

	# load vantage points
	vantage_pts = []
	vantage_ids = pickle.load(open('vantage_pts.dat', 'rb'))
	# calc dist from input_ts to vantage points
	dist = []
	for i in vantage_ids:
		vt = pickle.load(open('ts_data/ts_' + str(i) + '.dat', 'rb'))
		dist.append((calcDist(vt, input_ts), str(i)))
	# sort vantage points by distance
	dist.sort(key=lambda kv: kv[0])

	# print(dist)
	id_set = set()
	similar_ts_pQ = []
	for i in range(n):
		cur_dist = dist[i][0]
		cur_vt_id = dist[i][1]
		cur_db = connect('ts_db_index/ts_' + cur_vt_id + '.db')
		# find ts in current circle
		radius = 2 * cur_dist
		dist_ids = cur_db.get_smaller_than(radius)
		cur_db.close()
		# calc distance from input ts to ts in current circle
		for (ds, Id) in dist_ids:
			if Id not in id_set:
				id_set.add(Id)
				cur_ts = pickle.load(open('ts_data/ts_' + Id + '.dat', 'rb'))
				ds_to_input = calcDist(input_ts, cur_ts)
				heapq.heappush(similar_ts_pQ, (-ds_to_input, cur_ts))
				if len(similar_ts_pQ) > n:
						heapq.heappop(similar_ts_pQ)

	return similar_ts_pQ
