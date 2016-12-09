from timeseries.ArrayTimeSeries import ArrayTimeSeries
import numpy as np
import json

from socket import *
import threading
import pickle
from _thread import *
from timeseries.FileStorageManager import FileStorageManager

def clientThread(conn, sm):
  data = b''
  while True:
  #    conn.send("Server waiting for input:".encode())
    rec = conn.recv(1024)
    if not rec:
      break
    print("Server received:",rec)
    receivedData = pickle.loads(rec)
    if receivedData['cmd'] == "BYID":
      # Get ts storage using id received
      conn.send(pickle.dumps("---Some timeseries---"))
    else:
      break
    # data += rec
    # print("DATA",pickle.loads(data))    
  conn.close()


StorageManager = FileStorageManager()
a = ArrayTimeSeries([1,2,3],[4,5,6])
print(a)
autoId = StorageManager.generateId()
StorageManager.store(autoId, a)
s = StorageManager.get(autoId)
print(s)

s = socket()
host = gethostname()
port = 12340
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
try:
  while True:
    c, addr = s.accept()
    print("Got connection from:",addr)
    t = threading.Thread(target=clientThread,args=(c,StorageManager))
    t.start()
finally:
  s.close()

