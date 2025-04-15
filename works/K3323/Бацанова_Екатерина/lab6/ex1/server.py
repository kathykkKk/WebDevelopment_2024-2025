import socket

HOST = '127.0.0.1'
PORT = 65432
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("Сервер запущен, ожидаем соединения...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Подключен клиент: {addr}")
                data = conn.recv(1024)
                print(f"Получено сообщение от клиента: {data.decode()}")

                response = "Hello, client"
                conn.sendall(response.encode())

except KeyboardInterrupt:
    print("\nСервер остановлен пользователем (Ctrl+C)")

