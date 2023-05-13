# ChunkDownloadder.py
import json
import os
import socket
import time

import ChunkUploader

output_directory = 'downloads'


def download_chunks(content_name, content_dict):
    chunknames = [content_name + '_' + str(i + 1) for i in range(5)]
    total_chunks = len(chunknames)

    for i, chunkname in enumerate(chunknames):
        if chunkname in content_dict:
            peers = []
            for ip_address in content_dict[chunkname]:
                try:
                    with socket.create_connection((ip_address, ChunkUploader.PORT)) as sock:
                        message = json.dumps({"requested-content": chunkname})
                        sock.sendall(message.encode())

                        with open(chunkname, 'wb') as file:
                            while True:
                                data = sock.recv(1024)
                                if not data:
                                    break
                                file.write(data)

                        print(f"\nDownloaded {chunkname} from {ip_address}")
                        progress = (i + 1) / total_chunks
                        progress_percentage = int(progress * 100)
                        progress_bar = '=' * int(progress * 50)  # 50 units of progress bar

                        print(f"\r[{progress_bar:<50}] {progress_percentage}%", end='\t')

                        # Add connected peers to list
                        message = json.dumps({"requested-peers": chunkname})
                        sock.sendall(message.encode())
                        data = sock.recv(1024)
                        if data:
                            peers += json.loads(data.decode())["peers"]

                        break
                except Exception as e:
                    print(f"\nFailed to download {chunkname} from {ip_address} due to {str(e)}")
            # Update the progress bar

            # Use PEX to download from other clients
            for peer in peers:
                try:
                    with socket.create_connection((peer, ChunkUploader.PORT)) as sock:
                        message = json.dumps({"requested-content": chunkname})
                        sock.sendall(message.encode())

                        with open(chunkname, 'wb') as file:
                            while True:
                                data = sock.recv(1024)
                                if not data:
                                    break
                                file.write(data)

                        print(f"\nDownloaded {chunkname} from {peer}")
                        break
                except Exception as e:
                    print(f"\nFailed to download {chunkname} from {peer} due to {str(e)}")
        print()  # Newline after each chunk

    print()  # Newline at the end of the progress bar


def delete_chunks(content_name):
    files = os.listdir('.')
    for file in files:
        if file.startswith(content_name + '_'):
            os.remove(os.path.join('.', file))


def combine_chunks(content_name):
    chunknames = [content_name + '_' + str(i + 1) for i in range(5)]
    with open(os.path.join(output_directory, content_name + '.png'), 'wb') as outfile:
        for chunk in chunknames:
            with open(chunk, 'rb') as infile:
                outfile.write(infile.read())
    delete_chunks(content_name)
    print(f'Combined Chunks into: {content_name}.png')


if __name__ == "__main__":
    # Load content dictionary from a file
    with open("content_dict.json", "r") as file:
        content_dict = json.load(file)

    # Ask the user for the file to download
    content_name = input("Enter the name of the file to download: ")

    # Download chunks
    download_chunks(content_name, content_dict)

    # Combine chunks
    combine_chunks(content_name)
