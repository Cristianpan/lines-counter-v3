from .utils import get_indent, is_line_too_long, extract_inline_comment
from .grouping import group_functions, group_strings
from .detectors import (
    is_asign,
    is_function_call,
    is_string,
    is_import,
    is_function_definition,
)


def format_line_code(line: str) -> str:
    if not is_line_too_long(line):
        return line

    comment = extract_inline_comment(line)
    code = line.replace(comment.strip(), "")

    if comment and is_line_too_long(comment):
        comment = _format_comment(comment)

    if code and is_line_too_long(code):
        if is_import(code):
            code = _format_import(code)

        elif is_function_definition(code):
            code = _format_function_definition(code)

        elif is_asign(code):
            code = _format_asign(code)

        elif is_function_call(code):
            code = _format_function_call(code)

        elif is_string(code):
            code = _format_string(code)
        else:
            code = _generic_format(code)

    return comment + code


def _format_asign(line: str) -> str:
    base_indent, total_indent = get_indent(line)

    assignment, expression = is_asign(line)

    terms = expression.strip().split()
    terms = group_functions(terms)
    terms = group_strings(terms)

    formatted_line = f"{assignment} (\n"
    is_first = True
    expecting_operator = True

    for term in terms:
        if is_line_too_long(total_indent + term):
            term = format_line_code(f"{total_indent}{term}")

        if is_first:
            formatted_line += f"{total_indent}{term.strip()} \n"
            is_first = False
            continue

        if expecting_operator:
            formatted_line += f"{total_indent}{term} "
        else:
            formatted_line += f"{term}\n"

        expecting_operator = not expecting_operator

    formatted_line += f"{base_indent}) \n"

    return formatted_line


def _format_comment(comment: str) -> str:
    base_ident, _ = get_indent(comment)

    tokens = comment.strip().replace("#", "").split()
    formatted_comment = ""
    aux_formatted_comment = f"{base_ident}# "

    for token in tokens:
        if is_line_too_long(aux_formatted_comment + token):
            formatted_comment += f"{aux_formatted_comment}\n"
            aux_formatted_comment = f"{base_ident}# "

        aux_formatted_comment += f"{token} "

    formatted_comment += f"{aux_formatted_comment}\n"

    return formatted_comment.rstrip()


def _format_function_definition(line: str) -> str:
    base_indent, total_indent = get_indent(line)

    function_declaration, rest = line.split("(", 1)
    params_block, final_declaration = rest.split(")", 1)

    params = params_block.split(",")

    formatted_line = function_declaration + "(\n"
    for param in params:
        formatted_line += f"{total_indent}{param.strip()},\n"

    formatted_line += f"{base_indent}){final_declaration}"

    return formatted_line


def _format_function_call(line: str) -> str:
    base_indent, total_indent = get_indent(line)
    function_call, function_rest = is_function_call(line)

    arguments = function_rest.split(",")
    arguments = group_functions(arguments)
    arguments = group_strings(arguments)

    formatted_line = f"{base_indent}{function_call}\n"

    for argument in arguments:
        if is_line_too_long(total_indent + argument):
            argument = format_line_code(f"{total_indent}{argument}")
            formatted_line += f"{total_indent}{argument.lstrip()}, \n"
        else:
            formatted_line += f"{total_indent}{argument}, \n"

    formatted_line += f"{base_indent})\n"

    return formatted_line


def _format_import(line: str) -> str:
    base_indent, total_indent = get_indent(line)

    # Remove parentheses if present
    line = line.replace("(", "").replace(")", "")

    # Split the line into the part before and after 'import'
    before_import, after_import = line.split("import", 1)

    formatted_line = f"{before_import}import (\n"

    # Split the imported modules by comma
    modules = after_import.split(",")

    for module in modules:
        formatted_line += f"{total_indent}{module.strip()},\n"

    # Close the import block
    formatted_line += f"{base_indent})"

    return formatted_line


def _format_string(line: str) -> str:
    base_indent, total_indent = get_indent(line)
    string_prefix, string_suffix = is_string(line)

    # Remove prefix to tokenize string content only
    content_tokens = line.replace(string_prefix, "").rstrip(string_suffix).split()

    formatted_line = "(\n"
    current_line = string_prefix

    for token in content_tokens:
        # Check if adding this token would exceed the max line size
        if is_line_too_long(total_indent + current_line + token):
            formatted_line += f"{total_indent}{current_line.strip()} {string_suffix}\n"
            current_line = string_prefix  # Start new line with prefix

        current_line += f"{token} "

    # Add the final accumulated line
    formatted_line += f"{total_indent}{current_line.strip()} {string_suffix}\n"

    formatted_line += f"{base_indent})"

    return formatted_line


def _generic_format(line: str) -> str:
    base_indent, total_indent = get_indent(line)

    tokens = line.strip().split()
    tokens = group_functions(tokens)
    tokens = group_strings(tokens)

    formatted_line = ""
    current_line = ""
    is_first_line = True

    for token in tokens:
        indent = base_indent if is_first_line else total_indent

        # Reformat token if it exceeds line length by itself
        if is_line_too_long(token):
            token = format_line_code(f"{indent}{token}")
            token = f"{indent}{token.lstrip()}"

        # If adding token would make line too long, wrap it
        if is_line_too_long(indent + current_line + token):
            formatted_line += f"{indent}{current_line.strip()}\\\n"
            current_line = ""
            is_first_line = False

        current_line += f"{token} "

    # Add the final line
    formatted_line += f"{total_indent}{current_line.strip()}\n"

    return formatted_line
