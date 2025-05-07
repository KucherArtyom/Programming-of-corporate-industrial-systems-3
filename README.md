# Programming-of-corporate-industrial-systems-3

## Кучер Артем Сергеевич ЭФМО-02-24

### Практика 3

### Анализатор текстовых файлов (Клиент-серверное приложение)

### Пример использования
```
server.py:
Сервер запущен и ожидает подключений...
Подключен клиент: ('127.0.0.1', 49556)

client.py:
Введите путь к файлу: D://text.txt
Результат анализа:
 Имя файла: text.txt
Строк: 1, Слов: 149, Символов: 1315

analysis_result.txt:
Имя файла: text.txt
Строк: 1, Слов: 149, Символов: 1315

Имя файла: text1.txt
Строк: 1, Слов: 25, Символов: 197

Имя файла: text.txt
Строк: 1, Слов: 149, Символов: 1315

Имя файла: text.txt
Строк: 1, Слов: 149, Символов: 1315

Имя файла: text.txt
Строк: 1, Слов: 149, Символов: 1315

Имя файла: text.txt
Строк: 1, Слов: 149, Символов: 1315
```

### Код программы
#### model.py
```
import os
from dataclasses import dataclass


@dataclass
class FileAnalysisResult:
    filename: str
    lines: int
    words: int
    chars: int

    # Вывод результатов анализа
    def __str__(self):
        return f"Имя файла: {self.filename}\nСтрок: {self.lines}, Слов: {self.words}, Символов: {self.chars}"


class FileReceiver:

    # Создание директории
    def __init__(self, save_dir="received_files"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    # Сохранение полученного файла в директории
    def save_file(self, filename, file_data):
        save_path = os.path.join(self.save_dir, f"received_{filename}")
        with open(save_path, 'wb') as file:
            file.write(file_data)
        return save_path


class FileAnalyzer:
    # Анализ файла
    @staticmethod
    def analyze(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.count('\n') + 1
            words = len(content.split())
            chars = len(content)
        return lines, words, chars


class AnalysisRepository:
    # Файл для сохранения файла
    def __init__(self, result_file="analysis_result.txt"):
        self.result_file = result_file

    # Добавление результатов анализа в файл
    def save_result(self, result: FileAnalysisResult):
        with open(self.result_file, 'a', encoding='utf-8') as f:
            f.write(f"{str(result)}\n\n")
```

#### controller.py
```
from model import FileAnalysisResult, FileReceiver, FileAnalyzer, AnalysisRepository
import os


class ServerController:
    def __init__(self):
        self.file_receiver = FileReceiver()
        self.analyzer = FileAnalyzer()
        self.repository = AnalysisRepository()

    # Анализ и сохранение результата анализа
    def process_file(self, filename, file_data):
        saved_path = self.file_receiver.save_file(filename, file_data)
        lines, words, chars = self.analyzer.analyze(saved_path)
        result = FileAnalysisResult(filename, lines, words, chars)
        self.repository.save_result(result)
        return result


class ClientController:
    def __init__(self, server_host='127.0.0.1', server_port=12345):
        self.server_host = server_host
        self.server_port = server_port

    # Чтение содержимого файла
    def send_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Файл не найден")

        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            file_data = file.read()

        return filename, file_data
```


#### view.py
```
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
```

#### server.py
```
import threading
from controller import ServerController
from view import ServerView, NetworkView


class FileAnalysisServer:
    def __init__(self):
        self.controller = ServerController()
        self.view = ServerView()
        self.network = NetworkView()

    # Обработка клиентского подключения
    def handle_client(self, client_socket, addr):
        print(f"Подключен клиент: {addr}")
        try:
            filename = self.view.receive_filename(client_socket) #Получает имя файла
            if not filename:
                raise ValueError("Имя файла не получено")

            self.view.send_confirmation(client_socket) #Отправляет подтверждение
            file_data = self.view.receive_file_data(client_socket) #Принимает данные файла
            result = self.controller.process_file(filename, file_data)
            self.view.send_response(client_socket, str(result))

        except Exception as e:
            print(f"Ошибка: {e}")
            self.view.send_response(client_socket, f"Ошибка: {e}")
        finally:
            client_socket.close()

    # Запуск сервера
    def start(self):
        server_socket = self.network.create_server_socket()
        print("Сервер запущен и ожидает подключений...")

        while True:
            client_socket, addr = self.network.accept_connection(server_socket)
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr)
            )
            client_thread.start()


if __name__ == "__main__":
    server = FileAnalysisServer()
    server.start()
```

#### client.py
```
from controller import ClientController
from view import ClientView, NetworkView
import socket


class FileAnalysisClient:
    def __init__(self):
        self.controller = ClientController()
        self.view = ClientView()
        self.network = NetworkView()

    # Основной цикл работы программы
    def run(self):
        file_path = self.view.get_file_path()

        try:
            filename, file_data = self.controller.send_file(file_path)
            client_socket = self.network.create_client_socket()

            try:
                client_socket.send(filename.encode('utf-8')) #Клиент отправляет имя файла
                confirmation = client_socket.recv(1024) #Ждет подтверждения от сервера
                if confirmation != b"OK":
                    raise ValueError("Сервер не подтвердил получение имени файла")

                client_socket.send(file_data)  #Отправляет содержимое файла
                client_socket.shutdown(socket.SHUT_WR)

                response = client_socket.recv(1024).decode('utf-8')
                self.view.display_analysis_result(response)

            finally:
                client_socket.close()

        except Exception as e:
            self.view.display_error(e)


if __name__ == "__main__":
    client = FileAnalysisClient()
    client.run()
```
