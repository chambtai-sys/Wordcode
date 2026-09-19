import unittest
from wordcode.lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    def test_keywords_and_identifiers(self):
        source = "set x to ten"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        values = [t.value for t in tokens]
        self.assertEqual(types, [TokenType.SET, TokenType.IDENTIFIER, TokenType.TO, TokenType.NUMBER, TokenType.EOF])
        self.assertEqual(values, ["set", "x", "to", 10, ""])

    def test_phrases_and_operators(self):
        source = "x is less than or equal to y plus five"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(types, [
            TokenType.IDENTIFIER,
            TokenType.LESS_OR_EQUAL,
            TokenType.IDENTIFIER,
            TokenType.PLUS,
            TokenType.NUMBER,
            TokenType.EOF
        ])

    def test_string_literal(self):
        source = 'display "Hello World"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.DISPLAY)
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].value, "Hello World")

if __name__ == "__main__":
    unittest.main()
