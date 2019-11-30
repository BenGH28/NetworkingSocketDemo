import socket
import struct
import time

def conError():
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
            print("trying to receive")
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

def disconnection(data, soc, addr):
    count = 0
    try:
        if data == b'close':
            while count < 3:
                try:
                    soc.sendto(b'terminated', (server, port))
                    count = 3
                except:
                    count += 1
            count = 0
            while count < 3:
                try:
                    d, addr = soc.recvfrom(1024)
                    count = 3
                except:
                    count += 1
            if d == b'okay':
                print("Connection gracefully terminated")
                return True
        return False
    except:
        pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
host = socket.gethostname()
port = 8000
data = None
# server = "142.66.140.47"
try:
    server= input("Enter the IP address of the server to connect to: ")
    data = estConnection(port, server)
except:
    print("Not an active server address. Connection aborted.")

while data is not None:
    try:
        data, addr = sock.recvfrom(1024) #recieve array
        print("receiving: {} from {}".format(data,addr))
        # ack = 0
        # sock.sendto(bytes(ack),(server, port))
        # ack += 1
        closed = disconnection(data, sock,addr)
        if closed:
            break
    except:
        print("this didn't receive array")
        break;
