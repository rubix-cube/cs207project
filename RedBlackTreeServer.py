# import sys
# sys.path.append('../')
# sys.path.append('./')

from timeseries.TimeSeries import TimeSeries
from simsearch.simSearcher import similaritySearcher

ss = similaritySearcher()
# ts = TimeSeries(['1','2', '3'], ['4', '5', '6'])
print(ss.simsearch_existed(5, 5))

# print(ss.simsearch_non_exist(ts, 5))

