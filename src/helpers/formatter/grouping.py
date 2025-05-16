from re import match


def group_strings(tokens: list[str]) -> list[str]:
    """
    Groups tokens that represent string literals (including multi-token strings).

    Args:
        tokens (list[str]): A list of code tokens.

    Returns:
        list[str]: A list where string tokens are grouped into single entries.
    """
    result = []
    is_string = False
    type_string = ""
    buffer = []

    for token in tokens:
        clear_token = token.replace("f", "").strip()

        if not is_string:
            if clear_token.startswith(('"', "'")):
                is_string = True
                # Detect string type: " or '
                type_string = clear_token[:1]
                buffer.append(token)
            else:
                result.append(token)
        else:
            buffer.append(token)

        if clear_token.endswith(type_string) and is_string:
            result.append(" ".join(buffer))
            buffer.clear()
            is_string = False
            type_string = ""

    return result


def group_functions(tokens: list[str]) -> list[str]:
    """
    Groups tokens that form function calls.

    Args:
        tokens (list[str]): A list of code tokens.

    Returns:
        list[str]: A list where function calls are grouped into single entries.
    """
    result = []
    is_function = False
    function_regex = r"(?:\w+\(\))*(?:\w+\.)*\w+\("
    buffer = []

    for token in tokens:
        if not is_function:
            # Match start of function call
            if match(function_regex, token):
                is_function = True
                buffer.append(token)
            else:
                result.append(token)
        else:
            buffer.append(token)

        if token.strip().endswith(")") and is_function:
            result.append(" ".join(buffer))
            buffer.clear()
            is_function = False

    return result
