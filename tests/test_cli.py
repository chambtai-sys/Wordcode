import unittest
import subprocess
import sys
import os

class TestCLI(unittest.TestCase):
    def test_cli_file_run(self):
        example_path = os.path.join("examples", "hello.wc")
        result = subprocess.run(
            [sys.executable, "-m", "wordcode", example_path],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Hello, World from Wordcode!", result.stdout)

    def test_cli_version(self):
        result = subprocess.run(
            [sys.executable, "-m", "wordcode", "--version"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Wordcode v0.1.0-beta", result.stdout)

if __name__ == "__main__":
    unittest.main()
