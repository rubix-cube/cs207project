from timeseries.StorageManagerInterface import StorageManagerInterface
from timeseries.ArrayTimeSeries import ArrayTimeSeries
import numpy as np
import json
import random

class FileStorageManager(StorageManagerInterface):
	def __init__(self):
		try:
			json_file = open('id.json', 'r')
			self._id = json.load(json_file)
		except:
			self._id = dict()

	def store(self, tid, t):
		if isinstance(tid, int):
			tid = str(tid)
		# Convert time series to correct format
		timeseries = np.vstack((t.times(), t.values())).astype(np.float64)

		# Save size of time series
		self._id[tid] = len(t.times())

		# Save time series
		np.save(str(tid), timeseries)

		# Save sizes dict with each store of time series
		with open("id.json", "w") as json_file:
			json.dump(self._id, json_file)


	def size(self, tid):
		if not isinstance(tid, str):
			tid = str(tid)
		if tid in self._id:
			return self._id[tid]
		else:
			return -1

	def get(self, tid):
		# Returns SizedContainerTimeSeriesInterface object
		if not isinstance(tid, str):
			tid = str(tid)
		if tid in self._id:
			timeseries = np.load(tid+".npy")
			return ArrayTimeSeries(timeseries[0], timeseries[1])
		else:
			return None

	def generateId(self):
		i = random.randint(0,9)
		rid = 'autogenid'
		while True:
			rid += str(i)
			if rid not in self._id:
				return rid
			i = random.randint(0,9)

StorageManager = FileStorageManager()

if __name__ == '__main__':
	StorageManager = FileStorageManager()
	a = ArrayTimeSeries([1,2,3],[4,5,6])
	print(a)
	autoId = StorageManager.generateId()
	StorageManager.store(autoId, a)
	s = StorageManager.get(autoId)
	print(s)

