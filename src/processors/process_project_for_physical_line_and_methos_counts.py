from ..models.lines_count_report import LinesCountReport
from ..usecases.count_physical_lines_from_project import (
    count_physical_lines_from_project,
)
from ..usecases.count_methods_from_project import (
    count_methods_from_project,
)


def process_project_for_physical_line_and_method_counts(
    project_path: str, project_name: str, output_path: str
) -> None:
    physical_lines_count, files_lines_count = count_physical_lines_from_project(
        project_path
    )
    methods_count_list = count_methods_from_project(project_path)

    LinesCountReport(
        project_name,
        physical_lines_count,
        files_lines_count,
        methods_count_list,
        output_path,
    ).generate()

    print(
        f"Report with the number of physical lines and methods in the project '{project_name}' generated."
    )
