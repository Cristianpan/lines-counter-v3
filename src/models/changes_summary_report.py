import os
from io import TextIOWrapper
from ..types.file_changes import FileChanges
from ..types.changes_count import ChangesCount


class ChangeSummaryReport:
    __DIVIDER = f"+{'-' * 41} + {'-' * 20} + {'-' * 20} + {'-' * 21}+\n"

    def __init__(
        self,
        output_path: str,
        added_files: list[FileChanges],
        deleted_files: list[FileChanges],
        modified_files: list[FileChanges],
    ):
        self.__output_path = output_path
        self.__added_files = added_files
        self.__deleted_files = deleted_files
        self.__modified_files = modified_files

    def generate(self):
        report_filename = "project_changes_report.txt"
        full_path = os.path.join(self.__output_path, report_filename)

        with open(full_path, "w", encoding="utf-8") as report_file:
            self.__write_section(report_file, "Archivos agregados", self.__added_files)
            self.__write_section(
                report_file, "Archivos modificados", self.__modified_files
            )
            self.__write_section(report_file, "Archivos borrados", self.__deleted_files)

    def __write_section(
        self, file_writer: TextIOWrapper, title: str, files: list[FileChanges]
    ):
        file_writer.write(self.__build_header(title))
        total = ChangesCount()

        for file_change in files:
            counter = file_change.counter
            total.added += counter.added
            total.deleted += counter.deleted
            total.modified += counter.modified

            file_writer.write(self.__format_row(file_change.relative_path, counter))

        file_writer.write(self.__format_row("Total", total))
        file_writer.write("\n\n")

    def __build_header(self, title: str) -> str:
        return (
            f"+{'-' * 111}+\n"
            f"|{title:^111}|\n"
            f"{self.__DIVIDER}"
            f"| {'Archivo':<40} | {'Líneas borradas':<20} | {'Líneas modificadas':<20} | {'Líneas agregadas':<20} |\n"
            f"{self.__DIVIDER}"
        )

    def __format_row(self, file_name: str, counter: ChangesCount) -> str:
        return (
            f"| {file_name:<40} | {counter.deleted:<20} | {counter.modified:<20} | {counter.added:<20} |\n"
            f"{self.__DIVIDER}"
        )
