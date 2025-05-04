def get_similarity_percentage(str1: str, str2: str) -> float:
    if str1 == str2:
        return 1

    tokens_str1 = str1.split(" ")
    tokens_str2 = str1.split(" ")

    tokens_zip = zip(tokens_str1, tokens_str2)
    matches = sum(_get_similarity_between_tokens(t1, t2) for t1, t2 in tokens_zip)

    return matches / min(len(str1), len(str2))


def _get_similarity_between_tokens(token1: str, token2: str) -> float:
    return sum(t1 == t2 for t1, t2 in zip(token1, token2))
