import socket
import random
import time
import threading
import struct
import pickle
import _thread
import sys
from timer import Timer

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

# Receive thread
def receive(socket):
    print("")
    print("in recv")
    global mutex
    global num
    global timer
    value = True
    while value:
        # try:
        #     mutex.aquire()
        # except:
        #     print("mutex issues")
        print("trying to receive")
        packet, addr = socket.recvfrom(bufferSize)
        print("received bob")
        packet, _ = packet, addr
        ack, _ = extractPacket(packet)
        if not packet:
            print ("No ACK")
        else:
            # If we get an ACK for the first in-flight packet
            print("Got ACK", ack)
            if (ack >= num):
                num = ack + 1
                print("num updated", num)
                timer.stop()
                timer.start()
                value = False

def readFile(filename):
    file = open(filename, 'rb')
    packet = []
    seqNum = 0
    while True:
        data = file.read()
        if not data:
            break
        packet.append(makePacket(seqNum, data))
        seqNum += 1

#send using thread
def send(socket, filename, address):
    global mutex, num, timer
     # Add all the packet to the buffer
    readFile(filename)
    packetNums = 0
    windowSize = windowSizeSet(packetNums)
    sendNext = 0
    num = 0

    while num <= packetNums:
        # Send all the packet in window size
        while sendNext < num + windowSize:
            print("Sending packet", sendNext)
            socket.sendto(packet[sendNext],address)
            sendNext += 1
            packetNums += 1

        # Start timer
        if not timer.running():
            print("Start timer")
            timer.start()
            # Wait until timer goes off or get an ACK
            while not timer.timeout():
                # Start the receiver thread
                try:
                    _thread.start_new_thread(receive, (socket,))
                except AttributeError and RuntimeError:
                    print("thread issues")
                print("Received", packetNums)
                try:
                    mutex.release()
                except:
                    print("release issues")
                print("Sleeping")
                time.sleep(timerSleep)
                try:
                    mutex.acquire()
                except:
                    print("can't get thread")
                if timer.timeout():
                    print("Timeout")
                    timer.stop();
                    sendNext = num
                else:
                    print("Shifting window")
                    windowSize = windowSizeSet(packetNums)
                    try:
                        mutex.release()
                    except:
                        print("final release...not")
    num += 1
    file.close()

timerSleep = 0.10
timerTimeout = 3
windowSize = 3
bufferSize = 1024
dataSize = 12
dataList = []
port = 8000

#Resources for threading
num = 0
mutex = _thread.allocate_lock()
timer = Timer(timerTimeout)


#to run
if __name__ == '__main__':
    host = socket.gethostname()
    clientAddress = (host, port)
    # serverAddress = (host, 0)
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind(clientAddress)
    fileCreate()
    filename = sys.argv[0]
    addrSend = estConnection()
    send(socket, filename, addrSend)
    print("end session")


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
