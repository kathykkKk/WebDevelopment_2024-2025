import socket

HOST = '127.0.0.1'
PORT = 65432

def request_data_positive(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Ошибка: число должно быть положительным.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите число, пожалуйста.")

def request_data_any(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число, пожалуйста.")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            print("\nВыберите операцию:")
            print("1       | Теорема Пифагора")
            print("2       | Решение квадратного уравнения")
            print("3       | Площадь трапеции")
            print("4       | Площадь параллелограмма")
            print("'exit'  | Выход")

            choice = input("Введите номер операции или 'exit' для выхода: ").strip()

            try:
                s.sendall(choice.encode())
            except Exception:
                print("Соединение с сервером прервано. Завершение работы.")
                break

            if choice == 'exit':
                print("Отключение от сервера...")
                break

            if choice == '1':
                a = request_data_positive("Введите катет a: ")
                b = request_data_positive("Введите катет b: ")
                params = f"{a} {b}"
            elif choice == '2':
                a = request_data_any("Введите коэффициент a: ")
                b = request_data_any("Введите коэффициент b: ")
                c = request_data_any("Введите коэффициент c: ")
                params = f"{a} {b} {c}"
            elif choice == '3':
                a = request_data_positive("Введите основание a: ")
                b = request_data_positive("Введите основание b: ")
                h = request_data_positive("Введите высоту h: ")
                params = f"{a} {b} {h}"
            elif choice == '4':
                base = request_data_positive("Введите основание: ")
                height = request_data_positive("Введите высоту: ")
                params = f"{base} {height}"
            else:
                print("Некорректный выбор, попробуйте снова.")
                continue

            try:
                s.sendall(params.encode())
            except Exception:
                print("Ошибка при отправке данных. Сервер недоступен.")
                break

            try:
                data = s.recv(1024)
                if not data:
                    print("Сервер закрыл соединение.")
                    break

                response = data.decode()

                print(f"Результат: {response}")
            except Exception:
                print("Ошибка при получении ответа от сервера.")
                break

except ConnectionRefusedError:
    print("Не удалось подключиться к серверу. Убедитесь, что он запущен.")
