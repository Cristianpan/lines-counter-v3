import os

class LineChangesReport:
    @staticmethod
    def generate_report_with_comments(file_path: str, file_content: list[str]):
        file_name = os.path.basename(file_path)
        new_file_name = file_path.replace(file_name, "comment-" + file_name)

        with open(new_file_name, "w", encoding="utf8") as file:
            for line in file_content:
                if line.strip().startswith("def"):
                    file.write("\n")
                file.write(line)
