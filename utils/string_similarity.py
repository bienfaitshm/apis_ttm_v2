import jellyfish

str1 = "Lubumbashi"
str2 = "lshi"
str3 = "lububashi"


def are_strings_similar(s1: str, s2: str, threshold: int = 2):
    return jellyfish.damerau_levenshtein_distance(s1, s2)


print(are_strings_similar(str1, str2))
print(are_strings_similar(str1, str3))

