import os
from ..types.file_path import FilePath


class FormattedFileGenerator:
    def __init__(
        self, output_base_path: str, formatted_files: list[tuple[FilePath, list[str]]]
    ):
        self.__output_base_path = output_base_path
        self.__formatted_files = formatted_files

    def generate(self):
        for file_path, formatted_lines in self.__formatted_files:
            self.__write_formatted_file(file_path.relative_path, formatted_lines)

    def __write_formatted_file(self, relative_path: str, content_lines: list[str]):
        file_name = relative_path.replace(".py", "-formatted.py")
        full_output_path = self.__output_base_path + file_name

        self.__ensure_directories_exist(full_output_path)

        with open(full_output_path, "w", encoding="utf8") as file:
            file.writelines(content_lines)

    def __ensure_directories_exist(self, path: str):
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
