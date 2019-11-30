import socket
import random
import time
import threading
import struct
import pickle

def conError():
    print ("connection error")
    s.close()


def estConnection(port, host):
        data, addr = sock.recvfrom(1024) # receive 1

        if data:
            print ("Received {} from {}".format(data,addr))
            sock.sendto(data, addr) # sending 1
            print ("Sending {} to {}".format(data,addr))
            data, addr = sock.recvfrom(1024) # receive 2
        if data:
            print("Connection Established")
            return addr
        else:
            print("Connection Failed")
            sock.close()
def disconnection(data, sock, addr):
        if data == b'terminated':
            sock.sendto(b'okay', addr)
            print("Received close acknowledgement from {}".format(addr))
            print("Connection Closed")
            sock.close()

array = []
for i in range(20):
    array.append(random.randint(1,1001))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data_array = pickle.dumps(array)

print("Awaiting connection...")

host = socket.gethostname()
port = 8000
sock.bind((host,port))
address = estConnection(host, port)
sock.sendto(b'close', address)
data, addr = sock.recvfrom(1024)
print(data)
disconnection(data, sock, addr)
