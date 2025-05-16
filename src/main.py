from .processors.process_project_for_physical_line_and_methos_counts import (
    process_project_for_physical_line_and_method_counts,
)

from .processors.process_project_to_count_changes import (
    process_project_to_count_changes,
)

from .processors.process_project_to_format_files import process_project_to_format_files


def main():
    project_name = input("Please enter the project name: ")

    old_project_path = input(
        "Please enter the path to the old version of the project: "
    )

    new_project_path = input(
        "Please enter the path to the new version of the project: "
    )

    report_save_path = input(
        "Please enter the path to save the reports and the formatted files with the annotated changes: "
    )

    print("\n", "=" * 130, "\n")

    try:
        process_project_for_physical_line_and_method_counts(
            old_project_path, project_name + " old version", report_save_path
        )

        process_project_for_physical_line_and_method_counts(
            new_project_path, project_name + " new version", report_save_path
        )

        process_project_to_count_changes(
            old_project_path, new_project_path, report_save_path
        )

        process_project_to_format_files(new_project_path, report_save_path)

    except Exception as error:
        print(
            f"Oh no! An error occurred while getting the line count. Verify that the project path is correct and you have read permissions to the directory: {error}"
        )

    input("\nPress Enter to exit: ")


if __name__ == "__main__":
    main()
