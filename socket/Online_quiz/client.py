import socket
import json

HOST = "127.0.0.1"
PORT = 5001


def send_data(sock, data):
    message = json.dumps(data).encode()
    sock.sendall(len(message).to_bytes(4, "big") + message)


def receive_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Server disconnected")

        data += chunk

    return data


def receive_data(sock):
    length = int.from_bytes(receive_exact(sock, 4), "big")
    data = receive_exact(sock, length)
    return json.loads(data.decode())


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))

        print("Connected to Quiz Server!")

        welcome = receive_data(client)

        print("\n========== ONLINE QUIZ ==========")
        print("Total Questions:", welcome["total"])

        while True:
            data = receive_data(client)

            if data["type"] == "question":

                print("\n--------------------------------")
                print(f"Question {data['number']}/{data['total']}")
                print(data["question"])

                for option in data["options"]:
                    print(option)

                answer = input("Enter your answer (1-4): ").strip()

                send_data(client, {
                    "answer": answer
                })

                result = receive_data(client)

                print("\n" + result["message"])
                print("Current Score:", result["score"])

            elif data["type"] == "final":

                print("\n========== QUIZ COMPLETED ==========")
                print("Your Final Score:", data["score"], "/", data["total"])
                print("====================================")

                break

    except (ConnectionError, OSError, json.JSONDecodeError) as e:
        print("Connection error:", e)

    finally:
        client.close()


if __name__ == "__main__":
    main()