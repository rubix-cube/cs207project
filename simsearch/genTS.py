import sys
sys.path.append('../')

import os
import pickle
import random

from calculateDistance import tsmaker, standardize
import click

from Globals import mean_start, mean_end, std_start, std_end, scale_start, scale_end

@click.command()
@click.option('-n', default=1000, help='number of ts to generate, default 1000')
@click.option('--n', default=1000, help='number of ts to generate, default 1000')
def genTS(n):
	"""generate n standardized time series, each stored in a file in ts_data/.
	"""
	if not os.path.exists('ts_data/'):
		os.makedirs('ts_data/')

	mean = [random.uniform(mean_start, mean_end) for i in range(n)]
	std = [random.uniform(std_start, std_end) for i in range(n)]
	scale = [random.randint(scale_start, scale_end) for i in range(n)]

	for i in range(n):
		with open('ts_data/ts_' + str(i) + '.dat', 'wb+') as f:
			ts = standardize(tsmaker(mean[i], std[i], scale[i]))
			pickle.dump(ts, f)

if __name__ == '__main__':
	genTS()