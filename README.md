# NetworkingSocketDemo
Our humble implementation of client/server transport layer protocol
Instructions:
1. Download all files for the repository located at https://github.com/BenGH28/NetworkingSocketDemo
2. In a console window on one computer in the folder containing the files. In the console window, type "python3 server.py" to initiate the program and await connection. This will run infintely, so it must be forcefully terminated when the server is done being used (use ctrl C)
3. On another computer, open a console window and go to the folder containing the files. In the console window, type "python3 client.py output(number)" to start the client to connect to the server. the output and number is the text file that will be saved to the folder location, defined by the user. This is used to sav various outputs that will be sent from the server.
4. Enter the IP address of the server. If you don't know the address, type "ifconfig" on the server computer before running the server, and locate it in the second text grouping where it says "inet x.x.x.x". For example:

enp0s31f6: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 142.66.140.47  netmask 255.255.254.0  broadcast 142.66.141.255
        inet6 fe80::1a66:daff:fe03:c039  prefixlen 64  scopeid 0x20<link>
        
142.66.140.47 is the IP address of this computer.

5. The connection between the two computers is now linked, and packets will begin sending
6. After the server sends all the data to the client, the connection will close and the program will terminate on the client side. The server will continue to run indefinitely until forcefully terminated. The client can now be re-run with a new number in the output file (or the same one if you want to rewrite the file).
