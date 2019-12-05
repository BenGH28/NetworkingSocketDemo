import socket
import time
from timer import Timer

def fileWrite(data):
    count = 0
    file = open("file.txt", "w")
    while data is not None and count < 1:
        file.write(data)
        count += 1
    file.close()

def receive(data):
    count = 0
    file = open("file.txt", "w")
    x = 0
    dataList = []
    #seqNum = 0
    while data is not None:
        t = Timer(5)
        t.start()
        try:
            data, addr = sock.recvfrom(1024)
            #print("1")
            if data and data != b'close':
                print("Received data: ", data)
                x +=1
                text = str(data)
                if count == 0:
                    dataList.append(text)
                    count += 1
                    #print("2")
                else:
                    dataList.append(text)
                    count = 0
                    #print("3")
                #temp = str(seqNum)

                if x%3 == 0:
                    sock.sendto(b'ack', addr)
                    for a in range (len(dataList)):
                        file.write(dataList[a])
                        file.write("\n")
                    dataList.clear()

                #seqNum += 1
                #print("4")
            elif data == b'close':
                #print("6")
                print(data)
                file.close()
                sock.settimeout(None)
                #sock.close()
                return data
        except:
            if t.timeout():
                #print ("5")
                sock.sendto(b'resend', addr)
                break
        #t.stop()


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
    #try:
        if data == b'close':
            sock.sendto(b'terminated', (server, port))
            print("terminated")
            d, addr = sock.recvfrom(1024)
            if d == b'okay':
                print("Connection gracefully terminated")
                sock.close()
                return True
            else:
                print("Cant terminate")
    #except:
    #    pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.settimeout(2)
host = socket.gethostname()
port = 8000
data = None
#server = "142.66.140.355"
#try:
server = input("Enter the IP address of the server to connect to: ")
data = estConnection(port, server)
#except:
#    print("Not an active server address. Connection aborted.")

while True:
        data = receive(data)

        #data, addr = sock.recvfrom(1024) #receive array
        #print("receiving: {} from {}".format(data,addr))
        # ack = 0
        # sock.sendto(bytes(ack),(server, port))
        # ack += 1
        closed = disconnection(data, sock)
        if closed:
            break
#    except:
#        print("this didn't receive array")
#        break;
