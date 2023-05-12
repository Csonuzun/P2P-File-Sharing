import socket
import json


def discover_content():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('localhost', 5001)  # Change this to your listening IP address and port
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
            content_dict[chunk].append(address[0])

        print(f"Content dictionary: {content_dict}")
        with open("content_dict.json", "w") as file:
            json.dump(content_dict, file)


if __name__ == "__main__":
    discover_content()
