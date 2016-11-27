import sys, os
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]+'/timeseries')

import numpy.fft as nfft
import numpy as np
import ArrayTimeSeries as ts
from scipy.stats import norm


def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.001)
    v = norm.pdf(t, m, s) + j*np.random.randn(1000)
    return ts.ArrayTimeSeries(t, v)

def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts.ArrayTimeSeries(t, v)

def stand(x, m, s):
    "standardize timeseries x my mean m and std deviation s"
    #your code here
    return (x.subConst(m)).multConst(1/s)

def ccor(ts1, ts2):
    "given two standardized time series, compute their cross-correlation using FFT"
    # http://lexfridman.com/blogs/research/2015/09/18/fast-cross-correlation-and-time-series-synchronization-in-python/
    #your code here
    fft_1 = nfft.fft(ts1._value)
    fft_2 = nfft.fft(np.flipud(ts2._value))
    cc = np.real(nfft.ifft(fft_1 * fft_2))
    return nfft.fftshift(cc)/len(ts1)

# this is just for checking the max correlation with the
#kernelized cross-correlation
def max_corr_at_phase(ts1, ts2):
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr

#The equation for the kernelized cross correlation is given at
#http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
#normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
#of a time series with itself is 1. We'll set the default multiplier to 1.
def kernel_corr(ts1, ts2, mult=1):
    "compute a kernelized correlation so that we can get a real distance"
    #your code here.
    ccorts = ccor(ts1, ts2)
    num = np.sum(np.exp(mult*ccorts))
    denom = np.sqrt(np.sum(np.exp(mult*ccor(ts1, ts1))))*np.sqrt(np.sum(np.exp(mult*ccor(ts2, ts2))))
    return num/denom