from simsearch.search_funcs import simsearch_non_exist, simsearch_existed
from timeseries.TimeSeries import TimeSeries
from socket import *
import threading
import pickle
from _thread import *


def clientThread(conn):
	while True:
		rec = conn.recv(1024)
		if not rec:
			break
		
		receivedData = pickle.loads(rec)
		if receivedData['cmd'] == "SIMID":
			# Find 5 similar points by id
			results = simsearch_existed(receivedData['id'], receivedData['n'])
			conn.send(pickle.dumps(results))
		elif receivedData['cmd'] == "SIMTS":
			# Find 5 similar points by ts
			ts = TimeSeries(input_value=receivedData['value'], input_time=receivedData['time'])
			results = simsearch_non_exist(ts, receivedData['n'])
			conn.send(pickle.dumps(results))
		else:
			break
		 
	conn.close()

if __name__ == "__main__":

	s = socket()
	host = gethostname()
	port = 12341
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(5)
	try:
		while True:
			c, addr = s.accept()
			print("Got connection from:",addr)
			t = threading.Thread(target=clientThread,args=(c,))
			t.start()
	finally:
		s.close()
