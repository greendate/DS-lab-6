#!/usr/bin/env python

from time import gmtime, strftime
import random
from random import randint
import sys
import socket
import select


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8808)
server_socket.connect(server_address)

try:
    for path in sys.argv[1:]:
        file = open(path, 'rb')
        bytes = file.read()
        length = len(bytes)

        server_socket.sendall("LENGTH %s" % length) # send length to server
        ans = server_socket.recv(4096)

        print ("answer: ", ans)

        if ans == 'LENGTH RECIVED':
            server_socket.sendall(bytes)

            ans = server_socket.recv(4096)
            print ("answer: ", ans)

            if ans == 'DOCUMENT RECIVED':
                server_socket.sendall("END")
                print("IMAGE IS SENT TO SERVER")

        file.close()

finally:
    server_socket.close()
