# SIMSEARCH

This directory contains methods to search the most similar timeseries from a database of timeseries where each index is an unbalanced binary tree, as presented in CS207's lab 10.
This script will only with the ArrayTimeSeries format.

## NB:
Due to the fact that the timeseries code provided in rubixcube was not installable, please look at the way these packages are imported in the files of this directory.

### Files:

A number of files are contained in this directory. Here's a quick presentation of each of them:

- util.py: contains methods to evaluate different types of correlation as well as generating timeseries.
- binarytree.py: contains the data structure
- proj6script.py: demo script to illustrate the use of the Kernelized Cross Correlation
- generate_data.py: script to generate timeseries data using the tsmaker function
- generate_vantagepoints.py: script to select randomly vantage points and generate the indices
- simsearch.py: script to look for the top N most similar timeseries to a timeseries parsed as argument in the command line

### Usage:

#### Scripts

Scripts should be called in the following order:

1. generate_data.py
2. generate_vantagepoints.py
3. simsearch.py

Taking into account arguments:

1. `python generate_data.py 1000`
2. `python generate_vantagepoints.py --n 20`
3. `python simsearch.py ts_data\ts_0 --n 10`

Note:

- `generate_data.py` has a mandatory argument which must be parsed in the command line as the number of timeseries wanted e.g. 1000
- `generate_vantagepoints.py` takes an optional argument equal to the number of desired vantage points e.g. `--n 20` and the default is set to 20 and another one corresponding to the number of timeseries in the database, default 1000
- `simsearch.py` takes a mandatory argument i.e. the timeseries of interest and the number of most similar timeseries desired e.g. `--n 10` and the default is set to 1

#### BinaryTree Sturcture and DBS:

Timeseries are considered close to each other if their kernelised cross correlation is close to 1 and far from each other if close to 0. This is why the databases have keys equal to `-kernel_corr(ts1, ts2)` and value: `ts2`. The main addition to the code written in lab10 is the addition of the function `get_closer_than` which will look for values whose corresponding keys are smaller than the value parsed as argument.

### Data:

This directory holds two main data file: ts_data and dbs. Both of them are respectively filled by `generate_data.py` and `generate_vantagepoints.py`.

### Testing:
Testing is also provided in this directory. A first testing file is used to assess the data structure and the second file is used to test kernel correlation and the lookup methods.

