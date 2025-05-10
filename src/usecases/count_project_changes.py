from ..helpers.get_all_python_file_paths_from_directory import (
    get_all_python_file_paths_from_directory,
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

from ..types.file_path import FilePath

from ..types.file_changes import FileChanges

from ..types.changes_count import ChangesCount

from ..helpers.get_similarity_percentage import get_similarity_percentage


def count_project_changes(
    old_version_path: str, new_version_path: str
) -> tuple[list[FileChanges], list[FileChanges], list[FileChanges]]:

    old_version_files = get_all_python_file_paths_from_directory(old_version_path)

    new_version_files = get_all_python_file_paths_from_directory(new_version_path)

    file_differences = get_file_paths_changes_between_versions(
        old_version_path,
        old_version_files,
        new_version_path,
        new_version_files,
    )

    new_files = _process_new_files(file_differences.new_files)
    deleted_files = _process_deleted_files(file_differences.deleted_files)
    modified_files = _process_common_files(file_differences.common_files)

    return new_files, deleted_files, modified_files


def _process_deleted_files(deleted_files: list[FilePath]) -> list[FileChanges]:
    changes = []

    for deleted_file in deleted_files:
        old_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(deleted_file.full_path)
        )

        deleted_line_count = len(old_content)
        changes_counter = ChangesCount(deleted=deleted_line_count)

        file_changes = FileChanges(
            relative_path=deleted_file.relative_path, counter=changes_counter
        )

        changes.append(file_changes)

    return changes


def _process_new_files(new_files: list[FilePath]) -> list[FileChanges]:
    changes = []

    for new_file in new_files:
        new_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(new_file.full_path)
        )

        added_lines = len(new_content)
        changes_counter = ChangesCount(added=added_lines)

        file_changes = FileChanges(
            relative_path=new_file.relative_path, counter=changes_counter
        )

        changes.append(file_changes)

    return changes


def _process_common_files(
    common_files_pairs: list[tuple[FilePath, FilePath]],
) -> list[FileChanges]:
    changes = []

    for old_version, new_version in common_files_pairs:
        old_version_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(old_version.full_path)
        )

        new_version_content = remove_all_comments_from_content_lines(
            get_lines_with_visible_content_from_file(new_version.full_path)
        )

        changes_counter, old_annotated_content, new_annotated_content = (
            _compare_content(old_version_content, new_version_content)
        )

        if _has_changes(changes_counter):
            file_changes = FileChanges(
                relative_path=new_version.relative_path,
                counter=changes_counter,
                old_content=old_annotated_content,
                new_content=new_annotated_content,
            )

            changes.append(file_changes)

    return changes


def _compare_content(
    old_content: list[str], new_content: list[str]
) -> tuple[ChangesCount, list[str], list[str]]:
    
    min_file_size = min(len(old_content), len(new_content))
    changes_counter = ChangesCount()
    IS_EQUAL = 1.0
    IS_MODIFIED = 0.6

    for i in range(0, min_file_size):

        old_line = old_content[i].rstrip()
        new_line = new_content[i].rstrip()

        similarity_percentage = get_similarity_percentage(old_line, new_line)

        if similarity_percentage == IS_EQUAL:
            continue
        else:
            changes_counter.deleted += 1
            old_content[i] = _annotate_line(old_content[i], "borrado")

        if similarity_percentage >= IS_MODIFIED:
            new_content[i] = _annotate_line(new_content[i], "modificado")
            changes_counter.modified += 1
        else:
            new_content[i] = _annotate_line(new_content[i], "agregado")
            changes_counter.added += 1

    if len(old_content) > min_file_size:
        for i in range(min_file_size, len(old_content)):
            changes_counter.deleted += 1
            old_content[i] = _annotate_line(old_content[i], "borrado")

    if len(new_content) > min_file_size:
        for i in range(min_file_size, len(new_content)):
            new_content[i] = _annotate_line(new_content[i], "agregado")
            changes_counter.added += 1

    return changes_counter, old_content, new_content


def _has_changes(counter: ChangesCount) -> bool:
    return counter.added or counter.deleted or counter.modified


def _annotate_line(line: str, annotation: str) -> str:
    return f"{line.replace('\n', '')} #{annotation}\n"
