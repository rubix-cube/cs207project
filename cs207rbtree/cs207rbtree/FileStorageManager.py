from StorageManagerInterface import StorageManagerInterface

class FileStorageManager(StorageManagerInterface):
	def __init__(self):
		pass

	def store(self, id, t):
        return "This is the StorageManagerInterface, implement it in subclasses"

    def size(self, id):
        return "This is the StorageManagerInterface, implement it in subclasses"

    def get(self, id):
    	# Returns SizedContainerTimeSeriesInterface object
        return ""