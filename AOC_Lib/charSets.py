CHARSET_HEXADECIMAL_LOWER = ['0','1','2','3','4','5','6','7','8','9', 'a', 'b', 'c', 'd', 'e','f']
CHARSET_HEXADECIMAL_UPPER = ['0','1','2','3','4','5','6','7','8','9', 'A', 'B', 'C', 'D', 'E','F']

CHARSET_DECIMAL = list(map(lambda x: str(x), range(10)))

CHARSET_OCTAL = list(map(lambda x: str(x), range(8)))

CHARSET_DIGITS = CHARSET_DECIMAL
ALPHABET_LOWER = list(map(lambda x: chr(x + ord('a')), range(26)))
ALPHABET_UPPER = list(map(lambda x: chr(x + ord('A')), range(26)))