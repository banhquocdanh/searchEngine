import re

PRODUCT_PATHFILE = '../sanbox/product_names.txt'

NUMBER_OF_DOCUMENTS_RESULT = 20 #NUMBER_OF_DOCUMENTS_RESULT < 0 is get all result
K1 = 1.2 #K1 in [1.2, 2.0]
B = 0.75

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
echo_patterns = {
    re.compile('[\{\}\[\]\(\)!@#\$%\^&*<>\?\/,\.\-\+\\|";:\'~`]')
}