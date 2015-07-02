#-*- coding=utf-8 -*-

'''
socket server demo program.
'''

import os
import socket
import SocketServer

#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
	
#bind the socket to a public host, and a well-known port
serversocket.bind(("localhost", 12640))

#become a server socket
serversocket.listen(5)

while True:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
	
    #now do something with the clientsocket
    #in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)	
    ct.run()
