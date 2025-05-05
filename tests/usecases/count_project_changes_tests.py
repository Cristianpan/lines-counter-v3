from src.usecases.count_project_changes import count_project_changes
from src.types.changes_count import ChangesCount
from unittest import TestCase


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

    def test_that_counts_changes_correctly_from_file_with_changes(self):
        common_file = self.common_files[0]
        changes_counter = common_file.counter

        self.assertEqual(common_file.relative_path, "\common_file.py")
        self.assertEqual(changes_counter.added, 2)
        self.assertEqual(changes_counter.deleted, 2)
        self.assertEqual(changes_counter.modified, 2)

    def test_that_counts_changes_correctly_from_deleted_file(self):
        deleted_file = self.deleted_files[0]
        changes_counter = deleted_file.counter

        self.assertEqual(deleted_file.relative_path, "\deleted_file.py")
        self.assertEqual(changes_counter.added, 0)
        self.assertEqual(changes_counter.deleted, 3)
        self.assertEqual(changes_counter.modified, 0)

    def test_that_counts_changes_correctly_from_new_file(self):
        new_file = self.new_files[0]
        changes_counter = new_file.counter

        self.assertEqual(new_file.relative_path, "\\new_file.py")
        self.assertEqual(changes_counter.added, 7)
        self.assertEqual(changes_counter.deleted, 0)
        self.assertEqual(changes_counter.modified, 0)

    def test_that_not_return_changes_from_unchanged_file(self):
        exist_unchanged_file = False
        for common_file in self.common_files:
            if common_file.relative_path == "\\unchanged_file.py":
                exist_unchanged_file = True

        self.assertFalse(exist_unchanged_file)
