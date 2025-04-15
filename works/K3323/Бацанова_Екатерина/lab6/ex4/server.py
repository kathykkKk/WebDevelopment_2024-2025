import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = []
nicknames = []
server_running = True

def broadcast(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                clients.remove(c)
                nicknames.remove(nicknames[clients.index(c)])

def send_private_message(sender, nickname, message):
    try:
        index = nicknames.index(nickname)
        client = clients[index]
        client.send(f"Личное сообщение от {sender}: {message}".encode())
    except ValueError:
        return None
    return True

def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode()

            if message == 'exit':
                print(f"{nickname} покинул чат.")
                client.send('Вы покинули чат.'.encode())
                broadcast(f"Пользователь {nickname} вышел из чата.".encode(), client)
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                break

            if message.startswith('@'):
                parts = message.split(' ', 1)
                if len(parts) == 2:
                    recipient_nickname = parts[0][1:]
                    private_message = parts[1]
                    if send_private_message(nickname, recipient_nickname, private_message) is None:
                        client.send(f"Ошибка: Пользователь с никнеймом {recipient_nickname} не найден.".encode())
                else:
                    client.send("Ошибка: Неверный формат личного сообщения.".encode())
            else:
                broadcast(f"{nickname}: {message}".encode(), client)
        except:
            print(f"{nickname} покинул чат (неактивность или ошибка соединения).")
            clients.remove(client)
            nicknames.remove(nickname)
            client.close()
            break

def receive():
    while server_running:
        try:
            client, address = server.accept()
            print(f"Подключен: {str(address)}")

            while True:
                client.send("Введите свой никнейм: ".encode())
                nickname = client.recv(1024).decode()

                if nickname in nicknames:
                    client.send("Ошибка: Никнейм уже занят, выберите другой.".encode())
                    continue
                else:
                    break

            clients.append(client)
            nicknames.append(nickname)

            broadcast(f'{nickname} присоединился к чату!'.encode(), client)
            client.send('Вы подключены к чату!'.encode())

            thread = threading.Thread(target=handle, args=(client, nickname))
            thread.start()

        except Exception as e:
            if server_running:
                print(f"Ошибка при принятии нового подключения: {e}")

def stop_server():
    global server_running
    server_running = False
    print("Завершаем работу сервера...")

    for client in clients[:]:
        try:
            print(f"Отправляем сообщение клиенту {client}")
            client.send("Сервер завершил свою работу. Закрытие соединения...".encode())
        except Exception as e:
            print(f"Ошибка при отправке сообщения клиенту {client}: {e}")
            pass

    # Теперь закрываем соединения с клиентами
    for client in clients[:]:
        try:
            client.close()
            clients.remove(client)
        except Exception as e:
            pass

    server.close()
    print("Сервер завершил свою работу.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Сервер запущен на {HOST}:{PORT}")

thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

while server_running:
    command = input("Введите 'shutdown' для завершения работы сервера: ")
    if command == 'shutdown':
        stop_server()
        break
