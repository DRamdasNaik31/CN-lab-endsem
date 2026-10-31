
import socket
import hashlib
import struct
import os

HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 4096


def main():

    filename = input("Enter file path: ")

    if not os.path.isfile(filename):
        print("File not found!")
        return

    filesize = os.path.getsize(filename)

    # Calculate original file SHA-256
    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:

        while True:
            chunk = f.read(BUFFER_SIZE)

            if not chunk:
                break

            sha256.update(chunk)

    client_hash = sha256.digest()

    basename = os.path.basename(filename)
    name_bytes = basename.encode()

    # Connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    print("Connected to server")

    # Send filename length
    client.sendall(struct.pack('!H', len(name_bytes)))

    # Send filename
    client.sendall(name_bytes)

    # Send file size
    client.sendall(struct.pack('!Q', filesize))

    # Send SHA-256 checksum
    client.sendall(client_hash)

    # Send file contents
    with open(filename, "rb") as f:

        while True:
            chunk = f.read(BUFFER_SIZE)

            if not chunk:
                break

            client.sendall(chunk)

    print("File sent successfully!")
    print("Original SHA-256:", client_hash.hex())

    client.close()


if __name__ == "__main__":
    main()
