def get_file_content(file_path: str) -> list[str]:
    with open(file_path, encoding="utf-8") as file:
        return file.readlines()
