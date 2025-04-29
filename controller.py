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