import socket
import json
import os
import hashlib
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096

os.makedirs("server_files", exist_ok=True)


def send_message(conn, data):
    message = json.dumps(data).encode()
    conn.sendall(len(message).to_bytes(4, "big") + message)


def receive_exact(conn, size):
    data = b""

    while len(data) < size:
        chunk = conn.recv(min(BUFFER_SIZE, size - len(data)))

        if not chunk:
            raise ConnectionError("Client disconnected")

        data += chunk

    return data


def receive_message(conn):
    length = int.from_bytes(receive_exact(conn, 4), "big")
    data = receive_exact(conn, length)
    return json.loads(data.decode())


def calculator(request):
    a = float(request["num1"])
    b = float(request["num2"])
    op = request["operation"]

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return "Invalid operation"

    return str(result)


def string_operations(request):
    text = request["text"]
    op = request["operation"]

    if op == "1":
        return text[::-1]

    elif op == "2":
        return text.upper()

    elif op == "3":
        cleaned = "".join(c.lower() for c in text if c.isalnum())
        return "Palindrome" if cleaned == cleaned[::-1] else "Not a palindrome"

    return "Invalid string operation"


def receive_file(conn, request):
    filename = os.path.basename(request["filename"])
    size = int(request["size"])

    if size < 0:
        raise ValueError("Invalid file size")

    filepath = os.path.join("server_files", filename)

    remaining = size

    with open(filepath, "wb") as f:
        while remaining > 0:
            chunk = conn.recv(min(BUFFER_SIZE, remaining))

            if not chunk:
                raise ConnectionError("File transfer interrupted")

            f.write(chunk)
            remaining -= len(chunk)

    return f"File uploaded successfully: {filename}"


def send_file(conn, request):
    filename = os.path.basename(request["filename"])
    filepath = os.path.join("server_files", filename)

    if not os.path.isfile(filepath):
        send_message(conn, {
            "status": "error",
            "message": "File not found on server"
        })
        return

    size = os.path.getsize(filepath)

    send_message(conn, {
        "status": "ok",
        "filename": filename,
        "size": size
    })

    with open(filepath, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)

            if not data:
                break

            conn.sendall(data)


def handle_client(conn, address):
    print("Connected:", address)

    try:
        while True:
            request = receive_message(conn)
            service = request.get("service")

            if service == "1":
                result = calculator(request)
                send_message(conn, {"status": "ok", "result": result})

            elif service == "2":
                result = string_operations(request)
                send_message(conn, {"status": "ok", "result": result})

            elif service == "3":
                operation = request.get("operation")

                if operation == "upload":
                    result = receive_file(conn, request)
                    send_message(conn, {"status": "ok", "result": result})

                elif operation == "download":
                    send_file(conn, request)

                else:
                    send_message(conn, {
                        "status": "error",
                        "message": "Invalid file operation"
                    })

            elif service == "4":
                current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                send_message(conn, {
                    "status": "ok",
                    "result": current_time
                })

            elif service == "0":
                break

            else:
                send_message(conn, {
                    "status": "error",
                    "message": "Invalid menu choice"
                })

    except (ConnectionError, json.JSONDecodeError, KeyError, ValueError) as e:
        print("Client error:", e)

    finally:
        conn.close()
        print("Disconnected:", address)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, address = server.accept()
    handle_client(conn, address)