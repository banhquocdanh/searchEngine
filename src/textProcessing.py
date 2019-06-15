import re
from config import diacritic_patterns, echo_patterns

#remove diacritics in VietNamese
def removeDiacritics(text):
    result = text
    for item in diacritic_patterns:
        regex, replace = item
        result = regex.sub(replace, result)
    return result

#remove echo characters
def removeEchoCharacters(text):
    result = text
    for regex in echo_patterns:
        result = regex.sub('', result)
    return result

