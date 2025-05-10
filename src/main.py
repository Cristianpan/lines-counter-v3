from .models.lines_count_report import LinesCountReport

from .models.changes_summary_report import ChangeSummaryReport

from .models.annotated_code_generator import AnnotatedCodeGenerator

from .usecases.count_physical_lines_from_project import (
    count_physical_lines_from_project,
)
from .usecases.count_methods_from_project import (
    count_methods_from_project,
)

from .usecases.count_project_changes import count_project_changes


def process_project_for_physical_line_and_method_counts(
    project_path: str, project_name: str, version_label: str
) -> None:
    physical_lines_count, files_lines_count = count_physical_lines_from_project(
        project_path
    )
    methods_count_list = count_methods_from_project(project_path)

    print(f"Report for the {version_label} version of the project:")
    print(
        LinesCountReport(
            project_name,
            physical_lines_count,
            files_lines_count,
            methods_count_list,
        )
    )


def main():
    #project_name = input("Please enter the project name: ")
    project_name = "chanchito"

    old_project_path = "tests\\assets\\versions_project\\old_version"
    #old_project_path = input("Please enter the path to the old version of the project:")

    new_project_path = "tests\\assets\\versions_project\\new_version"
    #new_project_path = input("Please enter the path to the new version of the project:")

    report_save_path = "tests\\assets\\versions_project\\results"

    try:
        process_project_for_physical_line_and_method_counts(
            old_project_path, project_name, "old"
        )

        process_project_for_physical_line_and_method_counts(
            new_project_path, project_name, "new"
        )

        new_files, deleted_files, modified_files = count_project_changes(
            old_project_path, new_project_path
        )

        ChangeSummaryReport(
            report_save_path, new_files, deleted_files, modified_files
        ).generate()

        AnnotatedCodeGenerator(
            report_save_path, modified_files
        ).generate()

        print("Report with the number of changes, generated")

    except Exception as error:
        print(
            f"Oh no! An error occurred while getting the line count. Verify that the project path is correct and you have read permissions to the directory: {error}"
        )


if __name__ == "__main__":
    main()
