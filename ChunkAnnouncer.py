import os
import math
import socket
import json
import time


def chunk_file(content_name, filename):
    c = os.path.getsize(filename)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)

    index = 1
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = content_name + '_' + str(index)
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
    chunk_file.close()


def broadcast_files(content_name):
    # Get the list of files in the current directory
    files = os.listdir('.')
    matching_files = [file for file in files if file.startswith(content_name+'_')]


    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5001)  # Change this to your broadcast IP address and port
    try:
        while True:
            # Send data
            message = json.dumps({"chunks": matching_files})
            sock.sendto(message.encode(), server_address)
            print(f"Broadcasted files: {matching_files}")

            # Wait
            time.sleep(10)
    finally:
        sock.close()


if __name__ == "__main__":
    # Ask the user for the file to host
    content_name = input("Enter the name of the file to host: ")
    filename = content_name + '.png'
    chunk_file(content_name, filename)

    # Start broadcasting
    broadcast_files(content_name)
