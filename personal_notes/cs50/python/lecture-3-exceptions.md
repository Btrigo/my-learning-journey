# CS50 Python — Exceptions Study Notes

**Date:** October 10, 2026  
**Sources:** David Malan’s Exceptions lecture transcript (approximately 4:07:34–4:51:37 in the full-course video) and today’s discussion and practice.  
**Goal:** Understand errors, validate numeric input, retry invalid entries, and organize the program with functions.

> The video chapter label shown in some screenshots said “Floating Point Numbers,” but the supplied transcript and today’s code cover **Exceptions**.

## 1. What is an exception?

An exception signals that something went wrong while Python was executing an operation. For example, `int("cat")` cannot produce an integer and raises `ValueError`.

A syntax mistake is different from an unexpected input at runtime:

```python
# Broken syntax: missing closing quote
print("hello, world)
```

Python cannot start this file until the syntax is fixed:

```python
print("hello, world")
```

**Fix mistakes in the code. Handle expected runtime problems, such as invalid user input.**

### Errors we discussed

| Error | Meaning | Example |
|---|---|---|
| `SyntaxError` | Code does not follow Python’s grammar | Missing quote or colon |
| `ValueError` | An operation receives an unacceptable value | `int("cat")` |
| `NameError` | A name has not been defined | `print(x)` before assigning `x` |
| `TypeError` | An operation receives an incompatible type | `"5" + 2` |
| `ZeroDivisionError` | Division by zero | `5 / 0` |
| `IndexError` | A sequence position does not exist | `students[5]` in a three-item list |
| `KeyError` | A dictionary key does not exist | `student["age"]` when that key is missing |
| `FileNotFoundError` | A requested file cannot be found | Opening a nonexistent file |

A `SyntaxError` in the file itself generally prevents execution, so a `try` around that broken code cannot catch it.

## 2. Input starts as text

```python
text = input("What's x? ")
```

`input()` returns a string. Typing `5` gives the program `"5"`; typing `1/2` gives it `"1/2"`.

**`text` is a variable name we chose.** It is not a keyword. We could use `user_input` instead, provided we change all references consistently.

```python
name = "Brandon Trigo"
```

Here, `name` is a variable and `"Brandon Trigo"` is the assigned string value. A value is an **argument** when supplied to a call, as in `print(name)`.

### Choosing a conversion

| Conversion | Accepts examples | Rejects examples |
|---|---|---|
| `int(text)` | `"5"`, `"-5"`, `"0"` | `"0.5"`, `"1/2"`, `"cat"` |
| `float(text)` | `"5"`, `"-2.5"`, `"0.5"` | `"1/2"`, `"cat"` |
| `Fraction(text)` | `"5"`, `"0.5"`, `"1/2"` | `"1.5/2.5"`, `"cat"` |

`Fraction("1.5/2.5")` fails because the slash-form string requires integer numerator and denominator parts. We solve that by converting the two decimal strings separately.

```python
float("1/2")  # Conversion fails: this is text
1 / 2         # Division succeeds: this is a Python expression
```

Our goal is to accept text representing a number and convert it into a numeric object, while rejecting words. `input()` itself still returns text.

## 3. Catching an error with try and except

```python
try:
    x = int(input("What's x? "))
    print(f"x is {x}")
except ValueError:
    print("x is not an integer")
```

Read this as: “Try these operations. If they raise `ValueError`, run this handler.”

- Enter `5`: conversion succeeds, `x` receives `5`, and Python prints it.
- Enter `cat`: conversion fails, Python skips the rest of `try`, and the handler prints the message.

`try` and `except` are statements, not functions. They do not use call parentheses.

**A handler does not automatically retry input or stop the program.** Once a matching handler finishes, execution normally continues after the `try` statement.

### Catch specific exceptions

Prefer identifying expected errors instead of using a bare `except:`, which can conceal unrelated bugs and catch interruption signals.

Separate handlers let us give separate explanations:

```python
except ValueError:
    print("Enter a valid number.")
except ZeroDivisionError:
    print("The denominator cannot be zero.")
```

If both errors should produce the same response, they can share a handler:

```python
except (ValueError, ZeroDivisionError):
    print("Enter a valid number or fraction.")
```

For our program, separate messages are more useful.

## 4. Why x was not defined

This version has a problem:

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")

print(f"x is {x}")
```

Python must evaluate the right side of `=` before assigning its result to the left side.

For input `cat`:

| Step | What happens |
|---|---|
| `input(...)` | Returns `"cat"` |
| `int("cat")` | Raises `ValueError` |
| Assignment to `x` | Never happens |
| Matching handler | Prints the error message |
| Final `print()` | Tries to read the nonexistent `x`, raising `NameError` |

**This is an assignment failure, not a rule that hides variables inside `try`.** In this fresh program, `x` was never created. If it had already held a value, failed reassignment would leave that previous value intact.

## 5. else means success here

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")
else:
    print(f"x is {x}")
```

The `else` belongs to the `try` statement. It runs when the `try` completes normally without an exception. If the handler runs, this `else` is skipped.

This keeps the risky conversion in `try` and the success action in `else`. Keeping the protected section focused makes it easier to understand which operation raised an error. Exceptions raised inside `else` are not caught by the preceding handlers.

## 6. Retry with while True and break

```python
while True:
    try:
        x = int(input("What's x? "))
    except ValueError:
        print("x is not an integer")
    else:
        break

print(f"x is {x}")
```

- `while True` repeats until something exits the loop.
- Invalid input triggers the message, then the next iteration asks again.
- Valid input reaches `break`, which exits the loop.
- The final print is reached after a successful assignment.

Printing alone does not exit a loop.

### David’s shorter variation

```python
while True:
    try:
        x = int(input("What's x? "))
        break
    except ValueError:
        print("x is not an integer")

print(f"x is {x}")
```

Failed conversion skips `break`; successful conversion reaches it. Both versions work. Choose the structure you can read and explain most clearly—fewer lines are not automatically better.

## 7. Our fraction program

We extended the lecture’s integer example to accept whole numbers, decimals, and fractions whose numerator or denominator can contain decimals.

```python
from fractions import Fraction

while True:
    try:
        text = input("What's x? ")

        if "/" in text:
            numerator, denominator = text.split("/")
            x = Fraction(numerator) / Fraction(denominator)
        else:
            x = Fraction(text)

    except ValueError:
        print("Enter a whole number, decimal, or fraction.")
    except ZeroDivisionError:
        print("Fractions with 0 in the denominator are undefined. Please try again.")
    else:
        break

print(f"x is {float(x)}")
```

### How the fraction parsing works

For input `1.5/2.5`:

```python
text = "1.5/2.5"
```

1. `if "/" in text` checks for a slash.
2. `text.split("/")` returns the list `["1.5", "2.5"]`.
3. `numerator, denominator = ...` unpacks those two items into two variables.
4. `Fraction(numerator)` converts the first decimal string into a numeric fraction.
5. `Fraction(denominator)` converts the second.
6. `/` divides the resulting numbers, producing `3/5`.
7. `float(x)` displays the result as `0.6`.

`numerator` and `denominator` are descriptive variable names we invented. Their names do not perform the math; the conversions and division do.

If no slash exists, `Fraction(text)` converts the single number directly. This `if`/`else` chooses a parsing path; the later `try`/`except`/`else` decides what to do after success or failure.

### Expected behavior

| Input | Result |
|---|---|
| `5` | Prints `x is 5.0` |
| `-2.5` | Prints `x is -2.5` |
| `1/2` | Prints `x is 0.5` |
| `1.5/2.5` | Prints `x is 0.6` |
| `0/69.9` | Prints `x is 0.0` |
| `60/0` or `1/0.0` | Explains undefined division and asks again |
| `cat` or empty input | Gives the valid-number message and asks again |
| `1/2/3` | Unpacking raises `ValueError`; asks again |

**Zero numerator is allowed. Zero denominator is not.** `0/5` equals zero; `5/0` and `0/0` are undefined in ordinary arithmetic.

The program covers these numeric formats, not every mathematical notation. Expressions such as `2+3`, mixed numbers such as `1 1/2`, and symbols such as `π` are not supported. Converting to `float` can round results such as `1/3`; `print(x)` preserves the exact fraction display instead. Extremely large values may exceed the range of the final float conversion.

## 8. Organizing our program with functions

David creates `main()` and `get_int()`. We use `main()` and `get_number()` because ours accepts more than integers.

```python
from fractions import Fraction


def main():
    x = get_number()
    print(f"x is {float(x)}")


def get_number():
    while True:
        try:
            text = input("What's x? ")

            if "/" in text:
                numerator, denominator = text.split("/")
                x = Fraction(numerator) / Fraction(denominator)
            else:
                x = Fraction(text)

        except ValueError:
            print("Enter a whole number, decimal, or fraction.")
        except ZeroDivisionError:
            print("Fractions with 0 in the denominator are undefined. Please try again.")
        else:
            return x


main()
```

### Execution order

1. Python imports `Fraction` and executes the function definitions.
2. The bottom `main()` calls the main function.
3. `x = get_number()` calls our input function and waits for its result.
4. `get_number()` keeps asking until it obtains a valid number.
5. `return x` exits `get_number()` and sends that number to its caller.
6. `main()` assigns the returned number to its own `x` and prints it.

The two `x` variables belong to different functions. They do not need matching names: `main()` could use `number = get_number()` instead. The returned value connects them.

### break versus return versus print versus pass

| Statement | Job |
|---|---|
| `break` | Exits the nearest enclosing loop |
| `return x` | Exits the current function and hands a value to its caller |
| `print(x)` | Displays a value; does not exit the loop or return that value |
| `pass` | Does nothing; serves as a valid placeholder statement |

Because `return` exits the function, it also leaves the loop inside that function. We no longer need `break`.

## 9. Transcript refinements: pass and prompt

### Silently retrying with pass

David shows that an error can be caught without printing a message:

```python
def get_int():
    while True:
        try:
            return int(input("What's x? "))
        except ValueError:
            pass
```

`pass` does not cause repetition by itself. The enclosing loop repeats after the handler ends. We kept explanatory messages in our fraction program so the user knows why an entry was rejected.

### Making a function reusable with a parameter

The transcript’s final refinement lets the caller choose the question:

```python
def main():
    x = get_int("What's x? ")
    print(f"x is {x}")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


main()
```

- `prompt` is the **parameter** in the definition.
- `"What's x? "` is the **argument** supplied in the call.
- `input(prompt)` uses that supplied message.

To apply this refinement to our program, change three lines:

```python
# In main():
x = get_number("What's x? ")

# Function definition:
def get_number(prompt):

# Inside its try block:
text = input(prompt)
```

Keep the rest of our fraction logic the same. Then the same function can ask for another value with `get_number("What's y? ")`.

The transcript also mentions `raise`, which deliberately raises an exception; detailed use was deferred to later study. String checks such as `.isnumeric()` are not a complete replacement for numeric conversion: they do not cover our decimal, negative, and slash-fraction formats.

## 10. Indentation tells Python what belongs together

Use four spaces per indentation level consistently:

```python
def get_number():           # Function definition
    while True:            # Inside the function
        try:               # Inside the loop
            text = input() # Inside try
        except ValueError: # Aligned with try
            pass           # Inside the handler
```

Indentation controls which block a statement belongs to. It does not mean every block creates a separate variable scope: functions create local scopes, while an ordinary `try` block does not.

## 11. Tools and file organization from today

### Run a Python file in the Linux terminal

```bash
python3 exceptions.py
```

### Rename a file

Run from the directory containing the file:

```bash
mv lab.py exceptions.py
```

`mv` can move or rename a file. The first name is the source; the second is the destination. Avoid choosing an existing destination filename unless you intend to replace it.

Both the Hogwarts lists/dictionaries exercise and the rows/squares exercise belong to the Loops lesson. Suggested names were:

```bash
mv loops.py loops_students.py
mv random.py loops_patterns.py
```

These were naming suggestions, not confirmation that all renames were completed.

### Comment out several lines in VS Code

Select the lines and press **Ctrl + /**. Press it again to uncomment them. VS Code adds or removes `#` on each selected line. Triple quotes create strings, not a dedicated Python block comment.

## 12. Quick review and practice

Before reading the answers, explain these aloud:

1. Why does `x = int("cat")` fail to create `x` in a fresh program?
2. When does the `else` associated with `try` run?
3. Why does invalid input cause our program to ask again?
4. What does `"1.5/2.5".split("/")` produce?
5. Why can `return x` replace `break` in our function?
6. Are `text` and `get_number` built into Python?

### Answers

1. The right-hand conversion raises an exception before assignment happens.
2. When the `try` block completes normally without an exception.
3. A handler finishes, then the enclosing `while True` begins its next iteration; it has not reached a successful return.
4. The list `["1.5", "2.5"]`.
5. It exits the entire function, leaving its loop, and returns the valid number to the caller.
6. No. We chose the variable name and defined the function ourselves.

### Next-session drill

- Rebuild the integer retry loop without copying, then explain each line.
- Rebuild `main()` and `get_number()` using the readable structure above.
- Try `cat`, empty input, `60/0`, `0/0`, and then `1.5/2.5` in one run.
- Add the `prompt` parameter and ask for two numbers with different questions.
- Compare `print(x)` with `print(float(x))` using `1/3`.

**Main takeaway:** Convert the input, catch the specific errors you expect, retry when needed, and return a valid number from a function whose job is clearly defined.
