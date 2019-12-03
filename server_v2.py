import socket
import random
import time
import threading
import struct
import pickle
import _thread
import sys
from timer import Timer

#Resources for threading
a = 0.5
num = 0
mutex = _thread.allocate_lock()
timer = Timer(a)

def conError():
    print ("connection error")
    s.close()

def estConnection():
        data, addr = socket.recvfrom(1024) # receive 1
        if data:
            print ("Received {} from {}".format(data,addr))
            socket.sendto(data, addr) # sending 1
            print ("Sending {} to {}".format(data,addr))
            data, addr = socket.recvfrom(1024) # receive 2
        if data:
            print("Connection Established")
            return addr
        else:
            print("Connection Failed")
            return None
            # sock.close()
def disconnection(data, sock, addr):
        if data == b'terminated':
            sock.sendto(b'okay', addr)
            print("Received close acknowledgement from {}".format(addr))
            print("Connection Closed")
            sock.close()

#create data list
def dataCreate():
    for i in range (dataSize):
            dataList.append(random.randint(1,1001))

#insert dataList to a file
def fileCreate():
    file = open("filename", "w")
    dataCreate()
    for i in dataList:
        file.write(str(i) + "\n")
    file.close()

# Sets the window size
def windowSizeSet(packetNums):
    global num
    return min(windowSize, packetNums - num)

# Creates a packet from a sequence number and byte data
def makePacket(seqNum, data = b''):
    seqBytes = seqNum.to_bytes(4, byteorder = "little", signed = True)
    return seqBytes + data

# Extracts sequence number and data from a non-empty packet
def extractPacket(packet):
    seqNum = int.from_bytes(packet[0:4], byteorder = "little", signed = True)
    return seqNum, packet[4:]

#send using thread
def send(socket, filename, address):
    global mutex, num, timer
    file = open(filename, 'rb')
     # Add all the packet to the buffer
    packet = []
    seqNum = 0
    while True:
        data = file.read()
        if not data:
            break
        packet.append(makePacket(seqNum, data))
        seqNum += 1
    packetNums = dataSize
    windowSize = 3 #windowSizeSet(packetNums)
    sendNext = 0
    num = 0
    i = 0
	#start the receiver thread
    _thread.start_new_thread(receive, (socket,))
    while num < (packetNums/windowSize):
        # Send all the packet in window size
        while i < windowSize and sendNext < dataSize:
            print("Sending packet", sendNext)
            t1 = threading.thread(socket.sendto, (packet[sendNext], address))
            t1.start()
            t1.join()
            sendNext += 1
        i = 0
        # Start timer
        if not timer.running():
            print("Start timer")
            print("a")
            timer.start()
            print("b")
            # Wait until timer goes off or get an ACK
        while timer.running() and not timer.timeout():
		# Start the receiver thread
            print("4")
            #mutex.release()
            print("c")
            print("Sleeping")
            time.sleep(timerSleep)
            mutex.acquire()
        if timer.timeout():
            print("Timeout")
            timer.stop();
            sendNext = num
        #else:
            #print("Shifting window")
            #windowSize = windowSizeSet(packetNums)
        mutex.release()
    file.close()

# Receive thread
def receive(socket):
    global mutex
    global num
    global timer
    value = True
    while value:
        pkt, addr = socket.recvfrom(bufferSize)
        pkt1, _ = pkt, addr
        ack, _ = extractPacket(pkt1)
        print("Got Ack", ack)
        if(ack >= num):
            mutex.acquire()
            num = ack + 1
            print("Num updated", num)
            timer.stop()
            mutex.release()

timerSleep = 0.10
timerTimeout = 3
windowSize = 3
bufferSize = 1024
dataSize = 12
dataList = []
port = 8000


#to run
if __name__ == '__main__':


    host = socket.gethostname()
    clientAddress = (host, port)
    serverAddress = (host, 0)
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind(clientAddress)
    fileCreate()
    for i in range (len(dataList)):
            print (i, dataList[i])

    filename = sys.argv[0]
    addrSend = estConnection()
    send(socket, filename, addrSend)


#array = []
#for i in range(20):
#    array.append(random.randint(1,1001))
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#data_array = pickle.dumps(array)


#port = 8000
#sock.bind((host,port))
#address = estConnection(host, port)
#sock.sendto(b'close', address)
#data, addr = sock.recvfrom(1024)
#print(data)
#disconnection(data, sock, addr)
