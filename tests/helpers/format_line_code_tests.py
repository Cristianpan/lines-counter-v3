# noqa

from src.helpers.formatter import format_line_code
from unittest import TestCase


class FormatLineCodeTests(TestCase):
    def test_that_the_imports_is_formatted_correctly(self):
        import_test = "from .detectors import is_asign, is_function_call, is_string, is_import, is_function_definition"
        expected_result = "\n".join(
            [
                "from .detectors import (",
                "    is_asign,",
                "    is_function_call,",
                "    is_string,",
                "    is_import,",
                "    is_function_definition,",
                ")",
            ]
        )

        self.assertEqual(expected_result, format_line_code(import_test))

    def test_that_the_function_definition_is_formatted_correctly(self):
        function_def = "def get_file_paths_changes_between_versions(old_file_paths: List[FilePath],new_file_paths: List[FilePath]) -> FilePathComparison:"
        expected_result = "\n".join(
            [
                "def get_file_paths_changes_between_versions(",
                "    old_file_paths: List[FilePath],",
                "    new_file_paths: List[FilePath],",
                ") -> FilePathComparison:",
            ]
        )
        self.assertEqual(expected_result, format_line_code(function_def))

    def test_that_the_asignment_is_formatted_correctly(self):
        asigment = "new_files, deleted_files, modified_files = count_project_changes(old_project_path, new_project_path)"
        expected_result = "\n".join(
            [
                "new_files, deleted_files, modified_files = (",
                "    count_project_changes(old_project_path, new_project_path)",
                ")",
            ]
        )

        self.assertEqual(expected_result, format_line_code(asigment).strip())

    def test_that_the_string_is_formatted_correctly(self):
        string = '"este es un string que es demasiado largo y debe de ser formateado en lineas menores a 80 caracteres"'
        expected_result = "\n".join(
            [
                "(",
                '    "este es un string que es demasiado largo y debe de ser formateado en lineas"',
                '    "menores a 80 caracteres "',
                ")",
            ]
        )
        self.assertEqual(expected_result, format_line_code(string))

    def test_that_the_function_call_is_formatted_correctly(self):
        function_call = "ChangeSummaryReport.generate(report_save_path, new_files, deleted_files, modified_files)"

        expected_result = "\n".join(
            [
                "ChangeSummaryReport.generate(",
                "    report_save_path,",
                "    new_files,",
                "    deleted_files,",
                "    modified_files,",
                ")",
            ]
        )

        self.assertEqual(expected_result, format_line_code(function_call))

    def test_that_the_inline_comment_is_formatted_correctly(self):
        comment = "# este es un string que es demasiado largo y debe de ser formateado en lineas menores a 80 caracteres"
        expected_result = "\n".join(
            [
                "# este es un string que es demasiado largo y debe de ser formateado en lineas",
                "# menores a 80 caracteres",
            ]
        )

        self.assertEqual(expected_result, format_line_code(comment))

    def test_that_the_code_with_inline_comment_is_formatted_correctly(self):
        code_with_comment = "print('mensaje a imprimir') # este es un comentario que debe de ser formateado con el codigo"
        expected_result = "\n".join(
            [
                "# este es un comentario que debe de ser formateado con el codigo",
                "print('mensaje a imprimir')",
            ]
        )

        print(format_line_code(code_with_comment))
        self.assertEqual(expected_result, format_line_code(code_with_comment).strip())
