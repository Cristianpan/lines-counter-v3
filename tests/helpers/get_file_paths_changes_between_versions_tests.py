from unittest import TestCase
from src.types.file_path import FilePath

from src.helpers.get_file_paths_changes_between_versions import (
    get_file_paths_changes_between_versions,
)


class GetFilePathsChangesBetweenVersionsTests(TestCase):
    def test_that_a_python_project_has_mixed_changes(self):

        sample_old_file_paths = self.__generate_file_paths(
            "old_version_path", 
            ["/deleted-file.py","/common-file.py"]
        )

        sample_new_file_paths = self.__generate_file_paths(
            "new_version_path", 
            ["/common-file.py", "/new-file.py"]
        )

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_file_paths,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 1)
        self.assertEqual(len(file_paths_changes.new_files), 1)
        self.assertEqual(len(file_paths_changes.common_files), 1)

    def test_that_a_python_project_has_not_changes(self):
        sample_old_file_paths = self.__generate_file_paths(
            "old_version_path", 
            ["/common-file2.py","/common-file.py"]
        )

        sample_new_file_paths = self.__generate_file_paths(
            "new_version_path", 
            ["/common-file.py", "/common-file2.py"]
        )

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_file_paths,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 0)
        self.assertEqual(len(file_paths_changes.new_files), 0)
        self.assertEqual(len(file_paths_changes.common_files), 2)

    def test_that_a_python_project_has_deleted_files(self):
        sample_old_file_paths = self.__generate_file_paths(
            "old_version_path", 
            ["/common-file2.py","/common-file.py"]
        )

        sample_new_file_paths = []

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_file_paths,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 2)
        self.assertEqual(len(file_paths_changes.new_files), 0)
        self.assertEqual(len(file_paths_changes.common_files), 0)

    def test_that_a_python_project_has_new_files(self):
        sample_old_file_paths = []

        sample_new_file_paths = self.__generate_file_paths(
            "new_version_path", 
            ["/common-file.py", "/common-file2.py"]
        )

        file_paths_changes = get_file_paths_changes_between_versions(
            sample_old_file_paths,
            sample_new_file_paths,
        )

        self.assertEqual(len(file_paths_changes.deleted_files), 0)
        self.assertEqual(len(file_paths_changes.new_files), 2)
        self.assertEqual(len(file_paths_changes.common_files), 0)

    def __generate_file_paths(self, root_project: str, file_paths: list[str]) -> list[FilePath]:
        files = []
        for file_path in file_paths:
            files.append(FilePath(f"{root_project}{file_path}", file_path))

        return files
