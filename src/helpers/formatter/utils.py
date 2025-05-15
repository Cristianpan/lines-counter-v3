import tokenize
from io import StringIO


def is_line_too_long(line: str) -> bool:
    _MAX_LINE_SIZE = 80

    return len(line) > _MAX_LINE_SIZE


def get_indent(line: str):
    _ADITIONAL_INDENT = " " * 4
    base_indent = " " * (len(line) - len(line.lstrip()))
    total_ident = base_indent + _ADITIONAL_INDENT

    return base_indent, total_ident


def extract_inline_comment(line: str) -> tuple[str, str]:
    if "#" not in line:
        return ""

    base_indent, _ = get_indent(line)

    tokens = tokenize.generate_tokens(StringIO(line).readline)

    for type, text, _, _, _ in tokens:
        if type == tokenize.COMMENT:
            comment = f"{base_indent}{text}"
            return comment

    return ""
