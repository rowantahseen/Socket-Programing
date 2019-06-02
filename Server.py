import socket
import os
import sys
from _thread import *

#Needs to add a directory
dire = "database/"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '104.237.143.20'
PORT = 80
buffer_size = 2048

s.bind((HOST, PORT))
print('waiting for connection')


def threaded_client(conn):
    #print('entered thread')
    #conn.send(str.encode('Welcome, type your info\n'))
    message = conn.recv(buffer_size)
    #message = new_line
    #while len(new_line) > 0:
    #    new_line = conn.recv(buffer_size)
    #    message += new_line

    #print('recieved')
    string_data = message.decode('utf-8')
    #print(string_data)

    fields = string_data.split('\r\n')
    #print('fields = ', fields )
    request = fields[0].split(' ')
    #print('request = ', request)
    method, url, version = request[0], request[1], request[2]
    file_name = url[1:]

    if method == "GET":
        if file_name in os.listdir(dire):
            f = open((dire + file_name), "r")
            file = f.read()
            f.close()
            response = 'HTTP/1.0 200 OK\r\n' + '\r\n' + file
            conn.sendall(str.encode(response))
        else:
            conn.sendall(str.encode('HTTP/1.0 404 Not Found\r\n'))
    elif method == "POST":
        #print('entered "POST"')
        f = open((dire + file_name), "w")
        #print('directory = ', dire + file_name)
        f.write(fields[-1])
        f.close()
        #print('target files =', file_name)
        #print(fields)
        response = 'HTTP/1.0 200 OK\r\n' + '\r\n'
        conn.sendall(str.encode(response))
    else:
        #print('toot')
        conn.send(str.encode('Unspecified Method\r\n'))
    conn.close()

while True:
    s.listen(5)
    client_socket, client_addr = s.accept()
    print(f"Accepted new connection from {client_addr[0]}:{client_addr[1]}")
    start_new_thread(threaded_client,(client_socket,))

