import socket


class ServerView:

    # Отправка сообщение клиенту
    @staticmethod
    def send_response(client_socket, message):
        client_socket.send(message.encode('utf-8'))

    # Подтверждение подключения
    @staticmethod
    def send_confirmation(client_socket):
        client_socket.send(b"OK")

    # Получение имени файла от клиента
    @staticmethod
    def receive_filename(client_socket):
        return client_socket.recv(1024).decode('utf-8').strip()

    # Получение содержимого файла
    @staticmethod
    def receive_file_data(client_socket):
        file_data = b''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_data += data
        return file_data


class ClientView:

    # Запрос ввода пути к файлу
    @staticmethod
    def get_file_path():
        return input("Введите путь к файлу: ")

    # Вывод результата анализа
    @staticmethod
    def display_analysis_result(result):
        print("Результат анализа:\n", result)

    # Вывод ошибки
    @staticmethod
    def display_error(error):
        print(f"Ошибка: {error}")


class NetworkView:

    # Создание серверного сокета
    @staticmethod
    def create_server_socket(host='0.0.0.0', port=12345):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        return server_socket
    # Создание клиентского сокета и подключение к серверу
    @staticmethod
    def create_client_socket(host='127.0.0.1', port=12345):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket
    # Входящее подключение
    @staticmethod
    def accept_connection(server_socket):
        return server_socket.accept()