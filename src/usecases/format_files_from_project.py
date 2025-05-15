from ..helpers.formatter import format_line_code
from ..helpers.get_all_python_file_paths_from_directory import (
    get_all_python_file_paths_from_directory,
)
from ..helpers.get_file_content import get_file_content
from ..types.file_path import FilePath


def format_files_from_project(project_path: str) -> list[tuple[FilePath, list[str]]]:
    """
    Formats all Python files in a given project directory.

    Searches for all Python files within the specified project path,
    formats their contents and returns only the files that were modified
    during formatting.

    Args:
        project_path (str): The path to the root of the project directory.

    Returns:
        list[tuple[FilePath, list[str]]]
    """
    python_file_paths_in_project = get_all_python_file_paths_from_directory(
        project_path
    )

    formatted_files = []

    for file_path in python_file_paths_in_project:
        formatted_file, has_modifications = _format_file_from_project(
            file_path.full_path
        )

        if has_modifications:
            formatted_files.append((file_path, formatted_file))

    return formatted_files


def _format_file_from_project(file_path: str) -> tuple[list[str], bool]:
    original_lines = get_file_content(file_path)
    formatted_lines = []
    has_modifications = False

    for original_line in original_lines:
        formatted_line = format_line_code(original_line)
        formatted_lines.append(formatted_line)

        if original_line != formatted_line:
            has_modifications = True

    return formatted_lines, has_modifications
