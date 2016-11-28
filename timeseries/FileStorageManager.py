from StorageManagerInterface import StorageManagerInterface
from ArrayTimeSeries import ArrayTimeSeries
import numpy as np
import json

class FileStorageManager(StorageManagerInterface):
	def __init__(self):
		try:
			json_file = open('id.json', 'r')
			self._id = json.load(json_file)
		except:
			self._id = dict()

	def store(self, id, t):
		if isinstance(id, int):
			id = str(id)
		timeseries = np.vstack((t.times(), t.values())).astype(np.float64)
		self._id[id] = len(t.times())
		np.save(str(id), timeseries)
		with open("id.json", "w") as json_file:
			json.dump(self._id, json_file)


	def size(self, id):
		if not isinstance(id, str):
			id = str(id)
		if id in self._id:
			return self._id[id]
		else:
			return -1

	def get(self, id):
		# Returns SizedContainerTimeSeriesInterface object
		if not isinstance(id, str):
			id = str(id)
		if id in self._id:
			timeseries = np.load(id+".npy")
			return ArrayTimeSeries(timeseries[0], timeseries[1])
		else:
			return None

StorageManager = FileStorageManager()

