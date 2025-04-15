import socket
import os

HOST = '127.0.0.1'
PORT = 65432

def read_file(filename, content_type):
    if not os.path.exists(filename):
        return f"""HTTP/1.1 404 Not Found\r
Content-Type: text/html\r
\r
<h1>Файл {filename} не найден</h1>
""".encode()

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    return f"""HTTP/1.1 200 OK\r
Content-Type: {content_type}; charset=UTF-8\r
\r
{content}
""".encode()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Сервер запущен на {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Подключен клиент: {addr}")
                request = conn.recv(1024).decode()
                print(f"Запрос от клиента:\n{request}")
                if not request:
                    continue
                request_line = request.splitlines()[0]
                path = request_line.split(" ")[1]

                if path == "/" or path == "/index.html":
                    response = read_file("index.html", "text/html")
                elif path == "/style.css":
                    response = read_file("style.css", "text/css")
                else:
                    response = f"""HTTP/1.1 404 Not Found\r
    Content-Type: text/html\r
    \r
    <h1>404 - Не найдено</h1>""".encode()

                conn.sendall(response)

except KeyboardInterrupt:
    print("\nСервер остановлен пользователем (Ctrl+C)")


