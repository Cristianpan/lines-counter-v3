from .models.lines_count_report import LinesCountReport

from .models.lines_count_changes_report import LineCountChangesReport

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
    project_name = input("Please enter the project name: ")

    old_project_path = input("Please enter the path to the old version of the project:")

    new_project_path = input("Please enter the path to the new version of the project:")

    try:
        process_project_for_physical_line_and_method_counts(old_project_path, project_name, "old")
        process_project_for_physical_line_and_method_counts(new_project_path, project_name, "new")

        changes = count_project_changes(old_project_path, new_project_path)

        LineCountChangesReport(new_project_path, changes)

        print("Change report, generated")

    except Exception as error:
        print(
            f"Oh no! An error occurred while getting the line count. Verify that the project path is correct and you have read permissions to the directory: {error}"
        )

if __name__ == "__main__":
    main()
