
import socket
import struct
import hashlib
import os

HOST = '127.0.0.1'
PORT = 5001

BUFFER_SIZE = 1024
TIMEOUT = 2
MAX_RETRIES = 10


def send_packet(sock, packet, seq):

    retries = 0

    while retries < MAX_RETRIES:

        sock.sendto(packet, (HOST, PORT))

        print("Sent packet:", seq)

        try:

            ack_data, _ = sock.recvfrom(4)

            ack = struct.unpack('!I', ack_data)[0]

            if ack == seq:

                print("Received ACK:", ack)

                return True

            else:

                print("Unexpected ACK:", ack)

        except socket.timeout:

            print("Timeout! Retransmitting packet:", seq)

        retries += 1

    print("Maximum retries reached for packet:", seq)

    return False


def main():

    filename = input("Enter file path: ")

    if not os.path.isfile(filename):

        print("File not found!")

        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(TIMEOUT)

    seq = 1

    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:

        while True:

            data = f.read(BUFFER_SIZE)

            if not data:
                break

            sha256.update(data)

            # Header: sequence number + data flag
            header = struct.pack('!IB', seq, 0)

            packet = header + data

            success = send_packet(sock, packet, seq)

            if not success:

                print("Transfer failed!")

                sock.close()

                return

            seq += 1

    # Send END packet
    end_packet = struct.pack('!IB', seq, 1)

    success = send_packet(sock, end_packet, seq)

    if success:

        print("\nFile transfer completed!")

        print("Original SHA-256:", sha256.hexdigest())

    else:

        print("Final acknowledgement not received!")

    sock.close()


if __name__ == "__main__":
    main()
