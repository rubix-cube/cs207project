import os
import numpy as np
import json
import random
from socket import *
import threading
import pickle
from _thread import *


from timeseries.StorageManagerInterface import StorageManagerInterface
from timeseries.ArrayTimeSeries import ArrayTimeSeries

class FileStorageManager(StorageManagerInterface):
	
	"""
	FileStorageManager class inherited from StorageManagerInterface
	
	Attributes
	----------
	_id: int
		unique integer id for object saved on disk
		TimeSeries objects are stored as 2-D numpy array

	Methods
	-------
	Basic methods are inherited from StorageManagerInterface, with method for generating unique id for storage if no user specified given
	
	Usage
	--------
	FileStorageManager used to communicate with disk, can store to/get from disk
	sizes are tracked
	Saved as json file
	"""

	def __init__(self):
		"""
		The constructor either creates a json file called "id.json" to store an id dictionary if none existed, or open the existing "id.json" file. 
		The json file stores dictionary of existing ids with correspondoing length. 
		"""
		if not os.path.exists('sm_data/'):
			os.makedirs('sm_data/')

		try:
			json_file = open('sm_data/id.json', 'r')
			self._id = json.load(json_file)
		except:
			self._id = dict()

	def store(self, tid, t):
		"""
		The function stores the given timeseries with corresponding id

		Args
		--------
		 - tid: unique id of type string to be used to store the timeseries. if is already exists, will overwrite current data
		 - t: timeseries object, implemented to take in either TimeSeries or ArrayTImeSeries. 

		"""
		if isinstance(tid, int):
			tid = str(tid)
		# Convert time series to correct format
		timeseries = np.vstack((t.times(), t.values())).astype(np.float64)

		# Save size of time series
		self._id[tid] = len(t.times())

		# Save time series
		np.save("sm_data/"+str(tid), timeseries)

		# Save sizes dict with each store of time series
		with open("sm_data/id.json", "w") as json_file:
			json.dump(self._id, json_file)


	def size(self, tid):
		"""
		The function returns the size of given stored timeseries. 

		Args
		--------
		 - tid: id of timeseries to look up length

		Return
		--------
		return the stored length with corresponding id from the id dictionary, will return -1 if id does not exist

		"""

		if not isinstance(tid, str):
			tid = str(tid)
		if tid in self._id:
			return self._id[tid]
		else:
			return -1

	def get(self, tid):
		"""
		The function gets the stored timeseries value on disk with the given id 

		Args
		------
		- tid: id for the time series values to be looked up from disk

		Return
		------
		values returned in the form of ArrayTimeSeries object. 
		will return non if no file existed with the given tid

		"""
		# Returns SizedContainerTimeSeriesInterface object
		if not isinstance(tid, str):
			tid = str(tid)
		print("SELF_ID",self._id)
		if tid in self._id:
			timeseries = np.load("sm_data/"+tid+".npy")
			return ArrayTimeSeries(timeseries[0], timeseries[1])
		else:
			return None

	def generateId(self):
		"""
		Function to generate id if no user specified one given, as string with prefix "autogenid"
		will randomly get an integer between 0 and 9, and check if existed in file already. 
		If existed, will generate another integer and append to the existing id. 
		Repeat until unique one generated. 
		"""

		i = random.randint(0,9)
		rid = 'autogenid'
		while True:
			rid += str(i)
			if rid not in self._id:
				return rid
			i = random.randint(0,9)

	def clean_up(self):
		if os.path.exists('sm_data/'):
			for f in os.listdir('sm_data/'):
				os.remove(os.path.join('sm_data/', f))

"""
A global StorageManager object is created to be passed into SMTimeSeries
"""
StorageManager = FileStorageManager()



