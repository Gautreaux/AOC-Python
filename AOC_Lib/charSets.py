CHARSET_HEXADECIMAL_LOWER = ['0','1','2','3','4','5','6','7','8','9', 'a', 'b', 'c', 'd', 'e','f']
CHARSET_HEXADECIMAL_UPPER = ['0','1','2','3','4','5','6','7','8','9', 'A', 'B', 'C', 'D', 'E','F']

# note - this one no longer in order
CHARSET_HEXADECIMAL_BOTH = list(set(CHARSET_HEXADECIMAL_UPPER + CHARSET_HEXADECIMAL_LOWER))

CHARSET_DECIMAL = list(map(lambda x: str(x), range(10)))

CHARSET_OCTAL = list(map(lambda x: str(x), range(8)))

CHARSET_DIGITS = CHARSET_DECIMAL
ALPHABET_LOWER = list(map(lambda x: chr(x + ord('a')), range(26)))
ALPHABET_UPPER = list(map(lambda x: chr(x + ord('A')), range(26)))
ALPHABET_BOTH = ALPHABET_LOWER + ALPHABET_UPPER

REGEX_ALPHABET_LOWER = "[a-z]"
REGEX_ALPHABET_UPPER = "[A-Z]"
REGEX_ALPHABET_BOTH = "[a-zA-Z]"
REGEX_DIGITS = "[0-9]"
REGEX_HEXADECIMAL_LOWER = "[0-9A-F]"
REGEX_HEXADECIMAL_UPPER = "[0-9a-f]"
REGEX_HEXADECIMAL_BOTH = "[0-9a-fA-F]"
REGEX_OCTAL = "[0-7]"