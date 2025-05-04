from unittest import TestCase
from pathlib import Path

from src.helpers.get_all_python_file_paths_from_directory import (
    get_all_python_file_paths_from_directory,
)


class GetAllPythonFilePathsFromDirectoryTests(TestCase):
    def test_that_a_directory_without_python_files_should_return_zero(self):
        python_files = get_all_python_file_paths_from_directory(
            "tests/assets/empty_dir"
        )

        self.assertEqual(python_files, [])

    def test_that_a_python_project_has_more_than_one_file(self):
        python_files = get_all_python_file_paths_from_directory(
            "tests/assets/only_code_python_project"
        )

        self.assertGreaterEqual(len(python_files), 1)

    def test_that_a_python_project_has_a_main_file(self):
        python_files = get_all_python_file_paths_from_directory(
            "tests/assets/only_code_python_project"
        )
        python_files = [Path(p) for p in python_files]

        self.assertIn(
            Path("tests/assets/only_code_python_project/main.py"), python_files
        )

    def test_filter_python_file(self):
        callable = lambda name: "main" not in name
        python_files = get_all_python_file_paths_from_directory(
            "tests/assets/only_code_python_project", callable
        )

        python_files = [Path(p) for p in python_files]

        self.assertNotIn(
            Path("tests/assets/only_code_python_project/main.py"), python_files
        )
