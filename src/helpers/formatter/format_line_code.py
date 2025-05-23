from .utils import get_indent, is_line_too_long, extract_inline_comment
from .grouping import group_functions, group_strings
from .detectors import (
    is_asign,
    is_function_call,
    is_string,
    is_import,
    is_function_definition,
)

from re import split


def format_line_code(line: str) -> str:
    """
    Formats a code line to ensure it does not exceed a maximum length.

    It processes inline comments and different code structures
    (imports, function definitions, assignments, calls, strings) differently.

    Args:
        line (str): The line of code to format.

    Returns:
        str: The formatted line
    """
    if not is_line_too_long(line):
        return line

    comment = extract_inline_comment(line)

    code = line.replace(comment.strip(), "")

    if comment and code.strip():
        comment += "\n"

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
    # Group function calls and strings so they stay together
    terms = group_functions(terms)
    terms = group_strings(terms)

    formatted_line = f"{assignment} (\n"
    is_first = True
    expecting_operator = True

    for term in terms:
        # Recursively format term if too long
        if is_line_too_long(total_indent + term):
            term = format_line_code(f"{total_indent}{term}").rstrip()

        if is_first:
            formatted_line += f"{total_indent}{term.strip()}\n"
            is_first = False
            continue

        # Alternate between operator and operand formatting
        if expecting_operator:
            formatted_line += f"{total_indent}{term} "
        else:
            formatted_line += f"{term}\n"

        expecting_operator = not expecting_operator

    formatted_line += f"{base_indent})\n"

    return formatted_line


def _format_comment(comment: str) -> str:
    base_ident, _ = get_indent(comment)

    tokens = comment.strip().replace("#", "").split()
    formatted_comment = ""
    aux_formatted_comment = f"{base_ident}# "

    for token in tokens:
        # Wrap comment line if it gets too long
        if is_line_too_long(aux_formatted_comment + token):
            formatted_comment += f"{aux_formatted_comment.rstrip()}\n"
            aux_formatted_comment = f"{base_ident}# "

        aux_formatted_comment += f"{token} "

    formatted_comment += f"{aux_formatted_comment.rstrip()}"

    return formatted_comment


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

    split_regex = r"(\)\.|[,)])"

    function_rest = [p for p in split(split_regex, function_rest) if p != ""]

    # Group nested function calls and strings in arguments
    function_rest = group_functions(function_rest)
    function_rest = group_strings(function_rest)

    formatted_line = f"{base_indent}{function_call}"

    for argument in function_rest:
        if is_function_call(argument):
            formatted_line += _format_function_call(base_indent + argument).lstrip()
            continue

        if is_line_too_long(argument) and is_string(argument):
            formatted_line += _format_string(base_indent + argument).lstrip() 
            continue

        if argument.strip() == ",":
            formatted_line += f"{argument}"
            continue

        if argument == ").":
            formatted_line += (
                f"\n{argument}" if not formatted_line.endswith("(") else argument
            )
            continue

        if argument.strip().endswith(")"):
            formatted_line += (
                f"\n{base_indent}{argument}"
                if not formatted_line.endswith("(")
                else argument
            )
            continue

        if argument.strip():
            formatted_line += f"\n{total_indent}{argument.strip()}"

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
        # If adding token would make line too long, wrap it
        if is_line_too_long(total_indent + current_line + token):
            formatted_line += f"{total_indent}{current_line.strip()}{string_suffix}\n"
            current_line = string_prefix  # Start new line with prefix

        current_line += f"{token} "

    # Add the final accumulated line
    formatted_line += f"{total_indent}{current_line.strip()} {string_suffix}\n"

    formatted_line += f"{base_indent})"

    return formatted_line


def _generic_format(line: str) -> str:
    base_indent, total_indent = get_indent(line)

    tokens = line.strip().split()

    formatted_line = ""
    current_line = ""
    is_first_line = True

    for token in tokens:
        indent = base_indent if is_first_line else total_indent

        # Reformat token if it exceeds line length by itself
        if is_line_too_long(indent + token):
            token = format_line_code(f"{indent}{token.strip()}")
            token = f"{indent}{token.lstrip()}"

        # If adding token would make line too long, wrap it
        if is_line_too_long(current_line):
            formatted_line += f"{indent}{current_line.strip()}\\\n"
            current_line = ""
            is_first_line = False

        current_line += f"{token.strip()} "

    # Add the final line
    formatted_line += f"{base_indent}{current_line.strip()}\n"

    return formatted_line
