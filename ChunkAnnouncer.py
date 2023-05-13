import json
import math
import os
import socket
import time

directory = "media"


def chunk_file(content_name):
    full_path = os.path.join(os.getcwd(), directory, content_name + '.png')
    c = os.path.getsize(full_path)
    CHUNK_SIZE = math.ceil(c / 5)
    index = 1
    with open(full_path, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = os.path.join(directory, content_name + '_' + str(index))
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)

            index += 1
            chunk = infile.read(int(CHUNK_SIZE))


def broadcast_files(matching_files):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.1.255', 5001)
    try:
        while True:
            message = json.dumps({"chunks": matching_files})
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(message.encode(), server_address)
            print(f"Broadcasted files: {matching_files}")
            time.sleep(60)
    finally:
        sock.close()


def get_matching_files(content_names):
    files = os.listdir(directory)
    result = []
    for content_name in content_names:
        for file in files:
            if file.startswith(content_name + '_'):
                result.append(file)
    return result


def get_png_files():
    files = os.listdir(directory)
    return [file for file in files if file.endswith('.png')]


if __name__ == "__main__":
    png_files = get_png_files()
    content_names = []
    for png_file in png_files:
        content_name, _ = os.path.splitext(png_file)
        content_names.append(content_name)
        chunk_file(content_name)
    print(f'image files {content_names}')
    broadcast_files(get_matching_files(content_names))
