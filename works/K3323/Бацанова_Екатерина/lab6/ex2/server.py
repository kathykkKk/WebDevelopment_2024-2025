import socket
import threading

HOST = '127.0.0.1'
PORT = 65432
client_connections = []
client_threads = []
server_running = True

def pythagorean_theorem(a, b):
    return (a**2 + b**2) ** 0.5

def solve_quadratic(a, b, c):
    d = b ** 2 - 4 * a * c
    if d > 0:
        x1 = (-b + d ** 0.5) / (2 * a)
        x2 = (-b - d ** 0.5) / (2 * a)
        return f"Корни уравнения: x1 = {x1}, x2 = {x2}"
    elif d == 0:
        x = -b / (2 * a)
        return f"Один корень: x = {x}"
    else:
        return "Корней нет"

def trapezoid_area(a, b, h):
    return 0.5 * (a + b) * h

def parallelogram_area(base, height):
    return base * height

def validate_positive(value):
    return value > 0

def handle_client(conn, addr):
    print(f"Подключен клиент: {addr}")
    client_connections.append(conn)
    try:
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    request = data.decode()
                    if request == 'exit':
                        print(f"Клиент {addr} отправил 'exit'.")
                        break
                    params = conn.recv(1024).decode().split()
                    try:
                        if request == '1':
                            a, b = map(float, params)
                            if validate_positive(a) and validate_positive(b):
                                result = pythagorean_theorem(a, b)
                            else:
                                result = "Ошибка: параметры должны быть положительными."
                        elif request == '2':
                            a, b, c = map(float, params)
                            result = solve_quadratic(a, b, c)
                        elif request == '3':
                            a, b, h = map(float, params)
                            if all(map(validate_positive, [a, b, h])):
                                result = trapezoid_area(a, b, h)
                            else:
                                result = "Ошибка: параметры должны быть положительными."
                        elif request == '4':
                            base, height = map(float, params)
                            if validate_positive(base) and validate_positive(height):
                                result = parallelogram_area(base, height)
                            else:
                                result = "Ошибка: параметры должны быть положительными."
                        else:
                            result = "Неизвестная команда."
                    except (ValueError, IndexError):
                        result = "Ошибка: некорректный ввод."
                    conn.sendall(str(result).encode())
                except (ConnectionResetError, BrokenPipeError):
                    print(f"Клиент {addr} разорвал соединение.")
                    break
                except OSError:
                    # сокет закрыт сервером — завершение
                    break
    except Exception as e:
        print(f"Ошибка в потоке клиента {addr}: {e}")
    finally:
        if conn in client_connections:
            client_connections.remove(conn)
        print(f"Клиент {addr} отключен.")

def server_main():
    global server_running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1.0)
        print("Сервер запущен, ожидаем соединений...")

        while server_running:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
                client_threads.append(thread)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Ошибка сервера: {e}")
                break

        print("Сервер завершает работу, отключаем клиентов...")

        for client in client_connections[:]:
            try:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            except Exception as e:
                print(f"Ошибка при отключении клиента: {e}")

        for thread in client_threads:
            thread.join()

        print("Сервер завершён.")

server_thread = threading.Thread(target=server_main)
server_thread.start()

while True:
    command = input("Введите 'shutdown' для остановки сервера: ").strip().lower()
    if command == 'shutdown':
        server_running = False
        server_thread.join()
        break
