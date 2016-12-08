from timeseries.ArrayTimeSeries import ArrayTimeSeries
import numpy as np
import json

from socket import *
import threading
import pickle
from _thread import *
from timeseries.FileStorageManager import FileStorageManager

def clientThread(conn):
  data = b''
  while True:
  #    conn.send("Server waiting for input:".encode())
    rec = conn.recv(1024)
    if not rec:
      break
    print("Server received:",rec)
    print("REC:",pickle.loads(rec))

    data += rec
    print("DATA",pickle.loads(data))
    
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
    t = threading.Thread(target=clientThread,args=(c,))
    t.start()
finally:
  s.close()

# s = socket()
# host = gethostname()
# port = 12340
# s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# s.bind((host, port))

# s.listen(5)

# def clientThread(conn):
#   data = b''
#   while True:
# #    conn.send("Server waiting for input:".encode())
# #    data = conn.recv(1024)
# #    if data == b"quit":
# #      break
# #    print("Server received:",data)
#     received = conn.recv(1024)
#     if not received:
#       break
#     data += received

#   print(pickle.loads(data))
#   conn.close()
    
# try:
#   while True:

#     # init sm   

#     c, addr = s.accept()
#     print("Got connection from:",addr)
#     t = threading.Thread(target=clientThread,args=(c,))
#     t.start()
# finally:
#   s.close()
#     start_new_thread(clientThread, (c,))
#     c.send("Thank you for connecting!".encode())
#     c.close()
