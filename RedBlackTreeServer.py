import sys
sys.path.append('../')
sys.path.append('./')

from simsearch.simSearcher import similaritySearcher

ss = similaritySearcher()

print(ss.simsearch_existed(200, 5))

