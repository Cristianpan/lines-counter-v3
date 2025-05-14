from .changes_count import ChangesCount

from typing import NamedTuple


class FileChanges(NamedTuple):
    relative_path: str
    counter: ChangesCount
    old_content: list[str] = []
    new_content: list[str] = []
