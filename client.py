import socket
import threading
import struct
import sys

def conError():
    print ("connection error")
    s.close()

def estConnection(port, host):
    address = (host,port)
    #send 1
    sent = socket.sendto(b'10', address)
    print("sending {} bytes to {} ".format(sent,address))
    #receive 1
    data, addr = socket.recvfrom(1024)
    if data:
        print ("data received: ", data)
        #send 2
        sent = socket.sendto(b'ack', address)
        print("sending {} to {}".format(sent, address))
        print("connection established")
        return addr
    else:
        return None

def disconnection(data, soc,addr):
    if data == b'close':
        soc.sendto(b'terminated', (server, port))
        d, addr = soc.recvfrom(1024)
        if d == b'okay':
            print("Connection gracefully terminated")
            return True
    return False

# Creates a packet from a sequence number and byte data
def makePacket(seqNum, data = b''):
    seqBytes = seqNum.to_bytes(4, byteorder = "little", signed = True)
    return seqBytes + data

# Extracts sequence number and data from a non-empty packet
def extractPacket(packet):
    seqNum = int.from_bytes(packet[0:4], byteorder = "little", signed = True)
    return seqNum, packet[4:]

# Receive packets from server
def receive(socket, filename):
    expectedNum = 0
    file = open(filename, 'wb')
    while True:
        # Get the next packet from server
        packet, addr = socket.recvfrom(bufferSize)
        if not packet:
            break
        seqNum, data = extractPacket(packet)
        print("Got packet", seqNum)

        # Send back an ACK
        if seqNum == expectedNum:
            print("Expected packet received")
            print("Sending ACK", expectedNum)
            packet = makePacket(expectedNum)
            socket.sendto(packet, addr)
            expectedNum += 1
            file.write(data)
        else:
            print("Sending ACK", expectedNum - 1)
            packet = makePacket(expectedNum - 1)
            socket.sendto(packet, addr)
    file.close()

#To run
bufferSize = 1024
host = socket.gethostname()
server = '142.66.140.52'
port = 8000
if __name__ == '__main__':
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # socket.bind(host, port)
    server = estConnection(port, server)
    filename = sys.argv[0]
    receive(socket, filename)

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#host = socket.gethostname()
#port = 8000
#server= "142.66.140.56"#"142.66.140.48"
#data = estConnection(port, server)

#while data:
#    data, addr = sock.recvfrom(1024) #recieve array
#    print("recieving: {} from {}".format(data,addr))
    #send 3
    # ack = 0
    # sock.sendto(bytes(ack),(server, port))
    # ack += 1
#    closed = disconnection(data, sock,addr)
#    if closed:
#        break
