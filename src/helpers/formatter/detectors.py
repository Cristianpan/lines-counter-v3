from re import match


def is_import(line: str) -> bool:
    line = line.strip()
    return line.startswith(("from", "import"))


def is_function_definition(line: str) -> bool:
    line = line.strip()
    return line.startswith("def ")


def is_function_call(line: str) -> tuple[str, str] | None:
    """
    Detects if a line contains a function call and splits it into the call and the rest.

    Args:
        line (str): A line of code.

    Returns:
            tuple[str, str] | None:
                - A tuple with the function call part and the remaining part of the line if matched.
                - None if no function call is detected.
    """
    function_regex = r"\s*(?:\w+\(\))*(?:\w+\.)*\w+\("

    match_result = match(function_regex, line)

    if not match_result:
        return None

    # Extract function call substring
    function_call = line[: match_result.end()]
    function_rest = line[match_result.end() :]

    return function_call, function_rest


def is_asign(line: str) -> tuple[str, str] | None:
    """
    Checks if a line contains an assignment operation and splits it into assignment and expression.

    Args:
        line (str): A line of code.

    Returns:
            tuple[str, str] | None:
                - A tuple with the assignment part and the expression part if matched.
                - None if no assignment is detected.
    """
    assignment_regex = r"^\s*[\w\s,]+\s*(\+|-|\*|/|\\|\*\*|>>|<<|&|\||\^|=)?=\s*"

    match_result = match(assignment_regex, line)

    if not match_result:
        return None

    # Split into assignment operator and the rest expression
    assignment = line[: match_result.end()].rstrip()
    expresion = line[match_result.end() :]

    return assignment, expresion


def is_string(line: str) -> tuple[str, str] | None:
    """
    Checks if a line starts with a string literal and returns its prefix and suffix quotes.

    Args:
        line (str): A line of code.

    Returns:
        tuple[str, str] | None:
            - A tuple with the string prefix (including 'f' if present) and the closing quote.
            - None if the line doesn't start with a string literal.
    """

    string_regex = r"^(f)?[\"']"
    line = line.strip()

    match_result = match(string_regex, line)

    if not match_result:
        return None

    string_prefix = line[: match_result.end()]
    string_sufix = line[-1]  # Assumes line ends with closing quote

    return string_prefix, string_sufix
