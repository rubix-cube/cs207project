import sys, os, inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])
import unittest
import binarytree
import simsearch
import util
import numpy as np
import pickle

class DistancesTest(unittest.TestCase):
    '''
    These tests verifies that the distance methods as well as the search.
    ''' 
    def test_tsmakers(self):
        #Checks that tsmakers returns ArrayTimeSeries
        t1 = util.tsmaker(0.5, 0.1, 0.01)
        self.assertEqual(type(t1), util.ts.ArrayTimeSeries) 

    def test_standardisation(self):
        #Checks that standarisation is correct
        t1 = util.ts.ArrayTimeSeries(range(10), range(10))
        stand_t1 = util.stand(t1, t1.mean(), t1.std())
        m = np.mean(t1._value)
        v = np.std(t1._value)
        self.assertTrue(all(abs(stand_t1._value[i]-((t1._value-m)/v)[i])<0.000000001 for i in range(len(t1))))
        
    def test_kc_with_itself(self):
        #Checks that the kc is equal to 1 when evaluating the kc of a timeseries with itself
        t1 = util.tsmaker(0.5, 0.1, 0.01)
        self.assertTrue(abs(util.kernel_corr(t1, t1)-1)<0.000001)

    def test_kc_smaller_1(self):
        #Checks that the kc is smaller than 1 for any pair of random of timeseries
        t1 = util.random_ts(1)
        t2 = util.random_ts(10)
        self.assertTrue(util.kernel_corr(t1,t2)<=1)

    def test_search_closest(self):
        #Checks that we can correctly report the closest point in the DB
        ts = pickle.load(open("../ts_data/ts_0.p", "rb" ))
        ts_stand = util.stand(ts, ts.mean(), ts.std())
        vantage = pickle.load(open( "../ts_data/vantage_points.p", "rb"))
        closest_vantage, closest_distance  = simsearch.eval_closest_vantage(ts_stand, vantage, True)
        closest_in_all = simsearch.in_radius_from_vantage(ts_stand, closest_vantage[0], True)
        top_m, top_b = simsearch.return_top(ts_stand, closest_in_all, 1, False, True)
        san = simsearch.sanity(ts_stand, 1)[0]
        self.assertEqual('ts_data/'+top_b+'.p', san[0])

    def test_search_topn(self):
        #Checks that we can correctly report the n closest points in the DB
        ts = pickle.load(open("../ts_data/ts_0.p", "rb" ))
        ts_stand = util.stand(ts, ts.mean(), ts.std())
        vantage = pickle.load(open( "../ts_data/vantage_points.p", "rb"))
        closest_in_all = []
        for v in vantage:
            closest_in_all += simsearch.in_radius_from_vantage(ts_stand, v, True)
        closest_in_all = list(set(closest_in_all))
        te=simsearch.return_top(ts_stand, closest_in_all, 10, False, True)
        san = simsearch.sanity(ts_stand, 10)
        self.assertTrue(all(san[i][0]=='ts_data/'+te[i][0]+'.p' for i in range(len(san))))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DistancesTest))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())