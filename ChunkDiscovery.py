#ChunkDiscovery.py
import socket
import json

def discover_content():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 5001)  # Bind to all available network interfaces
    sock.bind(server_address)

    content_dict = {}

    while True:
        print('\nWaiting to receive message')
        data, address = sock.recvfrom(4096)

        data = json.loads(data.decode())
        print(f"Received data: {data} from {address}")

        for chunk in data["chunks"]:
            if chunk not in content_dict:
                content_dict[chunk] = []
            if address[0] not in content_dict[chunk]:
                content_dict[chunk].append(address[0])

        print(f"Content dictionary: {content_dict}")
        with open("content_dict.json", "w") as file:
            json.dump(content_dict, file)


if __name__ == "__main__":
    discover_content()
