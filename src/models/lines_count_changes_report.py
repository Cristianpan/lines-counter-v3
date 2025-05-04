from io import TextIOWrapper
from ..types.changes_count import ChangesCount


class LineCountChangesReport:
    @staticmethod
    def generate_report(root_path: str, data: dict[str, ChangesCount]):

        divider = "-" * 140 + "\n"
        report_name = "\\report_with_changes.txt"

        with open(root_path + report_name, "w+", encoding="utf-8") as file:
            file.write(LineCountChangesReport.__generate_header())
            file.write(divider)
            total_changes = ChangesCount()

            for file_path in data:
                changes = data[file_path]
                total_changes.added += changes.added
                total_changes.modified += changes.modified
                total_changes.deleted += changes.deleted
                file.write(
                    LineCountChangesReport.__generate_body(
                        file_name=file_path, changes=changes
                    )
                )
            file.write(divider)
            file.write(LineCountChangesReport.__generate_body("Total", total_changes))

    @staticmethod
    def __generate_header() -> str:
        return f"{"Archivo":<40} | {"Líneas borradas":<30} | {"Líneas modificadas":<30} | {"Lineas agregadas":<30}\n"

    @staticmethod
    def __generate_body(file_name: str, changes: ChangesCount) -> str:
        return f"{file_name:<40} | {changes.deleted:<30} | {changes.modified:<30} | {changes.added:<30}\n"
    
