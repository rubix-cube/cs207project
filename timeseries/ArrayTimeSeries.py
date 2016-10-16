import numpy as np
class ArrayTimeSeries(TimeSeries):
	def __init__(self, seq):
		self.arr = np.array(list(seq))
