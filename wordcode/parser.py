"""
Parser and Abstract Syntax Tree (AST) definitions for Wordcode.
"""

from typing import List, Optional, Any
from wordcode.lexer import Token, TokenType


# --- AST Nodes ---

class ASTNode:
    pass

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

# Program
class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

# Statements
class SetStatement(Statement):
    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"SetStatement({self.name} = {self.value})"

class DisplayStatement(Statement):
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions

    def __repr__(self):
        return f"DisplayStatement({self.expressions})"

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: List[Statement], else_branch: List[Statement]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfStatement({self.condition}, then={self.then_branch}, else={self.else_branch})"

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.body})"

class RepeatStatement(Statement):
    def __init__(self, count: Expression, body: List[Statement]):
        self.count = count
        self.body = body

    def __repr__(self):
        return f"RepeatStatement({self.count} times, {self.body})"

class FunctionDefStatement(Statement):
    def __init__(self, name: str, params: List[str], body: List[Statement]):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDefStatement({self.name}({self.params}), {self.body})"

class ReturnStatement(Statement):
    def __init__(self, value: Optional[Expression]):
        self.value = value

    def __repr__(self):
        return f"ReturnStatement({self.value})"

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __repr__(self):
        return f"ExpressionStatement({self.expression})"


# Expressions
class LiteralExpr(Expression):
    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f"Literal({repr(self.value)})"

class IdentifierExpr(Expression):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class BinaryExpr(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Binary({self.left} {self.operator} {self.right})"

class UnaryExpr(Expression):
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"Unary({self.operator} {self.operand})"

class CallExpr(Expression):
    def __init__(self, callee: str, args: List[Expression]):
        self.callee = callee
        self.args = args

    def __repr__(self):
        return f"Call({self.callee}, args={self.args})"

class AskExpr(Expression):
    def __init__(self, prompt: Optional[Expression]):
        self.prompt = prompt

    def __repr__(self):
        return f"Ask({self.prompt})"


# --- Parser ---

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self, offset: int = 0) -> Token:
        if self.pos + offset >= len(self.tokens):
            return self.tokens[-1] # EOF token
        return self.tokens[self.pos + offset]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self.tokens[self.pos - 1]

    def _check(self, type_: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type_

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, type_: TokenType, error_message: str) -> Token:
        if self._check(type_):
            return self._advance()
        tok = self._peek()
        raise SyntaxError(f"{error_message} at line {tok.line}, col {tok.column}. Found '{tok.value}'")

    def _skip_newlines(self):
        while self._check(TokenType.NEWLINE):
            self._advance()

    def parse(self) -> Program:
        statements = []
        self._skip_newlines()
        while not self._is_at_end():
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()
        return Program(statements)

    def _statement(self) -> Statement:
        self._skip_newlines()

        if self._match(TokenType.SET):
            return self._set_statement()
        if self._match(TokenType.DISPLAY, TokenType.SAY):
            return self._display_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.REPEAT):
            return self._repeat_statement()
        if self._match(TokenType.DEFINE):
            return self._function_def_statement()
        if self._match(TokenType.RETURN):
            return self._return_statement()

        # Otherwise expression statement (like function call or assignment)
        expr = self._expression()
        self._match(TokenType.NEWLINE)
        return ExpressionStatement(expr)

    def _set_statement(self) -> SetStatement:
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'set'")
        self._consume(TokenType.TO, "Expected 'to' or '=' after variable name in set statement")
        val_expr = self._expression()
        self._match(TokenType.NEWLINE)
        return SetStatement(name_tok.value, val_expr)

    def _display_statement(self) -> DisplayStatement:
        expressions = []
        expressions.append(self._expression())
        while self._match(TokenType.COMMA, TokenType.AND):
            expressions.append(self._expression())
        self._match(TokenType.NEWLINE)
        return DisplayStatement(expressions)

    def _if_statement(self) -> IfStatement:
        condition = self._expression()
        self._match(TokenType.THEN)
        self._skip_newlines()

        then_branch = []
        while not self._check(TokenType.ELSE) and not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._statement()
            if stmt:
                then_branch.append(stmt)
            self._skip_newlines()

        else_branch = []
        if self._match(TokenType.ELSE):
            self._skip_newlines()
            while not self._check(TokenType.END) and not self._is_at_end():
                stmt = self._statement()
                if stmt:
                    else_branch.append(stmt)
                self._skip_newlines()

        self._consume(TokenType.END, "Expected 'end' at end of if statement")
        self._match(TokenType.NEWLINE)
        return IfStatement(condition, then_branch, else_branch)

    def _while_statement(self) -> WhileStatement:
        condition = self._expression()
        self._match(TokenType.THEN) # optional then
        self._skip_newlines()

        body = []
        while not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._statement()
            if stmt:
                body.append(stmt)
            self._skip_newlines()

        self._consume(TokenType.END, "Expected 'end' at end of while loop")
        self._match(TokenType.NEWLINE)
        return WhileStatement(condition, body)

    def _repeat_statement(self) -> RepeatStatement:
        count_expr = self._expression()
        if not self._match(TokenType.TIMES, TokenType.TIMES_OP):
            raise SyntaxError("Expected 'times' in repeat statement")
        self._skip_newlines()

        body = []
        while not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._statement()
            if stmt:
                body.append(stmt)
            self._skip_newlines()

        self._consume(TokenType.END, "Expected 'end' at end of repeat loop")
        self._match(TokenType.NEWLINE)
        return RepeatStatement(count_expr, body)

    def _function_def_statement(self) -> FunctionDefStatement:
        self._match(TokenType.FUNCTION) # optional word function after define
        func_name_tok = self._consume(TokenType.IDENTIFIER, "Expected function name after 'define'")

        params = []
        if self._match(TokenType.WITH) or self._match(TokenType.LPAREN):
            # Parameter list
            if self._peek(-1).type == TokenType.WITH:
                self._match(TokenType.PARAMETERS)

            # Read parameters
            if self._check(TokenType.IDENTIFIER):
                params.append(self._advance().value)
                while self._match(TokenType.COMMA, TokenType.AND):
                    if self._check(TokenType.IDENTIFIER):
                        params.append(self._advance().value)
            if self._peek(-1).type == TokenType.LPAREN:
                self._consume(TokenType.RPAREN, "Expected ')' after parameters")

        self._skip_newlines()
        body = []
        while not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._statement()
            if stmt:
                body.append(stmt)
            self._skip_newlines()

        self._consume(TokenType.END, "Expected 'end' at end of function definition")
        self._match(TokenType.NEWLINE)
        return FunctionDefStatement(func_name_tok.value, params, body)

    def _return_statement(self) -> ReturnStatement:
        if self._check(TokenType.NEWLINE) or self._is_at_end() or self._check(TokenType.END):
            val = None
        else:
            val = self._expression()
        self._match(TokenType.NEWLINE)
        return ReturnStatement(val)


    # Expressions parsing using Pratt Parsing / Operator Precedence

    def _expression(self) -> Expression:
        return self._logic_or()

    def _logic_or(self) -> Expression:
        expr = self._logic_and()
        while self._match(TokenType.OR):
            right = self._logic_and()
            expr = BinaryExpr(expr, "or", right)
        return expr

    def _logic_and(self) -> Expression:
        expr = self._equality()
        while self._match(TokenType.AND):
            right = self._equality()
            expr = BinaryExpr(expr, "and", right)
        return expr

    def _equality(self) -> Expression:
        expr = self._comparison()
        while True:
            if self._match(TokenType.EQUALS, TokenType.IS):
                right = self._comparison()
                expr = BinaryExpr(expr, "==", right)
            elif self._match(TokenType.NOT_EQUALS):
                right = self._comparison()
                expr = BinaryExpr(expr, "!=", right)
            else:
                break
        return expr

    def _comparison(self) -> Expression:
        expr = self._term()
        while True:
            if self._match(TokenType.GREATER_THAN):
                right = self._term()
                expr = BinaryExpr(expr, ">", right)
            elif self._match(TokenType.GREATER_OR_EQUAL):
                right = self._term()
                expr = BinaryExpr(expr, ">=", right)
            elif self._match(TokenType.LESS_THAN):
                right = self._term()
                expr = BinaryExpr(expr, "<", right)
            elif self._match(TokenType.LESS_OR_EQUAL):
                right = self._term()
                expr = BinaryExpr(expr, "<=", right)
            else:
                break
        return expr

    def _term(self) -> Expression:
        expr = self._factor()
        while True:
            if self._match(TokenType.PLUS):
                right = self._factor()
                expr = BinaryExpr(expr, "+", right)
            elif self._match(TokenType.MINUS):
                right = self._factor()
                expr = BinaryExpr(expr, "-", right)
            else:
                break
        return expr

    def _factor(self) -> Expression:
        expr = self._unary()
        while True:
            # Only consume TIMES / TIMES_OP if it's followed by something other than NEWLINE/END
            if (self._check(TokenType.TIMES_OP) or self._check(TokenType.TIMES)) and self._peek(1).type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.END):
                self._advance()
                right = self._unary()
                expr = BinaryExpr(expr, "*", right)
            elif self._match(TokenType.DIVIDED_BY):
                right = self._unary()
                expr = BinaryExpr(expr, "/", right)
            elif self._match(TokenType.MODULO):
                right = self._unary()
                expr = BinaryExpr(expr, "%", right)
            else:
                break
        return expr

    def _unary(self) -> Expression:
        if self._match(TokenType.NOT):
            op = self._unary()
            return UnaryExpr("not", op)
        if self._match(TokenType.MINUS):
            op = self._unary()
            return UnaryExpr("-", op)
        return self._primary()

    def _primary(self) -> Expression:
        if self._match(TokenType.NUMBER):
            return LiteralExpr(self._peek(-1).value)
        if self._match(TokenType.STRING):
            return LiteralExpr(self._peek(-1).value)
        if self._match(TokenType.TRUE):
            return LiteralExpr(True)
        if self._match(TokenType.FALSE):
            return LiteralExpr(False)

        if self._match(TokenType.ASK):
            prompt = None
            if self._check(TokenType.STRING):
                prompt = self._expression()
            return AskExpr(prompt)

        if self._match(TokenType.IDENTIFIER):
            name = self._peek(-1).value
            # Check for function call
            if self._match(TokenType.LPAREN):
                args = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._expression())
                self._consume(TokenType.RPAREN, "Expected ')' after function call arguments")
                return CallExpr(name, args)
            elif self._match(TokenType.WITH): # e.g. run add with five, ten
                args = []
                args.append(self._expression())
                while self._match(TokenType.COMMA, TokenType.AND):
                    args.append(self._expression())
                return CallExpr(name, args)
            return IdentifierExpr(name)

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        tok = self._peek()
        raise SyntaxError(f"Unexpected token '{tok.value}' ({tok.type}) at line {tok.line}, col {tok.column}")
