#!/usr/bin/env python

import socket
import select
from time import gmtime, strftime
import random
from random import randint

base = "image_copy%s.png"
imgcnt = 1
clients = []

new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
new_socket.bind(('127.0.0.1', 8808)) # host and port
new_socket.listen(10)

clients.append(new_socket)
buff_len = 4096

while True:

    rs, ws, es = select.select(clients, [], []) # read, write and error sockets, respectly

    for s in rs: # list all reading sockets

        if s == new_socket:

            sock_fd, incoming_address = new_socket.accept()
            clients.append(sock_fd)

        else:
            try:
                print ("Buffer length: " + str(buff_len))
                data = s.recv(buff_len)
                text = str(data)

                if text.startswith('LENGTH'):
                    msg = text.split()
                    size = int(msg[1])

                    print ("lenght recived")
                    print ("length: ", size)

                    s.send("LENGTH RECIVED")
                    buff_len = 40960000

                elif text.startswith('END'):
                    s.shutdown()

                elif data:

                    file = open(base % imgcnt, 'wb')

                    if not data:
                        file.close()
                        break
                    file.write(data)
                    file.close()

                    s.send("DOCUMENT RECIVED")
                    buff_len = 4096
                    s.shutdown()
            except:
                s.close()
                clients.remove(s)
                continue
        imgcnt += 1
new_socket.close()
