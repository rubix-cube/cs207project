# SIMSEARCH

This directory contains methods to search the most similar timeseries from a database of timeseries where each index is an unbalanced binary tree, as presented in CS207's lab 10.
This script will only with the ArrayTimeSeries format.

### Files:

A number of files are contained in this directory. Here's a quick presentation of each of them:

- binarytree.py: contains the data structure
- proj6script.py: demo script to illustrate the use of the Kernelized Cross Correlation
- generate_data.py: script to generate timeseries data using the tsmaker function
- generate_vantagepoints.py: script to select randomly vantage points and generate the indices
- simsearch.py: script to look for the top N most similar timeseries to a timeseries parsed as argument in the command line

### Usage:

Scripts should be called in the following order:

1. generate_data.py
2. generate_vantagepoints.py
3. simsearch.py

Taking into account arguments:

1. `python generate_data.py 1000`
2. `python generate_vantagepoints.py --n 20`
3. `python simsearch.py ts_data\ts_0 --n 10`

Note:

- generate_data.py has a mandatory argument which must be parsed in the command line as the number of timeseries wanted e.g. 1000
- generate_vantagepoints.py takes an optional argument equal to the number of desired vantage points e.g. --n 20 and the default is set to 20
- simsearch.py takes a mandatory argument i.e. the timeseries of interest and the number of most similar timeseries desired e.g. --n 10 and the default is set to 1
