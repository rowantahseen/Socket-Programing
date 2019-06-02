import socket
import os
import sys
from _thread import *

HOST = '127.0.0.1'
PORT = 65432
buffer_size = 2048

while True:
    message = input() + '\r\n'
    request = message.split(' ')
    method, url, version = request[0], request[1], request[2]
    message += '\r\n'

    if method == 'POST':
        f = open(url[1:], "r")
        reply = f.read()
        message += reply

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message.encode())
    #print("here")
    result = s.recv(buffer_size).decode('utf-8')
    response = result.split('\r\n')
    response_message, response_data = response[0], response[-1]
    print(response_message)
    if method == 'GET':
        f = open(url[1:], 'w')
        f.write(response_data)
        f.close()
    s.close()