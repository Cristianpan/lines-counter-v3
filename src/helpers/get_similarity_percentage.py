def get_similarity_percentage(str1: str, str2: str) -> float:
    """
    Calculates the similarity percentage between two strings using the Levenshtein distance.

    Returns a value between 0.0 (completely different) and 1.0 (identical).

    Args:
        str1 (str): First string.
        str2 (str): Second string.

    Returns:
        float: Similarity ratio between the two strings.
    """

    if str1 == str2:
        return 1.0

    distance = _get_levenshtein_distance(str1, str2)
    max_length = max(len(str1), len(str2))

    return 1.0 - (distance / max_length)


def _get_levenshtein_distance(str1: str, str2: str) -> int:
    """
    Computes the Levenshtein distance between two strings.

    Args:
        str1 (str): First string.
        str2 (str): Second string.

    Returns:
        int: The Levenshtein distance between the two strings.

    Reference:
        https://www.geeksforgeeks.org/introduction-to-levenshtein-distance/
    """
    len_s1, len_s2 = len(str1), len(str2)

    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[len_s1][len_s2]
