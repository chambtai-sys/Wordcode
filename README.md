```
  __        _____  ____  ____    ____ ___  ____  _____
  \ \  /\  / / _ \|  _ \|  _ \  / ___/ _ \|  _ \| ____|
   \ \/  \/ / | | | |_) | | | || |  | | | | | | |  _|
    \  /\  /| |_| |  _ <| |_| || |__| |_| | |_| | |___
     \/  \/  \___/|_| \_\____/  \____\___/|____/|_____| [BETA]
```

# Wordcode

> An intuitive, readable programming language designed to write code using **only English words**.

Wordcode replaces abstract math symbols and cryptic syntax with natural English phrasing, making code self-explanatory and accessible for beginners while retaining fundamental programming features like variables, functions, conditional logic, and loops.

Wordcode source files use the **`.wc`** file extension.

---

## Key Features

- **Natural English Keywords**: Express math operations and comparisons using words like `plus`, `minus`, `divided by`, `is equal to`, `greater than`, `and`, `or`.
- **Word Numbers**: Native support for English number words such as `one`, `five`, `twenty`, `hundred`.
- **Built-in Functions & REPL**: Interactive REPL mode and script runner supporting `.wc` files.
- **Clean Syntax**: Readable block control structures using simple `if ... then ... else ... end`, `while ... end`, and `repeat ... times ... end`.

---

## File Format

Wordcode source files have the extension **`.wc`**.

Example file: `hello.wc`
```wordcode
# hello.wc
display "Hello, World from Wordcode!"

set name to "Alice"
display "Welcome", name
```

---

## Quick Start & Usage

### 1. Interactive REPL Mode
To launch the interactive REPL, run Wordcode without any arguments:

```bash
python3 -m wordcode
```

### 2. Execute a `.wc` Script
To execute a Wordcode file:

```bash
python3 -m wordcode examples/hello.wc
```

### 3. Check Version
```bash
python3 -m wordcode --version
```

---

## Wordcode Language Syntax Guide

### Variable Assignment
Use `set <variable> to <expression>`:
```wordcode
set counter to ten
set message to "Hello World"
```

### Display Output
Use `display` or `say` to output values to stdout:
```wordcode
display "The total count is", counter
say "Done!"
```

### Basic Arithmetic Operators
| Operator Word | Math Equivalent | Example |
|---|---|---|
| `plus` | `+` | `five plus ten` |
| `minus` | `-` | `twenty minus seven` |
| `times` / `multiply` | `*` | `three times four` |
| `divided by` / `divide` | `/` | `ten divided by two` |
| `modulo by` / `remainder of` | `%` | `ten modulo by three` |

### Comparison Operators
| Comparison Phrase | Math Equivalent | Example |
|---|---|---|
| `is equal to` / `is` / `equals` | `==` | `a is equal to b` |
| `is not equal to` / `not equal to` | `!=` | `a is not equal to b` |
| `is greater than` / `greater than` | `>` | `score is greater than fifty` |
| `is less than` / `less than` | `<` | `count is less than ten` |
| `is greater than or equal to` | `>=` | `age is greater than or equal to eighteen` |
| `is less than or equal to` | `<=` | `val is less than or equal to hundred` |

### Logical Operators
- `and`
- `or`
- `not`

### Conditionals (`if` / `else`)
```wordcode
if score is greater than fifty then
    display "You passed!"
else
    display "Try again."
end
```

### Loops
#### While Loop:
```wordcode
set count to one
while count is less than or equal to five
    display "Count is", count
    set count to count plus one
end
```

#### Repeat Loop:
```wordcode
repeat three times
    display "Hyped for Wordcode!"
end
```

### Functions
Define functions with `define [function] <name> with <parameters>`:
```wordcode
define add with a, b
    return a plus b
end

set result to add(five, ten)
display "Result is", result
```

---

## Examples

Check the `examples/` directory for full Wordcode samples:
- `examples/hello.wc`
- `examples/fizzbuzz.wc`
- `examples/fibonacci.wc`

---

## License

MIT License
