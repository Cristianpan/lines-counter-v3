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
        expected_python_file = Path("tests/assets/only_code_python_project/main.py")

        exist_python_file = False

        for python_file in python_files: 
            if Path(python_file.full_path) == expected_python_file: 
                exist_python_file = True
                break

        self.assertTrue(exist_python_file)
        