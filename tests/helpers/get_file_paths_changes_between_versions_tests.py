from unittest import TestCase

from src.helpers.get_file_paths_changes_between_versions import (
    get_file_paths_changes_between_versions,
)


class GetFilePathsChangesBetweenVersionsTests(TestCase):
    def test_that_a_python_project_has_mixed_changes(self):
        sample_old_version_path = "old_version_path"
        sample_old_file_paths = [
            f"{sample_old_version_path}/deleted-file.py",
            f"{sample_old_version_path}/common-file.py",
        ]
        sample_new_version_path = "new_version_path"
        sample_new_file_paths = [
            f"{sample_new_version_path}/common-file.py",
            f"{sample_new_version_path}/new-file.py",
        ]

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_version_path,
            sample_old_file_paths,
            sample_new_version_path,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 1)
        self.assertEqual(len(file_paths_changes.new_files), 1)
        self.assertEqual(len(file_paths_changes.common_files), 1)

    def test_that_a_python_project_has_not_changes(self):
        sample_old_version_path = "old_version_path"
        sample_old_file_paths = [
            f"{sample_old_version_path}/common-file.py",
            f"{sample_old_version_path}/common-file2.py",
        ]
        sample_new_version_path = "new_version_path"
        sample_new_file_paths = [
            f"{sample_new_version_path}/common-file.py",
            f"{sample_new_version_path}/common-file2.py",
        ]

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_version_path,
            sample_old_file_paths,
            sample_new_version_path,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 0)
        self.assertEqual(len(file_paths_changes.new_files), 0)
        self.assertEqual(len(file_paths_changes.common_files), 2)

    def test_that_a_python_project_has_deleted_files(self):
        sample_old_version_path = "old_version_path"
        sample_old_file_paths = [
            f"{sample_old_version_path}/deleted-file.py",
            f"{sample_old_version_path}/common-file.py",
        ]
        sample_new_version_path = "new_version_path"
        sample_new_file_paths = []

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_version_path,
            sample_old_file_paths,
            sample_new_version_path,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 2)
        self.assertEqual(len(file_paths_changes.new_files), 0)
        self.assertEqual(len(file_paths_changes.common_files), 0)

    def test_that_a_python_project_has_new_files(self):
        sample_old_version_path = "old_version_path"
        sample_old_file_paths = []
        sample_new_version_path = "new_version_path"
        sample_new_file_paths = [
            f"{sample_new_version_path}/common-file.py",
            f"{sample_new_version_path}/common-file2.py",
        ]

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_version_path,
            sample_old_file_paths,
            sample_new_version_path,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 0)
        self.assertEqual(len(file_paths_changes.new_files), 2)
        self.assertEqual(len(file_paths_changes.common_files), 0)
