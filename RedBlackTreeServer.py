# import sys
# sys.path.append('../')
# sys.path.append('./')

from timeseries.TimeSeries import TimeSeries
from simsearch.simSearcher import similaritySearcher
from simsearch.calculateDistance import random_ts

ss = similaritySearcher()
ts = random_ts(1)
# print(ss.simsearch_existed(5, 5))

print(ss.simsearch_non_exist(ts, 5))

