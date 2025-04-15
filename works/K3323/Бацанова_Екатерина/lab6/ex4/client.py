import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                continue

            if message.startswith("Сервер завершает работу"):
                print("Сервер завершил свою работу. Вы отключены.")
                client.close()
                break

            print(message)
        except:
            print("Вы потеряли соединение с сервером.")
            client.close()
            break
    sys.exit(0)

def send_messages(client):
    while True:
        try:
            message = input()
            if message.lower() == "exit":
                client.send("exit".encode())
                print("Вы покинули чат.")
                client.close()
                break
            client.send(message.encode())
        except:
            break
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    nickname = input("Введите свой никнейм: ")
    client.send(nickname.encode())
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

except ConnectionRefusedError:
    print("Не удалось подключиться к серверу.")
except KeyboardInterrupt:
    print("Клиент завершил работу.")



