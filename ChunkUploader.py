import socket
import json

PORT = 5000


def start_server():
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', PORT))  # Bind to your listening IP and port
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                request = json.loads(data.decode())
                chunkname = request["requested-content"]

                with open(chunkname, 'rb') as file:
                    conn.sendall(file.read())


if __name__ == "__main__":
    start_server()
