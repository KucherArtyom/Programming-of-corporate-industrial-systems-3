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