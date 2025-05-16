from typing import NamedTuple, List, Tuple
from .file_path import FilePath


class FilePathComparison(NamedTuple):
    new_files: List[FilePath]
    deleted_files: List[FilePath]
    common_files: List[Tuple[FilePath, FilePath]]
