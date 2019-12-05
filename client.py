"""
Ben Hunt
Ryan Bauert
Austin Kelly
Tony Ho
"""


import socket
import time
import sys
from timer import Timer

def fileWrite(data):
    count = 0
    file = sys.argv[1]
    open(file, "w+")
    while data is not None and count < 1:
        file.write(data)
        count += 1
    file.close()

def receive(data):
    count = 0
    file = open(sys.argv[1], "w")
    x = 0
    dataList = []
    while data is not None:
        t = Timer(5)
        t.start()
        try:
            data, addr = sock.recvfrom(1024)
            if data and data != b'close':
                print("Received data: ", data)
                x +=1
                text = str(data)
                if count == 0:
                    dataList.append(text)
                    count += 1
                else:
                    dataList.append(text)
                    count = 0
                if x%3 == 0:
                    sock.sendto(b'ack', addr)
                    for a in range (len(dataList)):
                        file.write(dataList[a])
                        file.write("\n")
                    dataList.clear()
            elif data == b'close':
                print(data)
                file.close()
                sock.settimeout(None)
                return data
        except:
            if t.timeout():
                sock.sendto(b'resend', addr)
                break


    print ("connection error")
    s.close()

def estConnection(port, host):
    address = (host,port)
    resend = False
    reRecv = False
    count = 0
    #send 1
    while not resend and count < 3:
        try:
            sent = sock.sendto(b'10', address)
            print("sending {} bytes to {} ".format(sent,address))
            resend = True
        except:
            print("this didn't send #1")
            count += 1
    #receive 1
    count = 0
    while not reRecv and count < 3 :
        try:
            data, addr = sock.recvfrom(1024)
            reRecv = True
        except:
            print("this didn't receive #1")
            count += 1
    count = 0
    if data:
        print ("data received: ", data)
        #send 2
        while True and count < 3:
            try:
                sent = sock.sendto(b'ack', address)
                print("sending {} to {}".format(sent, address))
                print("connection established")
                return data
            except:
                print("this didn't send #2")
                count += 1
    else:
        return None

def disconnection(data, soc):
    if data == b'close':
        sock.sendto(b'terminated', (server, port))
        print("terminated")
        d, addr = sock.recvfrom(1024)
        if d == b'okay':
            print("Connection gracefully terminated\n\n")
            sock.close()
            return True
        else:
            print("Can't terminate")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
port = 8000
data = None
server = input("Enter the IP address of the server to connect to: ")
data = estConnection(port, server)

while True:
    data = receive(data)
    closed = disconnection(data, sock)
    if closed:
        break
