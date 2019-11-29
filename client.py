import socket
import threading
import struct

def conError():
    print ("connection error")
    s.close()

def estConnection(port, host):
    address = (host,port)
    #send 1
    sent = sock.sendto(b'10', address)
    print("sending {} bytes to {} ".format(sent,address))
    #receive 1
    data, addr = sock.recvfrom(1024)
    if data:
        print ("data received: ", data)
        #send 2
        sent = sock.sendto(b'ack', address)
        print("sending {} to {}".format(sent, address))
        print("connection established")
        return data
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


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
port = 8000
server= "142.66.140.56"#"142.66.140.48"
data = estConnection(port, server)

while data:
    data, addr = sock.recvfrom(1024) #recieve array
    print("recieving: {} from {}".format(data,addr))
    #send 3
    # ack = 0
    # sock.sendto(bytes(ack),(server, port))
    # ack += 1
    closed = disconnection(data, sock,addr)
    if closed:
        break
