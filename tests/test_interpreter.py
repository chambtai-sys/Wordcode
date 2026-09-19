import unittest
import io
from wordcode.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def test_arithmetic_and_display(self):
        output = io.StringIO()
        interpreter = Interpreter(output_stream=output)
        source = """
set a to ten
set b to five
display a plus b
display a minus b
display a times b
display a divided by b
"""
        interpreter.run(source)
        lines = output.getvalue().strip().split("\n")
        self.assertEqual(lines, ["15", "5", "50", "2.0"])

    def test_function_execution(self):
        output = io.StringIO()
        interpreter = Interpreter(output_stream=output)
        source = """
define add with x, y
    return x plus y
end
set res to add(three, seven)
display res
"""
        interpreter.run(source)
        self.assertEqual(output.getvalue().strip(), "10")

    def test_repeat_loop(self):
        output = io.StringIO()
        interpreter = Interpreter(output_stream=output)
        source = """set msg to "hi"
repeat three times
    display msg
end
"""
        interpreter.run(source)
        lines = output.getvalue().strip().split("\n")
        self.assertEqual(lines, ["hi", "hi", "hi"])

if __name__ == "__main__":
    unittest.main()
