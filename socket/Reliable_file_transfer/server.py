
import socket
import struct
import time
import hashlib

HOST = '127.0.0.1'
PORT = 5001
BUFFER_SIZE = 1024

OUTPUT_FILE = "received_file.bin"

# Simulate dropping the first ACK for packet 2
DROP_ACK_FOR_SEQ = 2


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.bind((HOST, PORT))

    print("UDP Server waiting for client...")

    expected_seq = 1
    dropped_ack = False
    received_hash = hashlib.sha256()

    with open(OUTPUT_FILE, "wb") as f:

        while True:

            packet, client_addr = server.recvfrom(BUFFER_SIZE + 5)

            seq, flag = struct.unpack('!IB', packet[:5])
            data = packet[5:]

            # End of file packet
            if flag == 1:

                if seq == expected_seq:
                    print("Received END packet")

                server.sendto(struct.pack('!I', seq), client_addr)
                print("Sent ACK", seq)

                break

            # New packet
            if seq == expected_seq:

                f.write(data)
                received_hash.update(data)

                print("Received packet:", seq)

                expected_seq += 1

                # Simulate loss of first ACK for packet 2
                if seq == DROP_ACK_FOR_SEQ and not dropped_ack:

                    print("SIMULATED: ACK", seq, "DROPPED")

                    dropped_ack = True
                    continue

                server.sendto(struct.pack('!I', seq), client_addr)

                print("Sent ACK:", seq)

            # Duplicate packet
            elif seq < expected_seq:

                print("Duplicate packet detected:", seq)

                server.sendto(struct.pack('!I', seq), client_addr)

                print("Re-sent ACK:", seq)

            # Unexpected future packet
            else:

                print("Out-of-order packet:", seq)

                server.sendto(
                    struct.pack('!I', expected_seq - 1),
                    client_addr
                )

    print("\nFile received successfully!")

    print("Received SHA-256:", received_hash.hexdigest())

    server.close()


if __name__ == "__main__":
    main()
