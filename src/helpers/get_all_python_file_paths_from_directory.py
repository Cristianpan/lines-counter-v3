import os
from typing import Callable


def get_all_python_file_paths_from_directory(
    project_path: str, filter_fn: Callable[[str], bool] = lambda name: True
) -> list[str]:
    python_files = []

    for dirpath, _, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith(".py") and filter_fn(filename):
                full_path = os.path.join(dirpath, filename)
                python_files.append(full_path)

    return python_files
