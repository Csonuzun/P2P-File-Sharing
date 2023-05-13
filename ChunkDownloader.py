# ChunkDownloadder.py
import os
import socket
import json
import ChunkUploader
import time

output_directory = 'downloads'


def download_chunks(content_name, content_dict):
    chunknames = [content_name + '_' + str(i + 1) for i in range(5)]
    total_chunks = len(chunknames)

    # Display 0% progress at the start
    print(f"\r[{' ':<50}] 0%", end='\t')

    for i, chunkname in enumerate(chunknames):
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

                        print(f"\nDownloaded {chunkname} from {ip_address}")
                        break
                except Exception as e:
                    print(f"\nFailed to download {chunkname} from {ip_address} due to {str(e)}")
        time.sleep(0.15)
        # Update the progress bar
        progress = (i + 1) / total_chunks
        progress_percentage = int(progress * 100)
        progress_bar = '=' * int(progress * 50)  # 50 units of progress bar

        print(f"\r[{progress_bar:<50}] {progress_percentage}%", end='\t')

    print()  # Newline at the end of the progress bar


def combine_chunks(content_name):
    chunknames = [content_name + '_' + str(i + 1) for i in range(5)]
    with open(os.path.join(output_directory, content_name + '.png'), 'wb') as outfile:
        for chunk in chunknames:
            with open(chunk, 'rb') as infile:
                outfile.write(infile.read())
    delete_chunks(content_name)


def delete_chunks(content_name):
    files = os.listdir(output_directory)
    for file in files:
        if file.startswith(content_name + '_'):
            os.remove(os.path.join(output_directory, file))
            print(f"Deleted chunk: {file}")


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
