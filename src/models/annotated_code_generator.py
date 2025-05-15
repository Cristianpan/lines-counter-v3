import os
from ..types.file_changes import FileChanges


class AnnotatedCodeGenerator:
    def __init__(self, output_base_path: str, changed_files: list[FileChanges]):
        self.__output_base_path = output_base_path
        self.__changed_files = changed_files

    def generate(self):
        for file_change in self.__changed_files:
            old_lines = file_change.old_content
            new_lines = file_change.new_content
            relative_path = file_change.relative_path

            self.__write_annotated_file("old", relative_path, old_lines)
            self.__write_annotated_file("new", relative_path, new_lines)

    def __write_annotated_file(
        self, version_label: str, relative_path: str, content_lines: list[str]
    ):
        annotated_filename = relative_path.replace(".py", f"-{version_label}.py")
        full_output_path = self.__output_base_path + annotated_filename

        self.__ensure_directories_exist(full_output_path)

        with open(full_output_path, "w", encoding="utf8") as f:
            for line in content_lines:
                if line.strip().startswith("def"):
                    f.write("\n")
                f.write(line)

    def __ensure_directories_exist(self, path: str):
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
