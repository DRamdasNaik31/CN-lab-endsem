import socket
import json
import os

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096

os.makedirs("client_files", exist_ok=True)


def send_message(sock, data):
    message = json.dumps(data).encode()
    sock.sendall(len(message).to_bytes(4, "big") + message)


def receive_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(min(BUFFER_SIZE, size - len(data)))

        if not chunk:
            raise ConnectionError("Server disconnected")

        data += chunk

    return data


def receive_message(sock):
    length = int.from_bytes(receive_exact(sock, 4), "big")
    data = receive_exact(sock, length)
    return json.loads(data.decode())


def calculator(sock):
    a = input("Enter first number: ")
    b = input("Enter second number: ")

    print("\n1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")

    choice = input("Select operation: ")

    operations = {
        "1": "+",
        "2": "-",
        "3": "*",
        "4": "/"
    }

    if choice not in operations:
        print("Invalid operation")
        return

    send_message(sock, {
        "service": "1",
        "num1": a,
        "num2": b,
        "operation": operations[choice]
    })

    response = receive_message(sock)
    print("Result:", response.get("result", response.get("message")))


def string_service(sock):
    text = input("Enter a string: ")

    print("\n1. Reverse")
    print("2. Uppercase")
    print("3. Palindrome check")

    choice = input("Select operation: ")

    if choice not in ("1", "2", "3"):
        print("Invalid operation")
        return

    send_message(sock, {
        "service": "2",
        "text": text,
        "operation": choice
    })

    response = receive_message(sock)
    print("Result:", response.get("result", response.get("message")))


def upload_file(sock):
    filename = input("Enter filename from client_files: ")
    filepath = os.path.join("client_files", os.path.basename(filename))

    if not os.path.isfile(filepath):
        print("File not found")
        return

    size = os.path.getsize(filepath)

    send_message(sock, {
        "service": "3",
        "operation": "upload",
        "filename": os.path.basename(filename),
        "size": size
    })

    with open(filepath, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)

            if not data:
                break

            sock.sendall(data)

    response = receive_message(sock)
    print(response.get("result", response.get("message")))


def download_file(sock):
    filename = input("Enter filename from server_files: ")

    send_message(sock, {
        "service": "3",
        "operation": "download",
        "filename": os.path.basename(filename)
    })

    response = receive_message(sock)

    if response["status"] != "ok":
        print(response["message"])
        return

    size = int(response["size"])
    filepath = os.path.join("client_files", response["filename"])

    remaining = size

    with open(filepath, "wb") as f:
        while remaining > 0:
            chunk = sock.recv(min(BUFFER_SIZE, remaining))

            if not chunk:
                raise ConnectionError("File transfer interrupted")

            f.write(chunk)
            remaining -= len(chunk)

    print("File downloaded successfully:", filepath)


def file_service(sock):
    print("\n1. Upload file to server")
    print("2. Download file from server")

    choice = input("Select operation: ")

    if choice == "1":
        upload_file(sock)

    elif choice == "2":
        download_file(sock)

    else:
        print("Invalid choice")


def time_service(sock):
    send_message(sock, {"service": "4"})

    response = receive_message(sock)
    print("Server date and time:", response.get("result"))


def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        print("Connected to server!")

        while True:
            print("\n========== MAIN MENU ==========")
            print("1. Calculator")
            print("2. String Operations")
            print("3. File Transfer")
            print("4. Time Service")
            print("0. Exit")
            print("===============================")

            choice = input("Enter your choice: ")

            if choice == "1":
                calculator(sock)

            elif choice == "2":
                string_service(sock)

            elif choice == "3":
                file_service(sock)

            elif choice == "4":
                time_service(sock)

            elif choice == "0":
                send_message(sock, {"service": "0"})
                print("Disconnected from server")
                break

            else:
                print("Invalid menu choice")

        sock.close()

    except (ConnectionError, OSError) as e:
        print("Connection error:", e)


if __name__ == "__main__":
    main()