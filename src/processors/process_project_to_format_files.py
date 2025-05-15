from ..models.formatted_file_generator import FormattedFileGenerator


from ..usecases.format_files_from_project import format_files_from_project


def process_project_to_format_files(project_path: str, report_save_path: str) -> None:
    formatted_files = format_files_from_project(project_path)

    if formatted_files:
        FormattedFileGenerator(report_save_path, formatted_files).generate()
        print("Formatted files have been generated")
    else:
        print("There were no files to format")
