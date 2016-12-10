from setuptools import setup

setup(
	name='timeseries', 

	version='1.0.0',

	description='TimeSeries package, including various kinds of TimeSeries and a TimeSeries Storage Manager.',

	url='https://github.com/rubix-cube/cs207project',

	author='rubix-cube',

	classifiers=[
	'Programming Language :: Python :: 3.5'
	], 

	packages=['timeseries'],

	install_requires=['numpy'],

	setup_requires=['pytest-runner'],

	test_suite='tests',

	tests_require=['pytest'],

)