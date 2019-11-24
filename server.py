import socket
import random
import time
import threading

def conError()
    print "connection error"
    s.close()

array = []
for i in range(20):
    array.append(random.randint(1,1001))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostname()
port = 8000
s.bind((host,port))
data, addr = s.recvfrom(1024) # listening

while True:
    if data == "Hello World":
        timer.
        print "message: ", data
        s.sendto("Hello Universe", addr)
    data, addr = s.recvfrom(1024)
    print data
    s.sendto(bytes(array), addr)
    print array
    s.close()
