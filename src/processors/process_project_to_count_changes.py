from ..models.changes_summary_report import ChangeSummaryReport

from ..models.annotated_code_generator import AnnotatedCodeGenerator

from ..usecases.count_project_changes import count_project_changes


def process_project_to_count_changes(
    old_project_path: str, new_project_path: str, report_save_path
) -> None:
    new_files, deleted_files, modified_files = count_project_changes(
        old_project_path, new_project_path
    )

    ChangeSummaryReport(
        report_save_path, new_files, deleted_files, modified_files
    ).generate()

    AnnotatedCodeGenerator(report_save_path, modified_files).generate()

    print("Report with the number of changes, generated")
