import os
from ..types.file_path import FilePath


def get_all_python_file_paths_from_directory(project_path: str) -> list[FilePath]:
    python_files = []

    for dirpath, _, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                relative_path = _get_relative_path(project_path, full_path)
                python_files.append(FilePath(full_path, relative_path))

    return python_files


def _get_relative_path(root_path: str, file_path: str) -> str:
    return file_path.replace(root_path, "")
