import socket

PORT_NO = 50500

try:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server_sock.bind(('', PORT_NO))
    server_sock.listen(8)
    print('waiting for connection...')
    client_sock, (client_addr, client_port) = server_sock.accept()

    client_sock.shutdown()
except OSError as oserr:
    print(oserr)