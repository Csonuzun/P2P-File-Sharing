import socket
import time
import json

def divide_file(file_path):
    # Implement file division using the provided code.

def broadcast_chunks(chunk_list):
    broadcast_ip = '255.255.255.255'
    broadcast_port = 5001

    # AF_INET "IPV4" protokolü anlamına gelmektedir
    # type parametresi soketin stream tabanlı mı, yoksa datagram tabanlı mı olduğunu belirtir. TCP uygulamaları için bu
    # parametresinin sock.SOCK_STREAM biçiminde UDP için ise sock.SOCK_DGRAM biçiminde girilmesi gerekmektedir.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = json.dumps({"chunks": chunk_list})

    while True:
        sock.sendto(message.encode('utf-8'), (broadcast_ip, broadcast_port))
        time.sleep(60)

def run():
    file_path = input("Enter the file path: ")
    chunk_list = divide_file(file_path)
    broadcast_chunks(chunk_list)
