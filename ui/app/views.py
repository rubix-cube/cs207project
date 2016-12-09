from flask import render_template, flash, redirect, session, url_for, request,g
from app import app, db
from .forms import LoginForm
from .models import User, Post, Timeseries
import json
from sqlalchemy import and_

import socket
import sys
import pickle

def connectRBTree():
	port = 12341
	s = socket.socket()
	host = socket.gethostname()
	s.connect((host, port))
	return s

def connectSM():
	port = 12340 
	s = socket.socket()
	host = socket.gethostname()	
	s.connect((host, port))
	return s

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Kevin'}
	posts = [{'author': {'nickname':'John'},
			'body': 'Beautiful day in Portland!'},
			{'author': {'nickname': 'Susan'},
			'body': 'The movie was cool!'}]

	return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/success/<name>')
@app.route('/success')
def success(name=None):
	return 'welcome %s' % name

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		user = request.form['nm']
		return redirect(url_for('success', name=user))
	else:
		user = request.args.get('nm')
		return redirect(url_for('success', name=user))

@app.route('/loginPage')
def loginPage():
	return render_template('login.html',
		title='Login')

@app.route('/createUser', methods=['GET'])
def createUser():
	u = User(nickname='keasadvin',email='ka@gmail.com')
	db.session.add(u)
	db.session.commit()
	print("Added user to db!")
	return json.dumps({"1":"1"});
	

@app.route('/timeseries', methods=['POST','GET'])
def timeseries():
	if request.method == 'POST':
		# adds a new timeseries into the database given a json which has a
		# key for an id and a key for the timeseries, and returns the timeseries
		# print(request.files['file'].read())
		data = request.get_json(force=True)
		data['cmd'] = "ADDTS"
		s = connectSM()
		try:
			s.send(pickle.dumps(data))
			response = pickle.loads(s.recv(1024))

		finally:
			s.close()
			return json.dumps(response)
		
	else:
		# should send back a json with metadata from all the time series
		# Get all rows from table
		results = set(Timeseries.query.all())

		# Get query parameters
		mean_in = request.args.get('mean_in')
		level_in = request.args.get('level_in')
		level = request.args.get('level')
		
		# Filter by mean in 
		if mean_in is not None:
			mean_in = mean_in.split('-')
			m_min, m_max = float(mean_in[0]),float(mean_in[1])
			tmp = set(Timeseries.query.filter(and_(Timeseries.mean >= m_min, Timeseries.mean <= m_max)).all())
			results &= tmp
		
		# Filter by level in 
		if level_in is not None:
			level_in = level_in.split(',') 
			tmp = set(Timeseries.query.filter(Timeseries.level.in_(level_in)).all())
			results &= tmp
		
		# Filter by level 
		if level is not None:
			tmp = set(Timeseries.query.filter_by(level=level).all())
			results &= tmp
		
		# Serialize objects 
		r = [e.serialize() for e in results]
		return json.dumps(r)
	
@app.route('/simquery', methods=['POST','GET'])
def simquery():
	if request.method == 'POST':
		# take a timeseries as an input in a JSON, carry out the query, and 
		# return the appropriate ids as well. 
		ts = request.form['timeseries'] # json format
		pass
	else:
		#  take a id=the_id querystring and use that as an id into the database
		# to find the timeseries that are similar, sending back the ids of (say) the top 5
		sim_id = request.args.get('id')
		s = connectRBTree()
		try:
			while True:
				toSend = {"cmd":"SIMID", "id":5, "n":5}
				s.send(pickle.dumps(toSend))
				rec = s.recv(1024)
				# TODO data MORE THAN 1024, protocol?
				rec = pickle.loads(rec)
				return json.dumps({"similar_points": rec})	
		finally:
			s.close()
		

@app.route('/timeseries/<id>')
def timeseries_id(id):
	# should send back metadata and the timeseries itself in a JSON payload
	
	# Get metadata
	t = Timeseries.query.get(id).serialize()

	# Get timeseries 
	s = connectSM()
	try:
		toSend = {"cmd":"BYID","id":id} # A = get timeseries by id, B = get all timeseries etc
		s.send(pickle.dumps(toSend))
		rec = s.recv(1024)
		rec = pickle.loads(rec)
		return json.dumps({"timeseries": rec, "metadata": t})	

	finally:
		s.close()



