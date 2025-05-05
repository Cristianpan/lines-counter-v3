from typing import List, Tuple
from ..types.file_path import FilePath
from ..types.file_path_comparison import FilePathComparison


def get_file_paths_changes_between_versions(
    root_old_version: str,
    old_file_paths: List[str],
    root_new_version: str,
    new_file_paths: List[str],
) -> FilePathComparison:
    """
    Compares two sets of file paths from two different versions of a directory
    and returns the changes between them.

    Args:
        root_old_version (str): Root path of the old version.
        old_file_paths (List[str]): List of file paths from the old version.
        root_new_version (str): Root path of the new version.
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
        aux_new_file_path = old_file_path.replace(root_old_version, root_new_version)
        relative_file_path = _get_relative_path(root_old_version, old_file_path)

        if aux_new_file_path not in new_file_paths:
            deleted_files.append(FilePath(old_file_path, relative_file_path))

        if aux_new_file_path in new_file_paths:
            common_files.append(
                (
                    FilePath(old_file_path, relative_file_path),
                    FilePath(aux_new_file_path, relative_file_path),
                )
            )
            new_file_paths.remove(aux_new_file_path)

    for new_file_path in new_file_paths:
        relative_file_path = _get_relative_path(root_new_version, new_file_path)
        new_files.append(FilePath(new_file_path, relative_file_path))

    return FilePathComparison(new_files, deleted_files, common_files)


def _get_relative_path(root_path: str, file_path: str) -> str:
    return file_path.replace(root_path, "")
