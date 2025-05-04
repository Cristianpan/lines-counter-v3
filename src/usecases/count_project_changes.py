from ..helpers.get_all_python_file_paths_from_directory import (
    get_all_python_file_paths_from_directory
)

from ..helpers.get_file_paths_changes_between_versions import (
    get_file_paths_changes_between_versions,
)

from ..helpers.get_lines_with_visible_content_from_file import (
    get_lines_with_visible_content_from_file,
)

from ..helpers.remove_all_comments_from_content_lines import (
    remove_all_comments_from_content_lines,
)

from ..models.lines_changes_report import LineChangesReport

from ..types.file_path import FilePath

from ..types.changes_count import ChangesCount

from ..helpers.get_similarity_percentage import get_similarity_percentage


def count_project_changes(
    old_path_version: str, new_path_version: str
) -> dict[str, ChangesCount]:

    filter_files = lambda file_name: "comment-" not in file_name

    files_path_from_old_version = get_all_python_file_paths_from_directory(
        old_path_version, filter_files
    )

    files_path_from_new_version = get_all_python_file_paths_from_directory(
        new_path_version, filter_files
    )

    files_comparison = get_file_paths_changes_between_versions(
        old_path_version,
        files_path_from_old_version,
        new_path_version,
        files_path_from_new_version,
    )

    return {
        **_process_new_files(new_files=files_comparison.new_files),
        **_process_deleted_files(
            deleted_files=files_comparison.deleted_files,
        ),
        **_process_common_files(
            common_files=files_comparison.common_files,
        ),
    }


def _process_deleted_files(deleted_files: list[FilePath]) -> dict[str, ChangesCount]:

    changes = {}

    for deleted_file in deleted_files:

        old_file_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(deleted_file.full_path)
        )

        changes_by_file, old_file_content, new_file_content = _compare_content(
            old_file_content=old_file_content
        )

        changes[deleted_file.relative_path] = changes_by_file

        LineChangesReport.generate_report_with_comments(
            deleted_file.full_path, old_file_content
        )

    return changes


def _process_new_files(new_files: list[FilePath]) -> dict[str, ChangesCount]:
    changes = {}

    for new_file in new_files:

        new_file_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(new_file.full_path)
        )

        changes_by_file, old_file_content, new_file_content = _compare_content(
            new_file_content=new_file_content
        )
        changes[new_file.relative_path] = changes_by_file

        LineChangesReport.generate_report_with_comments(
            new_file.full_path, new_file_content
        )

    return changes


def _process_common_files(
    common_files: list[tuple[FilePath, FilePath]],
) -> dict[str, ChangesCount]:
    changes = {}

    for old_file, new_file in common_files:
        old_file_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(old_file.full_path)
        )

        new_file_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(new_file.full_path)
        )

        changes_by_file, old_file_content, new_file_content = _compare_content(
            old_file_content, new_file_content
        )

        changes[new_file.relative_path] = changes_by_file

        LineChangesReport.generate_report_with_comments(
            old_file.full_path, old_file_content
        )

        LineChangesReport.generate_report_with_comments(
            new_file.full_path, new_file_content
        )

    return changes


def _compare_content(
    old_file_content: list[str] = [], new_file_content: list[str] = []
) -> tuple[dict[str, ChangesCount, list[str], list[str]]]:
    min_file_size = min(len(old_file_content), len(new_file_content))

    changes = ChangesCount()

    for i in range(0, min_file_size):
        similarity_percentage = get_similarity_percentage(
            old_file_content[i].rstrip(), new_file_content[i].rstrip()
        )

        if similarity_percentage == 1:
            continue
        else:
            changes.deleted += 1
            old_file_content[i] = _annotate_line(old_file_content[i], "borrado")

        if similarity_percentage >= 0.7:
            new_file_content[i] = _annotate_line(new_file_content[i], "modificado")
            changes.modified += 1
        else:
            new_file_content[i] = _annotate_line(new_file_content[i], "agregado")
            changes.added += 1

    if len(old_file_content) > min_file_size:
        for i in range(min_file_size, len(old_file_content)):
            changes.deleted += 1
            old_file_content[i] = _annotate_line(old_file_content[i], "borrado")

    if len(new_file_content) > min_file_size:
        for i in range(min_file_size, len(new_file_content)):
            new_file_content[i] = _annotate_line(new_file_content[i], "agregado")
            changes.added += 1

    return changes, old_file_content, new_file_content


def _annotate_line(line: str, annotation: str) -> str:
    return f"{line.replace("\n", "")} #{annotation}\n"
