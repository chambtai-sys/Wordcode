"""
CLI interface for Wordcode interpreter.
"""

import sys
import argparse
from wordcode import __version__
from wordcode.interpreter import Interpreter

ASCII_LOGO = f"""
  __        _____  ____  ____    ____ ___  ____  _____
  \\ \\  /\\  / / _ \\|  _ \\|  _ \\  / ___/ _ \\|  _ \\| ____|
   \\ \\/  \\/ / | | | |_) | | | || |  | | | | | | |  _|
    \\  /\\  /| |_| |  _ <| |_| || |__| |_| | |_| | |___
     \\/  \\/  \\___/|_| \\_\\____/  \\____\\___/|____/|_____| [BETA]
                                          v{__version__}
"""


def run_file(filepath: str):
    if not filepath.endswith('.wc'):
        print(f"Warning: File '{filepath}' does not have the recommended .wc extension.")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

    interpreter = Interpreter()
    try:
        interpreter.run(source)
    except Exception as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        sys.exit(1)


def start_repl():
    print(ASCII_LOGO)
    print("Welcome to the Wordcode REPL!")
    print("Type your Wordcode code below. Type 'exit' or 'quit' to exit.\n")

    interpreter = Interpreter()

    while True:
        try:
            line = input("wordcode> ")
            if line.strip().lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            if not line.strip():
                continue

            interpreter.run(line)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Wordcode: A Programming Language made with plain English words."
    )
    parser.add_argument("file", nargs="?", help="Path to the Wordcode script (.wc)")
    parser.add_argument("-v", "--version", action="version", version=f"Wordcode v{__version__}")

    args = parser.parse_args()

    if args.file:
        run_file(args.file)
    else:
        start_repl()


if __name__ == "__main__":
    main()
