"""Commandline tool for finding the closest timeseries points to a given timeseries
"""
import sys
sys.path.append('../')
sys.path.append('./')

import os
import pickle
import heapq

from cs207rbtree import *
from simsearch.calculateDistance import calcDist, standardize
import click

from simsearch.Globals import NUM_TS_DATA, NUM_VANTAGE_PTS

	
class similaritySearcher:

	def __init__(self):

		self.ts_data = []
		for id in range(NUM_TS_DATA):
			cur_ts = pickle.load(open('simsearch/ts_data/ts_%d.dat'%id, 'rb'))
			self.ts_data.append(cur_ts)

		self.vantage_pts = []
		vantage_ids = pickle.load(open('simsearch/vantage_pts.dat', 'rb'))
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
			cur_db = connect('simsearch/ts_db_index/ts_' + cur_vt_id + '.db')
			# find ts in current circle
			radius = 2 * cur_dist
			dist_ids = cur_db.get_smaller_than(radius)
			cur_db.close()
			# calc distance from input ts to ts in current circle
			for (ds, Id) in dist_ids:
				if Id not in id_set:
					id_set.add(Id)
					cur_ts = pickle.load(open('simsearch/ts_data/ts_' + Id + '.dat', 'rb'))
					ds_to_input = calcDist(input_ts, cur_ts)
					heapq.heappush(similar_ts_pQ, (-ds_to_input, Id))
					if len(similar_ts_pQ) > n:
							heapq.heappop(similar_ts_pQ)
		sim_ts = sorted([(-ds, Id) for (ds, Id) in similar_ts_pQ])
		return sim_ts


	def simsearch_existed(self, id, n):
		# return n ts except id itself
		# make sure id is a integer
		if type(id) is not int or type(n) is not int:
			raise TypeError('Invalid Input Type')
		
		if id >= NUM_TS_DATA or id < 0:
			raise ValueError('Input Id Out of Range')

		if n + 1 > NUM_VANTAGE_PTS:
			raise ValueError('Number of Queries exceeds the Number of Vantage Points')
		
		input_ts = pickle.load(open('simsearch/ts_data/ts_' + str(id) + '.dat', 'rb'))

		# calc dist from input_ts to vantage points
		dist = []
		for (vt, id) in self.vantage_pts:
			dist.append((calcDist(vt, input_ts), str(id)))
		# sort vantage points by distance
		dist.sort(key=lambda kv: kv[0])

		# print(dist)
		id_set = set()
		similar_ts_pQ = []
		for i in range(n + 1):
			cur_dist = dist[i][0]
			cur_vt_id = dist[i][1]
			cur_db = connect('simsearch/ts_db_index/ts_' + cur_vt_id + '.db')
			# find ts in current circle
			radius = 2 * cur_dist
			dist_ids = cur_db.get_smaller_than(radius)
			cur_db.close()
			# calc distance from input ts to ts in current circle
			for (ds, Id) in dist_ids:
				if Id not in id_set:
					id_set.add(Id)
					cur_ts = pickle.load(open('simsearch/ts_data/ts_' + Id + '.dat', 'rb'))
					ds_to_input = calcDist(input_ts, cur_ts)
					heapq.heappush(similar_ts_pQ, (-ds_to_input, Id))
					if len(similar_ts_pQ) > n + 1:
							heapq.heappop(similar_ts_pQ)
		# except id itself
		sim_ts = sorted([(-ds, Id) for (ds, Id) in similar_ts_pQ])
		return sim_ts[1:]
