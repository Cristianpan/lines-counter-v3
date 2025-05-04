from usecases.count_project_changes import count_project_changes
from unittest import TestCase


class CountChangesFromProjectTests(TestCase):

    def setUp(self):
        old_path_version = "tests/assets/versions_project/old_version"
        new_path_version = "tests/assets/versions_project/new_version"
        self.changes = count_project_changes(old_path_version, new_path_version)


    def test_that_counts_changes_correctly_from_file_with_changes(self):
        common_file = "\common_file.py"

        changes = self.changes[common_file]

        self.assertEqual(changes.added, 2)
        self.assertEqual(changes.deleted, 1)
        self.assertEqual(changes.modified, 1)

    def test_that_counts_changes_correctly_from_deleted_file(self):
        deleted_file = "\deleted_file.py"

        changes = self.changes[deleted_file]

        self.assertEqual(changes.added, 0)
        self.assertEqual(changes.deleted, 3)
        self.assertEqual(changes.modified, 0)

    def test_that_counts_changes_correctly_from_new_file(self):
        deleted_file = "\\new_file.py"

        changes = self.changes[deleted_file]

        self.assertEqual(changes.added, 7)
        self.assertEqual(changes.deleted, 0)
        self.assertEqual(changes.modified, 0)

    def test_that_counts_changes_correctly_from_unchanged_file(self):
        unchanged_file = "\\unchanged_file.py"

        changes = self.changes[unchanged_file]
        
        self.assertEqual(changes.added, 0)
        self.assertEqual(changes.deleted, 0)
        self.assertEqual(changes.modified, 0)
