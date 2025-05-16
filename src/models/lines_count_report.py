import os


class LinesCountReport:
    __REPORT_FILE_NAME: str = "lines_count_report.txt"
    __DIVIDER = f"+ {'-' * 40} + {'-' * 20} + {'-' * 20} + {'-' * 20} +\n"
    open_file_type = "w+"

    def __init__(
        self,
        project_name: str,
        project_physical_lines_count: int,
        files_physical_lines_count: dict,
        files_methods_count: dict,
        output_path: str,
    ):
        self.__project_name = project_name
        self.__project_physical_lines_count = project_physical_lines_count
        self.__files_physical_lines_count = files_physical_lines_count
        self.__files_methods_count = files_methods_count
        self.__output_path = output_path

    def generate(self):
        report_full_path = os.path.join(self.__output_path, self.__REPORT_FILE_NAME)

        with open(
            report_full_path, LinesCountReport.open_file_type, encoding="utf-8"
        ) as report_file:
            report_file.write(self.__build_header(self.__project_name))
            for file_path in self.__files_physical_lines_count:
                physical_lines = self.__files_physical_lines_count[file_path]
                methods = self.__files_methods_count[file_path]
                for class_name, methods in methods.items():
                    report_file.write(
                        self.__format_row(
                            file_path, class_name, physical_lines, methods
                        )
                    )

            report_file.write(
                self.__format_row("Total", "", "", self.__project_physical_lines_count)
            )
            report_file.write("\n\n")
        LinesCountReport.open_file_type = "a"

    def __build_header(self, title: str) -> str:
        return (
            f"+{'-' * 111}+\n"
            f"| {title:^110}|\n"
            f"{self.__DIVIDER}"
            f"| {'Archivo':<40} | {'Clase':<20} | {'Métodos/Funciones':<20} | {'Líneas Físicas':<20} |\n"
            f"{self.__DIVIDER}"
        )

    def __format_row(
        self, file_path: str, class_name: str, methods: int | str, physical_lines: int
    ) -> str:
        return (
            f"| {file_path:<40} | {class_name:<20} | {methods:<20} | {physical_lines:<20} |\n"
            f"{self.__DIVIDER}"
        )
