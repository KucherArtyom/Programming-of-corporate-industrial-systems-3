import threading
from controller import ServerController
from view import ServerView, NetworkView


class FileAnalysisServer:
    def __init__(self):
        self.controller = ServerController()
        self.view = ServerView()
        self.network = NetworkView()

    def handle_client(self, client_socket, addr):
        print(f"Подключен клиент: {addr}")
        try:
            filename = self.view.receive_filename(client_socket)
            if not filename:
                raise ValueError("Имя файла не получено")

            self.view.send_confirmation(client_socket)
            file_data = self.view.receive_file_data(client_socket)
            result = self.controller.process_file(filename, file_data)
            self.view.send_response(client_socket, str(result))

        except Exception as e:
            print(f"Ошибка: {e}")
            self.view.send_response(client_socket, f"Ошибка: {e}")
        finally:
            client_socket.close()

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