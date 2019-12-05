"""
Ben Hunt
Ryan Bauert
Austin Kelly
Tony Ho
"""
import socket
import random
from timer import Timer
import time
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

def disconnection(sock, address):
        sock.sendto(b'close', address)
        kill, addr = sock.recvfrom(1024)
        print(kill)
        if kill:
            sock.sendto(b'okay', addr)
            print("Received close acknowledgement from {}".format(addr))
            print("Connection Closed\n\n")
        else:
            print("abrupt abort")

def createData(filename):
    dataList = []
    file = open(filename, "w+")
    for i in range (12):
            dataList.append(random.randint(1,1001))
    for i in dataList:
        file.write(str(i) + "\n")
    file.close()

def send(socket, address, file):
    with open(file, 'rb') as f:
        packets = f.read().splitlines()
    packets = [x.strip() for x in packets]
    count = 0
    sendNext = 0
    t = Timer(2)
    dropRate = 0;
    while sendNext < 12:
        # send all the packets in the window
        while count < 3:
            dropRate = random.randint(0,99)
            if dropRate < 5:
                print("dropped frame", sendNext)
                pass
            elif (dropRate >=5 and dropRate < 15):
                delayTime = round(random.random()*4 + 1,1)
                print("delayed frame", sendNext, " ", delayTime)
                time.sleep(delayTime)
                socket.sendto(packets[sendNext], address)
                count += 1
                sendNext += 1
            else:
                socket.sendto(packets[sendNext], address)
                print("successful frame", sendNext)
                count += 1
                sendNext += 1
        # wait for ack from client
        t.start()
        while not t.timeout():
            ack, addr = socket.recvfrom(1024)
            if ack:
                print("received ack: ", ack)
                break
        #if we time out send the packet again
        if t.timeout():
            socket.sendto(packets[sendNext], address)
        t.stop()
        count = 0

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Awaiting connection...")
    host = socket.gethostname()
    port = 8000
    sock.bind((host,port))
    filename = "output"
    counter = 0
    while True:
        createData(filename)
        address = estConnection(host, port)
        send(sock,address, filename)
        disconnection(sock,address)
        print("Awaiting connection...")
        counter += 1
        filename = 'output' + str(counter)
