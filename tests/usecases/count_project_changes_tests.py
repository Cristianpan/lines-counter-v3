from src.usecases.count_project_changes import count_project_changes
from src.types.file_changes import FileChanges
from unittest import TestCase
import os


class CountProjectChangesTests(TestCase):
    def setUp(self):
        old_path_version = "tests/assets/versions_project/old_version"
        new_path_version = "tests/assets/versions_project/new_version"

        new_files, deleted_files, common_files = count_project_changes(
            old_path_version, new_path_version
        )

        self.new_files = new_files
        self.deleted_files = deleted_files
        self.common_files = common_files

    def test_counts_changes_correctly_in_modified_file(self):
        common_file = self.get_file_by_path("/common_file.py", self.common_files)
        changes_counter = common_file.counter

        self.assertEqual(changes_counter.added, 2)
        self.assertEqual(changes_counter.deleted, 2)
        self.assertEqual(changes_counter.modified, 2)

    def test_counts_changes_correctly_in_deleted_file(self):
        deleted_file = self.get_file_by_path("/deleted_file.py", self.deleted_files)
        changes_counter = deleted_file.counter

        self.assertEqual(changes_counter.added, 0)
        self.assertEqual(changes_counter.deleted, 3)
        self.assertEqual(changes_counter.modified, 0)

    def test_counts_changes_correctly_in_new_file(self):
        new_file = self.get_file_by_path("/new_file.py", self.new_files)
        changes_counter = new_file.counter

        self.assertEqual(changes_counter.added, 7)
        self.assertEqual(changes_counter.deleted, 0)
        self.assertEqual(changes_counter.modified, 0)

    def test_returns_none_for_unchanged_file(self):
        unchanged_file = self.get_file_by_path("/unchanged_file.py", self.common_files)

        self.assertFalse(unchanged_file)

    def get_file_by_path(self, path: str, files: list[FileChanges]) -> FileChanges:
        normalized_path = os.path.normpath(path)
        for file in files:
            if os.path.normpath(file.relative_path) == normalized_path:
                return file
        return None
