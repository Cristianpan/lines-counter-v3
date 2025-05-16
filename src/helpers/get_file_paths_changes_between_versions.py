from typing import List
from ..types.file_path import FilePath
from ..types.file_path_comparison import FilePathComparison


def get_file_paths_changes_between_versions(
    old_file_paths: List[FilePath],
    new_file_paths: List[FilePath],
) -> FilePathComparison:
    """
    Compares two sets of file paths from two different versions of a directory
    and returns the changes between them.

    Args:
        old_file_paths (List[str]): List of file paths from the old version.
        new_file_paths (List[str]): List of file paths from the new version.

    Returns:
        FilePathComparison: An object with:
            - new_files (files present only in the new version)
            - deleted_files (files present only in the old version)
            - common_files (files present in both versions)
    """

    deleted_files = []
    new_files = []
    common_files = []

    for old_file_path in old_file_paths:
        # Try to find the same file (by relative path) in the new version
        index = _find_file_index(old_file_path.relative_path, new_file_paths)

        # Match found: file exists in both versions
        if index != -1:
            common_files.append((old_file_path, new_file_paths[index]))
            del new_file_paths[index]
        else:
            deleted_files.append(old_file_path)

    # Remaining files in new_file_paths are new (not present in old version)
    new_files = new_file_paths

    return FilePathComparison(new_files, deleted_files, common_files)


def _find_file_index(file_to_find: str, file_paths: list[FilePath]) -> int:
    """
    Searches for a file path in a list of FilePath objects and returns its index.

    Args:
        file_to_find (str): The relative path of the file to search for.
        file_paths (list[FilePath]): A list of FilePath objects to search in.

    Returns:
        int: The index of the file in the list if found; otherwise, -1.
    """
    for index, new_file_path in enumerate(file_paths):
        if file_to_find == new_file_path.relative_path:
            return index
    return -1
