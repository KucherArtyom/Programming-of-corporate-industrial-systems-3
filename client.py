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