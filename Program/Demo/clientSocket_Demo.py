'''
socket client demo program.
'''

import socket
import sys

HOST, PORT = '127.0.0.1', 12640
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")
    print ("Sent:     {}".format(data))
	
    # Receive data from the server and shut down
    try:
        while True:
            if sock != None:
                received = sock.recv(1024)
                if len(received):
                    print ("Received: {}".format(received))
            else:
                break
                
    except:
        print('error')
finally:
    sock.close()

