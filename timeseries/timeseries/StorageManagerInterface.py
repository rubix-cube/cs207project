from abc import ABCMeta, abstractmethod

class StorageManagerInterface(metaclass = ABCMeta):
    """
    Interface for StorageManager
    
    Methods
    -------
    store(id:int/string, t:SizedContainerTimeSeriesInterface):
        Returns SizedContainerTimeSeriesInterface
    
    size(id:int/string)
        Returns Integer

    get(id:int/string)
        Returns SizedContainerTimeSeriesInterface

    """

    @abstractmethod
    def store(self, id, t):
        return "This is the StorageManagerInterface, implement it in subclasses"

    @abstractmethod
    def size(self, id):
        return "This is the StorageManagerInterface, implement it in subclasses"

    @abstractmethod
    def get(self, id):
        return "This is the StorageManagerInterface, implement it in subclasses"    	
  	
