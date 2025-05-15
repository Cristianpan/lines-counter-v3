from re import match


def is_import(line: str) -> bool:
    line = line.strip()
    return line.startswith(("from", "import"))


def is_function_definition(line: str) -> bool:
    line = line.strip()
    return line.startswith("def ")


def is_function_call(line: str) -> tuple[str, str] | None:
    function_regex = r"\s*(?:\w+\(\))*(?:\w+\.)*\w+\("

    match_result = match(function_regex, line)

    if not match_result:
        return None

    function_call = line[: match_result.end()]
    function_rest = line[match_result.end() :]

    return function_call, function_rest


def is_asign(line: str) -> tuple[str, str] | None:
    assignment_regex = r"^\s*\w+\s*(\+|-|\*|/|\\|\*\*|>>|<<|&|\||\^|=)?=\s*"

    match_result = match(assignment_regex, line)

    if not match_result:
        return None

    assignment = line[: match_result.end()]
    expresion = line[match_result.end() :]

    return assignment, expresion


def is_string(line: str) -> tuple[str, str] | None:
    string_regex = r"^(f)?(\"|\')"
    line = line.strip()

    match_result = match(string_regex, line)

    if not match_result:
        return None

    string_prefix = line[: match_result.end()]
    string_sufix = line[-1] # Assumes line ends with closing quote

    return string_prefix, string_sufix
