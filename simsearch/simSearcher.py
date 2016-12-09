"""Commandline tool for finding the closest timeseries points to a given timeseries
"""
import sys
sys.path.append('../')
sys.path.append('./')

import os
import pickle
import heapq

from cs207rbtree import *
from calculateDistance import calcDist, standardize
import click

NUM_TS_DATA = 1000

class similaritySearcher:

	def __init__(self):

		self.ts_data = []
		for id in NUM_TS_DATA:
			cur_ts = pickle.load(open('ts_data/ts_%d.dat'%id, 'rb'))
			self.ts_data.append(cur_ts)

		self.vantage_pts = []
		vantage_ids = pickle.load(open('vantage_pts.dat', 'rb'))
		# load vantage points
		for id in vantage_ids:
			self.vantage_pts.append((self.ts_data[id], id))

	def simsearch_non_exist(self, input_ts, n):
		"""search for n closest points to input ts, results are stored as .dat file in search_res/
		"""

		input_ts = standardize(input_ts)
		# calc dist from input_ts to vantage points
		dist = []
		for (vt, id) in self.vantage_pts:
			dist.append((calcDist(vt, input_ts), str(id)))
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
					heapq.heappush(similar_ts_pQ, (-ds_to_input, Id))
					if len(similar_ts_pQ) > n:
							heapq.heappop(similar_ts_pQ)

		return similar_ts_pQ


	def simsearch_existed(self, id, n):
		# make sure id is a integer
		if type(id) is not int or int(id) >= NUM_TS_DATA or int(id) < 0:
			return None
		
		input_ts = pickle.load(open('ts_data/ts_' + id + '.dat', 'rb'))

		# calc dist from input_ts to vantage points
		dist = []
		for (vt, id) in self.vantage_pts:
			dist.append((calcDist(vt, input_ts), str(id)))
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
					heapq.heappush(similar_ts_pQ, (-ds_to_input, Id))
					if len(similar_ts_pQ) > n:
							heapq.heappop(similar_ts_pQ)

		return similar_ts_pQ
