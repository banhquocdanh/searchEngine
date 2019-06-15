import re

#TODO: move to config file
diacritic_patterns = {
    (re.compile('[àáảãạăắằẵặẳâầấậẫẩ]'), 'a'),
    (re.compile('[ÀÁẢÃẠĂẮẰẴẶẲÂẦẤẬẪẨ]'), 'A'),
    (re.compile('[đ]'), 'd'),
    (re.compile('[Đ]'), 'D'),
    (re.compile('[èéẻẽẹêềếểễệ]'), 'e'),
    (re.compile('[ÈÉẺẼẸÊỀẾỂỄỆ]'), 'E'),
    (re.compile('[ìíỉĩị]'), 'i'),
    (re.compile('[ÌÍỈĨỊ]'), 'I'),
    (re.compile('[òóỏõọôồốổỗộơờớởỡợ]'), 'o'),
    (re.compile('[ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ]'), 'O'),
    (re.compile('[ùúủũụưừứửữự]'), 'u'),
    (re.compile('[ÙÚỦŨỤƯỪỨỬỮỰ]'), 'U'),
    (re.compile('[ỳýỷỹỵ]'), 'y'),
    (re.compile('[ỲÝỶỸỴ]'), 'Y')
}
#TODO: move to config file
echo_patterns = {
    re.compile('[\{\}\[\]\(\)!@#\$%\^&*<>\?\/,\.\-\+\\|";:\'~`]')
}

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

