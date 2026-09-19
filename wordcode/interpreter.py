"""
Interpreter / Evaluator for Wordcode programming language.
"""

import sys
from typing import Dict, Any, List, Optional
from wordcode.lexer import Lexer
from wordcode.parser import (
    Parser, Program, Statement, Expression, SetStatement, DisplayStatement,
    IfStatement, WhileStatement, RepeatStatement, FunctionDefStatement,
    ReturnStatement, ExpressionStatement, LiteralExpr, IdentifierExpr,
    BinaryExpr, UnaryExpr, CallExpr, AskExpr
)


class ReturnControl(Exception):
    def __init__(self, value: Any):
        self.value = value


class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value)
            return
        self.values[name] = value  # default to defining in current scope if not present

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"Undefined variable or function '{name}'")


class WordcodeFunction:
    def __init__(self, name: str, params: List[str], body: List[Statement], closure: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def call(self, interpreter: 'Interpreter', args: List[Any]) -> Any:
        env = Environment(self.closure)
        for param, arg in zip(self.params, args):
            env.define(param, arg)

        prev_env = interpreter.environment
        interpreter.environment = env
        try:
            for stmt in self.body:
                interpreter.execute(stmt)
        except ReturnControl as ret:
            return ret.value
        finally:
            interpreter.environment = prev_env
        return None


class Interpreter:
    def __init__(self, output_stream=sys.stdout, input_stream=sys.stdin):
        self.global_env = Environment()
        self.environment = self.global_env
        self.output_stream = output_stream
        self.input_stream = input_stream

    def run(self, source: str) -> Any:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        return self.execute_program(program)

    def execute_program(self, program: Program) -> Any:
        result = None
        for stmt in program.statements:
            result = self.execute(stmt)
        return result

    def execute(self, stmt: Statement) -> Any:
        if isinstance(stmt, SetStatement):
            val = self.evaluate(stmt.value)
            self.environment.assign(stmt.name, val)
            return val

        elif isinstance(stmt, DisplayStatement):
            values = [self.evaluate(expr) for expr in stmt.expressions]
            output_str = " ".join(str(v) if not isinstance(v, bool) else str(v).lower() for v in values)
            self.output_stream.write(output_str + "\n")
            self.output_stream.flush()
            return None

        elif isinstance(stmt, IfStatement):
            cond_val = self.evaluate(stmt.condition)
            if self._is_truthy(cond_val):
                for s in stmt.then_branch:
                    self.execute(s)
            else:
                for s in stmt.else_branch:
                    self.execute(s)
            return None

        elif isinstance(stmt, WhileStatement):
            while self._is_truthy(self.evaluate(stmt.condition)):
                for s in stmt.body:
                    self.execute(s)
            return None

        elif isinstance(stmt, RepeatStatement):
            count_val = self.evaluate(stmt.count)
            if not isinstance(count_val, (int, float)):
                raise TypeError("Repeat count must be a number")
            for _ in range(int(count_val)):
                for s in stmt.body:
                    self.execute(s)
            return None

        elif isinstance(stmt, FunctionDefStatement):
            func = WordcodeFunction(stmt.name, stmt.params, stmt.body, self.environment)
            self.environment.define(stmt.name, func)
            return func

        elif isinstance(stmt, ReturnStatement):
            val = self.evaluate(stmt.value) if stmt.value else None
            raise ReturnControl(val)

        elif isinstance(stmt, ExpressionStatement):
            return self.evaluate(stmt.expression)

        else:
            raise NotImplementedError(f"Unknown statement type: {type(stmt)}")

    def evaluate(self, expr: Expression) -> Any:
        if isinstance(expr, LiteralExpr):
            return expr.value

        elif isinstance(expr, IdentifierExpr):
            return self.environment.get(expr.name)

        elif isinstance(expr, BinaryExpr):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            op = expr.operator

            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '%':
                return left % right
            elif op in ('==', 'equals', 'is'):
                return left == right
            elif op == '!=':
                return left != right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right
            elif op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == 'and':
                return self._is_truthy(left) and self._is_truthy(right)
            elif op == 'or':
                return self._is_truthy(left) or self._is_truthy(right)
            else:
                raise ValueError(f"Unknown binary operator '{op}'")

        elif isinstance(expr, UnaryExpr):
            val = self.evaluate(expr.operand)
            if expr.operator == 'not':
                return not self._is_truthy(val)
            elif expr.operator == '-':
                return -val
            else:
                raise ValueError(f"Unknown unary operator '{expr.operator}'")

        elif isinstance(expr, CallExpr):
            func = self.environment.get(expr.callee)
            if not isinstance(func, WordcodeFunction):
                raise TypeError(f"'{expr.callee}' is not a callable function")
            args = [self.evaluate(a) for a in expr.args]
            return func.call(self, args)

        elif isinstance(expr, AskExpr):
            if expr.prompt:
                prompt_str = str(self.evaluate(expr.prompt))
                self.output_stream.write(prompt_str)
                self.output_stream.flush()
            user_input = self.input_stream.readline().rstrip('\r\n')
            # Attempt numeric conversion if possible
            try:
                if '.' in user_input:
                    return float(user_input)
                return int(user_input)
            except ValueError:
                return user_input

        else:
            raise NotImplementedError(f"Unknown expression type: {type(expr)}")

    def _is_truthy(self, value: Any) -> bool:
        if value is None or value is False:
            return False
        if value is True:
            return True
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True
