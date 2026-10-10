# Python Study Notes — October 1, 2026
## CS50P: Functions and Variables

Based on the supplied transcript, covering the introduction through approximately 1:50:10. Instructor: David J. Malan. This is the opening functions-and-variables lecture; the notes below separate what you practiced from topics merely previewed for later.

## 1. The big picture

Programming means expressing instructions precisely enough for a computer to execute. Python is both the language you write and the name commonly used for the program that runs that code: the Python interpreter.

Today's central ideas:

- **Functions** perform tasks, sometimes accept inputs, and sometimes return results.
- **Variables** let you give names to values and reuse them.
- **Types** determine how values behave: text and numbers behave differently.
- **Your own functions** let you organize a program into smaller, reusable pieces.

Later course topics were only introduced: conditionals, loops, exceptions, libraries, unit tests, file input/output, regular expressions, and object-oriented programming. You do not need these to complete today's exercises.

## 2. Writing and running a program

A Python source file is plain text, usually with a `.py` extension. VS Code is an editor; it helps you write code with syntax highlighting, indentation, and a built-in terminal. The interpreter executes the code. These are different jobs.

Create/open a file from a terminal:

```bash
code hello.py
```

Write and save:

```python
print("hello, world")
```

Run from the directory containing the file:

```bash
python3 hello.py
```

The lecture uses `python hello.py`. The command available on your machine may be `python` or `python3`; an activated virtual environment commonly provides `python`. Neither command requires you to navigate inside `.venv`. Your program belongs in your project folder.

**Keep these contexts separate:**

| Context | What belongs there | Example |
|---|---|---|
| Editor / `.py` file | Python source code | `print("hello")` |
| Shell terminal | Commands to run tools | `python3 hello.py` |
| Python interactive prompt, `>>>` | Python expressions/statements | `1 + 1` |

The shell's `$` prompt and Python's `>>>` prompt are indicators, not characters you type as part of commands.

Useful terminal habits: Up arrow recalls previous commands; Tab commonly completes filenames. Enter `python3` alone to start Python's interactive mode, and use `exit()` to leave it. Interactive mode is useful for quick experiments; files preserve code for later reuse.

## 3. Functions, arguments, return values, and side effects

```python
print("hello, world")
```

- `print` is the function name.
- Parentheses call the function.
- `"hello, world"` is an **argument**, a value supplied to that call.
- The quotes mark a string; they do not appear in the printed output.
- Displaying text is a **side effect**: something the function does that is observable beyond handing back a result.

```python
name = input("What's your name? ")
```

`input` displays the prompt, waits for text and Enter, and **returns** the entered text. The assignment saves that result under `name`.

| Function | Typical purpose | Result returned |
|---|---|---|
| `input(...)` | Ask for user input | A string |
| `print(...)` | Display values | `None` |
| `int(...)` | Convert a suitable value to an integer | An integer |
| `float(...)` | Convert a suitable value to a floating-point number | A float |
| `round(...)` | Round a number | A rounded numeric value |

**Printing and returning are different.** Displaying `4` does not automatically make `4` available to the caller as a returned result. A function without an explicit returned value returns `None`.

## 4. Variables and assignment

```python
name = input("What's your name? ")
print(name)
```

Read assignment as: **evaluate the right-hand expression, then bind its result to the name on the left.** A variable is conveniently pictured as a labeled container, although Python more precisely binds names to objects.

`=` means assignment, not an equality test. You can reassign a name:

```python
name = "brandon"
name = name.title()
print(name)  # Brandon
```

Descriptive names help explain intent. `name`, `first`, and `total` often communicate more than `x`, though `x` and `y` are reasonable in a small arithmetic example.

### Quoted text versus a variable

```python
name = "Brandon"
print("name")          # name
print(name)            # Brandon
print("hello, name")   # hello, name
```

Ordinary quoted text is literal. Python does not substitute variable names inside it automatically.

## 5. Strings and four ways to build a greeting

A **string**, type `str`, is text: a character, a word, a sentence, or more. Single and double quotes both work; use a consistent style when practical.

```python
name = "Brandon"

# 1. Concatenation: combine strings into one string
print("hello, " + name)

# 2. Multiple arguments: print inserts a separator
print("hello,", name)

# 3. Two print calls: override the first call's ending
print("hello, ", end="")
print(name)

# 4. F-string: substitute a value inside text
print(f"hello, {name}")
```

All four produce `hello, Brandon` on one line. F-strings are especially useful when inserting several values into a sentence.

### Why spacing differs

`print("hello, " + name)` combines two strings before calling `print`; there is one resulting argument. You supply the space.

`print("hello,", name)` passes two arguments; `print` supplies a space between them by default. Writing `print("hello, ", name)` adds both your space and its separator, producing two spaces.

## 6. Reading function documentation: parameters versus arguments

A **parameter** is an input name declared by a function. An **argument** is the actual value you supply when calling it.

```python
def hello(to):  # to is a parameter
    print(f"hello, {to}")

hello("Brandon")  # "Brandon" is an argument
```

The lecture shows a signature shaped like:

```text
print(*objects, sep=' ', end='\n', file=None, flush=False)
```

For today, focus on:

- `*objects`: `print` accepts multiple values.
- `sep=" "`: a space is placed **between** those values by default.
- `end="\n"`: a newline is placed **after** the output by default.
- Defaults apply when you do not supply an override.

```python
print("A", "B", "C", sep="-")  # A-B-C
print("A", end="")
print("B")                      # AB on the same line
```

`"A"` and `"B"` are positional arguments. `sep="-"` and `end=""` are keyword arguments. Keyword parameters are not inherently optional; these particular parameters have defaults and are optional.

## 7. Escape sequences

Backslashes introduce escape sequences in ordinary string literals.

| Sequence | Meaning |
|---|---|
| `\n` | Newline |
| `\"` | A literal double quote |
| `\\` | A literal backslash |

Two ways to include quotation marks:

```python
print('hello, "friend"')
print("hello, \"friend\"")
```

Both display `hello, "friend"`. Alternating the outer quote style can be easier to read than escaping several quotes.

## 8. F-strings

```python
name = "Brandon"
print(f"hello, {name}")
```

- `f` immediately before the opening quote enables interpolation.
- `{name}` evaluates the expression and inserts its value.
- The braces and leading `f` are syntax, not printed text.

```python
print("hello, {name}")  # hello, {name}
print(f"hello, {name}") # hello, Brandon
```

The `f` in `f"..."` marks a formatted string. The `f` in a numeric format such as `:.2f` means fixed-point formatting. They have different roles.

## 9. Methods and cleaning user input

A **method** is a function accessed through an object, often using dot notation:

```python
name = name.strip()
```

`name` holds the string; the dot accesses `strip`; the parentheses call it. With no arguments, `strip()` removes whitespace from both ends.

| Method | What it does | Example result |
|---|---|---|
| `.strip()` | Remove leading/trailing whitespace | `"  brandon  "` → `"brandon"` |
| `.lstrip()` | Remove leading whitespace | `"  brandon  "` → `"brandon  "` |
| `.rstrip()` | Remove trailing whitespace | `"  brandon  "` → `"  brandon"` |
| `.capitalize()` | Capitalize the first character; lowercase the rest | `"BRANDON TRIGO"` → `"Brandon trigo"` |
| `.title()` | Apply title-style capitalization | `"brandon trigo"` → `"Brandon Trigo"` |
| `.split(" ")` | Split at each literal space into a list | `"Brandon Trigo"` → `["Brandon", "Trigo"]` |

Strings are **immutable**: these methods return new strings rather than changing the original string in place. Keep the returned value when you need it:

```python
name = "  brandon  "
name.strip()             # Result discarded; name still has spaces
name = name.strip()      # Name now refers to the cleaned result
```

### Step-by-step version

```python
name = input("What's your name? ")
name = name.strip()
name = name.title()
print(f"hello, {name}")
```

### Chained version

```python
name = input("What's your name? ").strip().title()
print(f"hello, {name}")
```

Execution order: ask for input → get the string → strip its outer whitespace → title-case that result → assign the final result to `name`.

Chaining works when the intermediate result supports the next method. You cannot blindly chain arbitrary methods together.

**Limits:** `strip()` does not remove spaces in the middle or fix spelling. `title()` is a useful demonstration, but it does not reliably preserve all real-world names and capitalization preferences.

## 10. Splitting and unpacking

Lecture example:

```python
name = input("What's your name? ").strip().title()
first, last = name.split(" ")
print(f"hello, {first}")
```

For `Brandon Trigo`, `split(" ")` returns two pieces. **Unpacking** assigns the first piece to `first` and the second to `last`.

This assumes exactly two pieces. One name, a middle name, or repeated internal spaces can produce a `ValueError` because the number of values does not match the two variables.

Small optional extension:

```python
first, last = name.split(maxsplit=1)
```

With no explicit separator, `split` treats runs of whitespace as separators; `maxsplit=1` splits at most once. This can handle a first name plus a multiword remainder, but it still requires two pieces when unpacking into two variables. Real names need more careful handling than this teaching example.

## 11. Comments and pseudocode

```python
# Ask for the user's name
name = input("What's your name? ")

# Greet the user
print(f"hello, {name}")
```

`#` starts a comment extending to the end of the line. Comments explain intent or decisions to humans; they do not execute.

**Pseudocode** outlines a solution in ordinary language before implementing it:

```python
# Ask for two numbers
# Convert the answers into numeric values
# Add the numbers
# Display the total
```

Use this when a problem feels too big: identify the steps, then implement each step. Comments should help readers understand your code; you do not need to narrate every obvious statement.

Clarification: triple-quoted text is a string literal, not a dedicated multiline-comment syntax. In certain positions it becomes a documentation string, or docstring. For ordinary multiline comments, use `#` on each line.

## 12. Data types and arithmetic

| Type | Meaning | Examples |
|---|---|---|
| `str` | Text | `"Brandon"`, `"12"` |
| `int` | Integer | `-2`, `0`, `12` |
| `float` | Floating-point number | `1.2`, `3.0`, `-0.5` |

`"12"` and `12` are different types. The fact that text looks numeric does not make it a number.

| Operator | Numeric meaning | Example |
|---|---|---|
| `+` | Addition | `2 + 3` → `5` |
| `-` | Subtraction | `5 - 2` → `3` |
| `*` | Multiplication | `3 * 4` → `12` |
| `/` | Division | `6 / 3` → `2.0` |
| `%` | Modulo / remainder | `7 % 3` → `1` |
| `**` | Exponentiation | `3 ** 2` → `9` |

`+` also concatenates strings: `"1" + "2"` produces `"12"`. Ordinary `/` produces a float for integer inputs, too. `^` is not Python's exponentiation operator; use `**` or `pow`.

## 13. The calculator bug: input returns strings

```python
x = input("What's x? ")
y = input("What's y? ")
print(x + y)
```

Entering `1` and `2` prints `12`: the program concatenates strings. Fix it by converting to numbers:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))
print(x + y)
```

Now the result is `3`.

Read `int(input(...))` from the inside outward:

1. `input` asks the question.
2. `input` returns a string such as `"1"`.
3. `int` converts that string into integer `1`.
4. Assignment binds the result to `x`.

To accept decimals:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))
total = x + y
print(total)
```

`int("cat")` and `int("1.2")` raise `ValueError`. `float("cat")` also raises `ValueError`. Error handling comes later; for today's initial examples, enter the expected type of input.

## 14. Rounding versus formatting

### Round a number for further use

```python
rounded = round(4.6)
print(rounded)        # 5

rounded = round(2 / 3, 2)
print(rounded)        # 0.67
```

`round(number)` returns an integer for a float input when no digit count is provided. `round(number, 2)` rounds to two decimal places. The optional digit count is an argument, not square brackets you literally type.

Positive digit counts refer to places after the decimal point: tenths and hundredths. Negative digit counts can round to tens or hundreds: `round(1234, -2)` is `1200`.

Python rounds exact halfway ties to the nearest even choice: `round(2.5)` is `2`; `round(3.5)` is `4`. Floating-point representation can also make some apparent decimal ties behave unexpectedly.

### Format a number for display

```python
z = 2 / 3
print(f"{z:.2f}")  # 0.67
```

`:.2f` displays two digits after the decimal point. It creates formatted text and leaves the numeric value in `z` unchanged.

```python
z = 2.5
print(round(z, 2))  # 2.5
print(f"{z:.2f}")  # 2.50
```

Rounding does not guarantee trailing zeros; fixed-point formatting does.

### Thousands separators

```python
total = 1000
print(f"{total:,}")  # 1,000
```

Optional combination:

```python
total = 1234.5
print(f"{total:,.2f}")  # 1,234.50
```

Within the braces, the colon begins the format specification. The comma requests grouping; `.2f` requests two decimal places. These explicit formats do not automatically switch punctuation when you change your computer's region.

## 15. Float precision

Floats approximate numbers using a finite binary representation. They cannot exactly represent every decimal fraction.

```python
print(0.1 + 0.2)  # 0.30000000000000004
```

This is not a broken calculator: it reflects how floating-point values are stored. Formatting can make the display clearer, but does not make the stored number infinitely precise.

Python integers have arbitrary precision, subject to practical memory/resource limits. Floats have limited precision. A float can represent a whole-number-looking value, such as `3.0`; it is still a float.

## 16. Defining your own functions

```python
def hello():
    print("hello")

hello()
```

- `def` introduces a function definition.
- `hello` is the name you choose.
- `()` declares no parameters here.
- `:` introduces its body.
- Indentation groups statements into the body; use four spaces consistently.
- `hello()` calls the function.

**Defining a function does not execute its body.** It makes the function available to be called later.

### Accept an argument

```python
def hello(to):
    print(f"hello, {to}")

name = input("What's your name? ")
hello(name)
```

If `name` refers to `"Brandon"`, the parameter `to` refers to that supplied value during the function call. The caller's variable name and the function's parameter name do not need to match.

### Supply a default

```python
def hello(to="world"):
    print(f"hello, {to}")

hello()           # hello, world
hello("Brandon")  # hello, Brandon
```

The default is used only when the caller omits the argument.

## 17. Organizing a program with main

```python
def main():
    name = input("What's your name? ").strip().title()
    hello(name)


def hello(to="world"):
    print(f"hello, {to}")


main()
```

`main` is a conventional name, not a special Python keyword that automatically runs.

Execution order:

1. Define `main`; its body does not run yet.
2. Define `hello`; its body does not run yet.
3. Call `main` at the bottom.
4. `main` asks for input and calls `hello`.
5. `hello` prints the greeting.

This works even though `hello` is below `main`, because it exists by the time `main` actually calls it. Functions need to exist when called, not necessarily appear above every textual reference to them.

If you omit the final `main()`, this file defines functions and exits without displaying a greeting.

## 18. Scope: where names are available

A variable assigned inside a function is normally local to that function.

Broken example:

```python
def main():
    name = input("What's your name? ")
    hello()


def hello():
    print(name)  # Cannot access main's local name


main()
```

This raises `NameError` because `hello` cannot directly access the local `name` belonging to `main`.

Pass the value explicitly:

```python
def main():
    name = input("What's your name? ")
    hello(name)


def hello(to):
    print(f"hello, {to}")


main()
```

Parameters make the function's required inputs visible and let it work with different callers.

## 19. Returning values from your own functions

```python
def main():
    x = int(input("What's x? "))
    result = square(x)
    print(f"x squared is {result}")


def square(n):
    return n * n


main()
```

For input `3`: `x` is `3` → call `square(3)` → `n` is `3` inside `square` → calculate `9` → return `9` → assign it to `result` → print it.

Equivalent implementations:

```python
def square(n):
    return n ** 2
```

```python
def square(n):
    return pow(n, 2)
```

`return` hands a value back to the caller and ends that function call. You can save the result, print it, pass it into another function, or use it in later calculations.

### Why using print instead changes the behavior

```python
def square(n):
    print(n * n)

result = square(3)  # Prints 9, but returns None
print(result)      # Prints None
```

Compare with:

```python
def square(n):
    return n * n

result = square(3)  # Returns 9; nothing printed yet
print(result)      # Prints 9
```

## 20. Bugs and debugging

| Problem | Typical symptom | What to inspect |
|---|---|---|
| Missing closing quote or parenthesis | `SyntaxError` | Delimiters and indicated line |
| Calling an undefined function | `NameError` | Spelling; whether definition executed before call |
| Using another function's local variable | `NameError` | Scope; missing parameter/argument |
| Converting unsuitable text to a number | `ValueError` | Entered text and conversion |
| Splitting into the wrong number of pieces | `ValueError` | Input structure and unpacking |
| Adding numeric-looking strings | Wrong result such as `12` | Data types; missing numeric conversion |
| Defining functions without calling them | No output | Final function call |
| Printing when you meant to return | Caller gets `None` | Function body and returned value |

Debugging routine:

1. Save the file and run the version you intend to test.
2. Read the error type and final message; inspect the named file and line.
3. Compare the actual behavior with your intended steps.
4. Follow the values: what was entered, what type is it, and what does each function return?
5. Make one focused correction and rerun.

Errors sometimes point at where Python noticed a problem, rather than where it began. A missing quote or parenthesis on an earlier line can cause a later line to be highlighted.

## 21. Readability and code style

Shorter code is not automatically clearer. Both explicit steps and modest chaining can be good.

Readable calculator:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))
print(x + y)
```

More difficult to inspect:

```python
print(int(input("What's x? ")) + int(input("What's y? ")))
```

Use variables when they explain meaning, make debugging easier, or store a value for reuse. A variable does not become bad merely because it is used once. Avoid nesting so much that the reader has to count parentheses to understand the program.

## 22. Practice checklist — use only today's concepts

Try these from a blank file before looking back at the examples. These are practice prompts, not claims that you already completed them.

### A. Personalized greeting

- [ ] Ask for a name, clean the outer whitespace, and display a greeting with an f-string.
- [ ] Test with `  brandon trigo  `.
- [ ] Rewrite the greeting using multiple arguments to `print`.
- [ ] Explain which version supplies the space and how.

### B. Formatting experiments

- [ ] Print three words separated by ` | `.
- [ ] Use two `print` calls to produce one output line.
- [ ] Print a sentence containing literal quotation marks.
- [ ] Predict what happens when you remove the `f` from an f-string, then test it.

### C. Calculator

- [ ] Ask for two integers and add them.
- [ ] Remove the `int` conversions, enter `1` and `2`, and explain the result.
- [ ] Switch to floats and test `1.2` plus `3.4`.
- [ ] Divide `2` by `3` and display exactly two decimal places.
- [ ] Display `1234.5` as `1,234.50`.

### D. Custom functions

- [ ] Define `hello(to="world")` and call it with and without an argument.
- [ ] Define `square(n)` that returns a result.
- [ ] Save that result and use it in a second calculation.
- [ ] Put the user interaction in `main`, the helper beneath it, and `main()` at the bottom.
- [ ] Explain why removing `main()` stops the interaction.

### E. Small project: order summary

Build a program that asks for a customer's name, a product name, a whole-number quantity, and a decimal unit price. Clean the name, calculate a total in your own function, and print a summary with two decimal places. Use `main` to organize it.

Example interaction:

```text
Customer:   brandon
Product: Cookie
Quantity: 3
Unit price: 2.5
Brandon ordered 3 x Cookie.
Total: $7.50
```

For this introductory exercise, `float` is fine. Real payment calculations need a deliberate money representation, such as integer cents or decimal arithmetic, which is outside this lecture.

## 23. Self-check questions

1. How do VS Code and the Python interpreter differ?
2. What is the difference between `"name"` and `name`?
3. What type does `input` return, even when the user enters digits?
4. Why does `"1" + "2"` produce `"12"`?
5. What do `sep` and `end` control?
6. Why does `name.strip()` alone fail to update `name`?
7. What is the difference between a parameter and an argument?
8. Why does defining `main` not automatically run it?
9. Why must you pass a local value from `main` into a helper?
10. How does `return` differ from `print`?
11. How does `round(z, 2)` differ from `f"{z:.2f}"`?
12. Why can `first, last = name.split(" ")` fail?

## 24. Quick reference

```python
# Input, variables, and string methods
name = input("Name: ").strip().title()

# Output and f-strings
print(f"hello, {name}")
print("A", "B", sep="-", end="\n")

# Numeric conversion
quantity = int(input("Quantity: "))
price = float(input("Price: "))

# Arithmetic, rounding, and formatting
total = quantity * price
rounded = round(total, 2)
print(f"Total: ${total:,.2f}")

# A reusable function with a return value
def square(n):
    return n ** 2
```

**Today's target:** be able to write a small interactive program, explain the type of each value, trace how data moves through function calls, and distinguish displaying a result from returning it.
