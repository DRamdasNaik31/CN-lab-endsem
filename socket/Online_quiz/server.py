import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 5001

questions = [
    {
        "question": "Which language is used for web development?",
        "options": ["1. Python", "2. HTML", "3. C", "4. Java"],
        "answer": "2"
    },
    {
        "question": "What is the capital of India?",
        "options": ["1. Mumbai", "2. Chennai", "3. New Delhi", "4. Kolkata"],
        "answer": "3"
    },
    {
        "question": "Which data structure uses FIFO?",
        "options": ["1. Stack", "2. Queue", "3. Tree", "4. Graph"],
        "answer": "2"
    },
    {
        "question": "Which protocol is connection-oriented?",
        "options": ["1. UDP", "2. IP", "3. TCP", "4. HTTP"],
        "answer": "3"
    },
    {
        "question": "Which company developed Python?",
        "options": ["1. Microsoft", "2. Google", "3. Apple", "4. Python Software Foundation"],
        "answer": "4"
    }
]


def send_data(conn, data):
    message = json.dumps(data).encode()
    conn.sendall(len(message).to_bytes(4, "big") + message)


def receive_exact(conn, size):
    data = b""

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Client disconnected")

        data += chunk

    return data


def receive_data(conn):
    length = int.from_bytes(receive_exact(conn, 4), "big")
    data = receive_exact(conn, length)
    return json.loads(data.decode())


def handle_client(conn, address):
    score = 0
    total = len(questions)

    print("Client connected:", address)

    try:
        send_data(conn, {
            "type": "welcome",
            "total": total
        })

        for i, q in enumerate(questions):

            # Send question without correct answer
            send_data(conn, {
                "type": "question",
                "number": i + 1,
                "total": total,
                "question": q["question"],
                "options": q["options"]
            })

            # Receive client's answer
            response = receive_data(conn)
            answer = response.get("answer", "")

            if answer in ["1", "2", "3", "4"]:
                if answer == q["answer"]:
                    score += 1
                    result = "Correct answer!"
                else:
                    result = "Wrong answer!"
            else:
                result = "Invalid answer!"

            send_data(conn, {
                "type": "result",
                "message": result,
                "score": score
            })

        # Send final score
        send_data(conn, {
            "type": "final",
            "score": score,
            "total": total
        })

        print(f"Client {address} scored {score}/{total}")

    except (ConnectionError, json.JSONDecodeError, OSError) as e:
        print(f"Client {address} disconnected or encountered an error: {e}")

    finally:
        conn.close()
        print("Connection closed:", address)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(10)

print("Quiz server started...")
print(f"Listening on {HOST}:{PORT}")

while True:
    conn, address = server.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(conn, address)
    )

    client_thread.start()
    