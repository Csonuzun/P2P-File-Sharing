import socket
import json
import ChunkUploader
import time


def download_chunks(content_name, content_dict):
    chunknames = [content_name + '_' + str(i + 1) for i in range(5)]
    for chunkname in chunknames:
        if chunkname in content_dict:
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

                        print(f"Downloaded {chunkname} from {ip_address}")
                        break
                except Exception as e:
                    print(f"Failed to download {chunkname} from {ip_address} due to {str(e)}")


def combine_chunks(content_name):
    chunknames = [content_name + '_' + str(i + 1) for i in range(5)]
    with open(content_name + '.png', 'wb') as outfile:
        for chunk in chunknames:
            with open(chunk, 'rb') as infile:
                outfile.write(infile.read())


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
