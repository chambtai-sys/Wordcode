"""
Lexer for Wordcode programming language.
"""

from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    SET = auto()
    TO = auto()
    DISPLAY = auto()
    SAY = auto()
    ASK = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    END = auto()
    WHILE = auto()
    REPEAT = auto()
    TIMES = auto()
    DEFINE = auto()
    FUNCTION = auto()
    WITH = auto()
    PARAMETERS = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()

    # Operators & Comparisons
    PLUS = auto()
    MINUS = auto()
    TIMES_OP = auto()
    DIVIDED_BY = auto()
    MODULO = auto()

    IS = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_OR_EQUAL = auto()
    LESS_OR_EQUAL = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    # Delimiters / Punctuation
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    NEWLINE = auto()
    EOF = auto()

    # Literals & Identifiers
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()


# Map word numbers to integers
NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000
}


class Token:
    def __init__(self, type_: TokenType, value, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source)

    def _peek(self, n: int = 0) -> str:
        if self.pos + n >= self.length:
            return ""
        return self.source[self.pos + n]

    def _advance(self, n: int = 1):
        for _ in range(n):
            if self.pos < self.length:
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1

    def _skip_whitespace_and_comments(self):
        while self.pos < self.length:
            ch = self._peek()
            if ch in ' \t\r':
                self._advance()
            elif ch == '#' or (ch == '/' and self._peek(1) == '/'):
                # Line comment
                while self.pos < self.length and self._peek() != '\n':
                    self._advance()
            else:
                break

    def _peek_phrase(self, phrase: str) -> bool:
        """Check if upcoming text matches phrase case-insensitively at word boundary."""
        substr = self.source[self.pos:self.pos + len(phrase)]
        if substr.lower() != phrase.lower():
            return False

        end_pos = self.pos + len(phrase)
        if end_pos < self.length:
            next_char = self.source[end_pos]
            if next_char.isalnum() or next_char == '_':
                return False
        return True

    def tokenize(self):
        tokens = []

        # Multi-word phrase mappings (longest match first)
        multi_word_tokens = [
            ("is greater than or equal to", TokenType.GREATER_OR_EQUAL),
            ("is less than or equal to", TokenType.LESS_OR_EQUAL),
            ("greater than or equal to", TokenType.GREATER_OR_EQUAL),
            ("less than or equal to", TokenType.LESS_OR_EQUAL),
            ("is not equal to", TokenType.NOT_EQUALS),
            ("not equal to", TokenType.NOT_EQUALS),
            ("is equal to", TokenType.EQUALS),
            ("is greater than", TokenType.GREATER_THAN),
            ("is less than", TokenType.LESS_THAN),
            ("greater than", TokenType.GREATER_THAN),
            ("less than", TokenType.LESS_THAN),
            ("divided by", TokenType.DIVIDED_BY),
            ("modulo by", TokenType.MODULO),
            ("remainder of", TokenType.MODULO),
        ]

        # Single word keyword/operator mappings
        single_word_tokens = {
            "set": TokenType.SET,
            "to": TokenType.TO,
            "display": TokenType.DISPLAY,
            "say": TokenType.SAY,
            "print": TokenType.DISPLAY,
            "ask": TokenType.ASK,
            "if": TokenType.IF,
            "then": TokenType.THEN,
            "else": TokenType.ELSE,
            "end": TokenType.END,
            "while": TokenType.WHILE,
            "repeat": TokenType.REPEAT,
            "times": TokenType.TIMES,
            "define": TokenType.DEFINE,
            "function": TokenType.FUNCTION,
            "with": TokenType.WITH,
            "parameters": TokenType.PARAMETERS,
            "parameter": TokenType.PARAMETERS,
            "return": TokenType.RETURN,
            "plus": TokenType.PLUS,
            "minus": TokenType.MINUS,
            "times": TokenType.TIMES_OP,
            "multiply": TokenType.TIMES_OP,
            "divide": TokenType.DIVIDED_BY,
            "modulo": TokenType.MODULO,
            "is": TokenType.IS,
            "equals": TokenType.EQUALS,
            "and": TokenType.AND,
            "or": TokenType.OR,
            "not": TokenType.NOT,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
        }

        while self.pos < self.length:
            self._skip_whitespace_and_comments()
            if self.pos >= self.length:
                break

            ch = self._peek()

            # Handle newlines explicitly for statement separators
            if ch == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self._advance()
                continue

            # Delimiters
            if ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column))
                self._advance()
                continue
            if ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column))
                self._advance()
                continue
            if ch == ',':
                tokens.append(Token(TokenType.COMMA, ',', self.line, self.column))
                self._advance()
                continue

            # String literals (double or single quotes)
            if ch in ('"', "'"):
                quote = ch
                start_line, start_col = self.line, self.column
                self._advance() # skip opening quote
                val = []
                while self.pos < self.length and self._peek() != quote:
                    if self._peek() == '\\' and self.pos + 1 < self.length:
                        self._advance()
                        escaped = self._peek()
                        if escaped == 'n': val.append('\n')
                        elif escaped == 't': val.append('\t')
                        elif escaped == 'r': val.append('\r')
                        else: val.append(escaped)
                    else:
                        val.append(self._peek())
                    self._advance()
                if self.pos < self.length and self._peek() == quote:
                    self._advance() # skip closing quote
                tokens.append(Token(TokenType.STRING, "".join(val), start_line, start_col))
                continue

            # Number literals (digits)
            if ch.isdigit() or (ch == '.' and self._peek(1).isdigit()):
                start_line, start_col = self.line, self.column
                num_str = ""
                has_decimal = False
                while self.pos < self.length and (self._peek().isdigit() or self._peek() == '.'):
                    if self._peek() == '.':
                        if has_decimal:
                            break
                        has_decimal = True
                    num_str += self._peek()
                    self._advance()
                val = float(num_str) if has_decimal else int(num_str)
                tokens.append(Token(TokenType.NUMBER, val, start_line, start_col))
                continue

            # Multi-word phrase check before single identifiers
            matched_phrase = False
            for phrase, tok_type in multi_word_tokens:
                if self._peek_phrase(phrase):
                    tokens.append(Token(tok_type, phrase, self.line, self.column))
                    self._advance(len(phrase))
                    matched_phrase = True
                    break
            if matched_phrase:
                continue

            # Identifiers, keywords, English word numbers, single-word operators
            if ch.isalpha() or ch == '_':
                start_line, start_col = self.line, self.column
                word = ""
                while self.pos < self.length and (self._peek().isalnum() or self._peek() == '_'):
                    word += self._peek()
                    self._advance()

                lower_word = word.lower()

                if lower_word in NUMBER_WORDS:
                    tokens.append(Token(TokenType.NUMBER, NUMBER_WORDS[lower_word], start_line, start_col))
                elif lower_word in single_word_tokens:
                    tok_type = single_word_tokens[lower_word]
                    tokens.append(Token(tok_type, word, start_line, start_col))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word, start_line, start_col))
                continue

            # Math symbol operators support (+, -, *, /, %, =, ==, !=, >, <, >=, <=)
            if ch in '+-*/%=><!':
                start_line, start_col = self.line, self.column
                if ch == '+' : tokens.append(Token(TokenType.PLUS, '+', start_line, start_col)); self._advance()
                elif ch == '-' : tokens.append(Token(TokenType.MINUS, '-', start_line, start_col)); self._advance()
                elif ch == '*' : tokens.append(Token(TokenType.TIMES_OP, '*', start_line, start_col)); self._advance()
                elif ch == '/' : tokens.append(Token(TokenType.DIVIDED_BY, '/', start_line, start_col)); self._advance()
                elif ch == '%' : tokens.append(Token(TokenType.MODULO, '%', start_line, start_col)); self._advance()
                elif ch == '=' and self._peek(1) == '=':
                    tokens.append(Token(TokenType.EQUALS, '==', start_line, start_col))
                    self._advance(2)
                elif ch == '=':
                    tokens.append(Token(TokenType.TO, '=', start_line, start_col))
                    self._advance()
                elif ch == '!' and self._peek(1) == '=':
                    tokens.append(Token(TokenType.NOT_EQUALS, '!=', start_line, start_col))
                    self._advance(2)
                elif ch == '>' and self._peek(1) == '=':
                    tokens.append(Token(TokenType.GREATER_OR_EQUAL, '>=', start_line, start_col))
                    self._advance(2)
                elif ch == '>':
                    tokens.append(Token(TokenType.GREATER_THAN, '>', start_line, start_col))
                    self._advance()
                elif ch == '<' and self._peek(1) == '=':
                    tokens.append(Token(TokenType.LESS_OR_EQUAL, '<=', start_line, start_col))
                    self._advance(2)
                elif ch == '<':
                    tokens.append(Token(TokenType.LESS_THAN, '<', start_line, start_col))
                    self._advance()
                continue

            # Unrecognized character
            raise SyntaxError(f"Unexpected character '{ch}' at line {self.line}, col {self.column}")

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
