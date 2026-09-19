import unittest
from wordcode.lexer import Lexer
from wordcode.parser import Parser, SetStatement, DisplayStatement, IfStatement, LiteralExpr, BinaryExpr

class TestParser(unittest.TestCase):
    def test_parse_set_statement(self):
        source = "set total to twenty plus five\n"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, SetStatement)
        self.assertEqual(stmt.name, "total")
        self.assertIsInstance(stmt.value, BinaryExpr)

    def test_parse_if_statement(self):
        source = "if count is equal to ten then\ndisplay \"ten\"\nelse\ndisplay \"other\"\nend\n"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        self.assertEqual(len(stmt.then_branch), 1)
        self.assertEqual(len(stmt.else_branch), 1)

if __name__ == "__main__":
    unittest.main()
