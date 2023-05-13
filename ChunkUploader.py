# ChunkUploader.py
import json
import os

PORT = 5000

import socket


def check_port_in_use(port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Try to bind the socket to the specified port
        sock.bind(("localhost", port))
        # Port is available
        return False
    except socket.error as e:
        if e.errno == 98 or e.errno == 48:  # Error codes for port already in use
            # Port is already in use
            return True
        else:
            # An error occurred
            print("An error occurred while checking port:", e)
            return False
    finally:
        sock.close()


def get_local_ip():
    # The SOCK_DGRAM argument means this is a UDP type socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't matter if you can't connect to this address, this method
        # is used to get the preferred outbound IP address
        sock.connect(('10.255.255.255', 1))
        local_ip = sock.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        sock.close()
    return local_ip


def start_server():
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((get_local_ip(), PORT))
        s.listen()
        print("waiting for connection...")
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                request = json.loads(data.decode())
                chunkname = request["requested-content"]

                with open(os.path.join('media', chunkname), 'rb') as file:
                    conn.sendall(file.read())


if __name__ == "__main__":
    print(f'local ip is {get_local_ip()}')
    # Call the function to check if port 5000 is in use
    port_in_use = check_port_in_use(5000)

    if port_in_use:
        print("Port 5000 is already in use by another program.")
    else:
        print("Port 5000 is available.")
    print("Server Starting...")
    start_server()
