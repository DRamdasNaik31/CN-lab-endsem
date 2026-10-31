
import socket
import hashlib
import struct
import os

HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 4096


def receive_exact(conn, size):
    data = b''

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection lost")

        data += chunk

    return data


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen(1)

    print("Server listening on port", PORT)

    conn, addr = server.accept()

    print("Connected by:", addr)

    with conn:

        # Receive filename length
        name_length = struct.unpack('!H', receive_exact(conn, 2))[0]

        # Receive filename
        filename = receive_exact(conn, name_length).decode()

        filename = os.path.basename(filename)

        # Receive file size
        file_size = struct.unpack('!Q', receive_exact(conn, 8))[0]

        # Receive client's SHA-256 checksum
        client_hash = receive_exact(conn, 32).hex()

        print("Receiving file:", filename)
        print("File size:", file_size, "bytes")

        received = 0
        sha256 = hashlib.sha256()

        with open("received_" + filename, "wb") as f:

            while received < file_size:

                chunk = conn.recv(min(BUFFER_SIZE, file_size - received))

                if not chunk:
                    raise ConnectionError("File transfer interrupted")

                f.write(chunk)

                sha256.update(chunk)

                received += len(chunk)

        server_hash = sha256.hexdigest()

        print("\nFile received successfully!")

        print("Client SHA-256:", client_hash)
        print("Server SHA-256:", server_hash)

        if client_hash == server_hash:
            print("\nINTEGRITY CHECK PASSED")
        else:
            print("\nINTEGRITY CHECK FAILED")

    server.close()


if __name__ == "__main__":
    main()
