# client.py

import socket
from _socket import SHUT_RDWR

PORT_NO = 50500

try:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    client_sock.connect(('127.0.0.1', PORT_NO))
    print('connected...')
    client_sock.shutdown(SHUT_RDWR)
    client_sock.close()

except OSError as oserr:
    print(oserr)