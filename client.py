import socket
import threading

def conError():
    print ("connection error")
    s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostname()
port = 8000
server= "142.66.140.47"#"142.66.140.48"
s.connect((server, port))

s.sendto(b'Hello World', (server, port))
timer = threading.Timer(5.0, conError)
timer.start()
data, addr = s.recvfrom(1024)
if data == "Hello Universe":
    print ("Message: ", data)
    s.sendto(b'Message Received', (server, port))
    data, addr = s.recvfrom(1024)
    s.sendto(b'0', (server, port))
    print (data)
