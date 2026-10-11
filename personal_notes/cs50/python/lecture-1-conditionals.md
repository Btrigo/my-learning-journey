# CS50P Study Notes — Conditionals

**Prepared:** October 10, 2026  
**Source:** Your supplied David Malan transcript, approximately 1:50:39–2:46:14. These notes explain the lecture and connect it to our later Hogwarts and Exceptions practice. They do not assign an unverified date to your original Conditionals session.

## 1. What conditionals do

A conditional lets a program decide which code to run based on a question. A **Boolean expression** evaluates to `True` or `False`.

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
```

Read it as: “If the value of x is less than the value of y, print this message.” When the condition is false, Python skips the indented block.

`input()` returns a string. `int()` converts suitable text into an integer so these comparisons use numbers. Invalid input can raise `ValueError`; catching that belongs to our Exceptions work.

## 2. Comparison operators

| Operator | Meaning | Example |
| --- | --- | --- |
| `<` | Less than | `3 < 5` is `True` |
| `<=` | Less than or equal to | `5 <= 5` is `True` |
| `>` | Greater than | `7 > 5` is `True` |
| `>=` | Greater than or equal to | `5 >= 5` is `True` |
| `==` | Equal to | `5 == 5` is `True` |
| `!=` | Not equal to | `3 != 5` is `True` |

**One equals sign assigns; two compare.**

```python
name = "Brandon Trigo"       # Assign a value to a variable
print(name == "Brandon Trigo")  # Compare; print True
```

In the assignment, `name` is the variable and `"Brandon Trigo"` is its value. The string becomes an **argument** when you pass it to a function, such as `print("Brandon Trigo")`.

## 3. Colons and indentation

```python
if x < y:
    print("x is less than y")
    print("This also belongs to the if block")

print("This runs after the conditional")
```

The colon starts the block. Indentation identifies its contents. Use four spaces per indentation level. The final print is outside the block, so it runs regardless of the comparison's result.

`else` aligns with its corresponding `if`; its body is indented:

```python
if x == y:
    print("Equal")
else:
    print("Different")
```

There is no condition after `else`. It means “otherwise.”

## 4. Separate `if` statements versus one chain

David first checked each possibility independently:

```python
if x < y:
    print("Less")
if x > y:
    print("Greater")
if x == y:
    print("Equal")
```

All three conditions are checked. For integers, only one of these particular comparisons is true, so only one message prints—but Python still asks all three questions.

An `if`/`elif` chain stops checking its remaining branches once one condition is true:

```python
if x < y:
    print("Less")
elif x > y:
    print("Greater")
else:
    print("Equal")
```

`elif` means “else if.” For these integer inputs, if x is neither less nor greater, it must be equal. The final equality check is unnecessary.

**Completing a branch does not end the whole program.** Execution continues with code following the chain.

| Structure | Behavior |
| --- | --- |
| Separate `if` statements | Check each condition independently; several bodies may run |
| `if` with `elif` branches | Run the first matching body; skip remaining branches |
| Final `else` | Run if none of the preceding conditions matched |

Use separate `if` statements when multiple independent actions should happen. Use a chain when choosing one outcome. You do not always need `elif` or `else`.

## 5. `or`, `and`, and `not`

`or` allows either condition to make the overall condition true:

```python
if x < y or x > y:
    print("Different")
else:
    print("Equal")
```

David simplified this to the actual question being asked:

```python
if x != y:
    print("Different")
else:
    print("Equal")
```

`and` requires both conditions to be true:

```python
if score >= 90 and score <= 100:
    print("A")
```

| First condition | Second condition | `and` | `or` |
| --- | --- | --- | --- |
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

**Extra review:** `not` reverses a Boolean result: `not True` is `False`.

Python also short-circuits these expressions: `and` stops if the first condition is false; `or` stops if the first is true. The remaining condition is then unnecessary.

## 6. Chained comparisons

Python lets you write a range much like you would in mathematics:

```python
if 90 <= score <= 100:
    print("A")
```

This checks that `score` is at least 90 and at most 100. Likewise:

```python
if 80 <= score < 90:
    print("B")
```

For integer scores, this includes 80 through 89. The boundary 90 belongs to A.

## 7. David's grade program: why order matters

Assuming an integer score from 0 through 100:

```python
score = int(input("Score: "))

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")
```

When Python reaches `elif score >= 80`, it already knows the first condition failed. Therefore, score is below 90. You do not have to ask that again.

| Score | First matching branch | Output |
| --- | --- | --- |
| 95 | `score >= 90` | A |
| 89 | `score >= 80` | B |
| 70 | `score >= 70` | C |
| 60 | `score >= 60` | D |
| 59 | `else` | F |

### Why separate `if` statements break this version

```python
score = 95

if score >= 90:
    print("A")
if score >= 80:
    print("B")
if score >= 70:
    print("C")
if score >= 60:
    print("D")
```

95 satisfies all four conditions, so all four letters print. The simplified thresholds rely on an `elif` chain.

Also, checking `score >= 60` first in a chain would give 95 a D. **Check the highest threshold first.**

### Adding a bounds check

This extension removes the lecture's assumption that the user provides a score within the expected range:

```python
if not 0 <= score <= 100:
    print("Score must be between 0 and 100.")
elif score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")
```

It checks the numeric range; it does not catch text that fails `int()` conversion or automatically ask again.

## 8. Modulo: checking even or odd

`%` is the modulo operator. With these positive divisors, it gives the remainder after division.

| Expression | Result |
| --- | --- |
| `4 % 2` | 0 |
| `5 % 2` | 1 |
| `7 % 3` | 1 |
| `0 % 2` | 0 |

An integer is even when dividing it by 2 leaves a remainder of zero:

```python
x = int(input("What's x? "))

if x % 2 == 0:
    print("Even")
else:
    print("Odd")
```

Read `x % 2 == 0` in two steps: calculate the remainder, then compare it to zero. `%` does not mean “percentage” here. Zero and negative even integers also pass this test.

Even/odd classification applies to integers. Our later fraction-input program has a different purpose; accepting fractions does not mean every fraction is even or odd.

## 9. Our own Boolean function

David separated the question from the output:

```python
def main():
    x = int(input("What's x? "))
    if is_even(x):
        print("Even")
    else:
        print("Odd")


def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False


main()
```

`is_even` is a function we define ourselves. In `def is_even(n)`, `n` is the parameter. In `is_even(x)`, the value of x is the argument passed in. If x is 6, n receives 6 for that call.

`return True` gives a Boolean value back to the caller. It does not print the word True. `main()` uses that result as its condition.

### Simplifying the function

David showed a conditional expression:

```python
def is_even(n):
    return True if n % 2 == 0 else False
```

Then he simplified further:

```python
def is_even(n):
    return n % 2 == 0
```

The comparison already produces `True` or `False`, so return its result directly. For 6 it returns True; for 7 it returns False.

All three versions answer the same question. Start with whichever makes the logic clear to you.

**Capitalization matters:** Boolean values are `True` and `False`, not `true`, `false`, or quoted strings.

## 10. Hogwarts decisions with `if` and `or`

```python
name = input("What's your name? ")

if name == "Harry" or name == "Hermione" or name == "Ron":
    print("Gryffindor")
elif name == "Draco":
    print("Slytherin")
else:
    print("Who?")
```

Each side of `or` contains a full comparison.

**Common mistake:**

```python
if name == "Harry" or "Hermione" or "Ron":
    print("Gryffindor")
```

This does not compare name to all three strings. The nonempty string `"Hermione"` is truthy, so the condition succeeds even for an unrelated name. Repeat the comparison as in the correct version.

String equality is case-sensitive: `"harry"` does not equal `"Harry"`.

**Optional extension using our earlier string methods:**

```python
name = input("What's your name? ").strip().title()
```

For these example names, this removes surrounding whitespace and converts input such as `hARRY` to `Harry` before comparison. It is an extension to the lecture example, not a requirement for conditionals.

## 11. Hogwarts decisions with `match`

David showed another way to choose among names:

```python
name = input("What's your name? ")

match name:
    case "Harry" | "Hermione" | "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

- `match name` examines the value of name.
- Each `case` provides a pattern to try.
- `|` separates alternative patterns in this example.
- `case _` matches anything remaining; put it last.
- Only the first matching case body runs. No `break` is required.

If no case matches and there is no catchall, none of the case bodies runs. `match` is available in Python 3.10 and later. Here it demonstrates matching literal strings; the feature also supports more complex patterns.

Keep quotes around literal names. An unquoted name in a pattern can capture a value instead of comparing it to a string.

**Connection to Loops:** `_` has a special wildcard meaning in `case _`. In `for _ in range(3)`, it is an ordinary variable name chosen by convention to signal an unused value.

## 12. Connecting conditionals to our later practice

### Optional Patronus output

In our Loops practice, you wanted Draco's greeting to stop at Slytherin. The same conditional-expression idea selects either Patronus text or an empty string:

```python
student = {"name": "Draco", "house": "Slytherin", "patronus": None}

extra = (
    f", your patronus is {student['patronus']}"
    if student['patronus']
    else ""
)

print(f"Welcome to Hogwarts, {student['name']} of {student['house']}" + extra)
```

Output:

```text
Welcome to Hogwarts, Draco of Slytherin
```

`None` is falsy, so Python selects `""`. A nonempty Patronus string is truthy, so Python selects the extra text. This changes what is printed without needing another print call.

### Choosing how to parse numeric input

In our Exceptions program:

```python
if "/" in text:
    numerator, denominator = text.split("/")
    x = Fraction(numerator) / Fraction(denominator)
else:
    x = Fraction(text)
```

The conditional chooses a parsing path based on whether the input contains `/`. The surrounding `try`/`except` handles failures, such as invalid numeric text or a zero denominator. The surrounding loop repeats the prompt after an error.

These tools work together:

| Tool | Job |
| --- | --- |
| Conditional | Choose an action |
| Loop | Repeat an action |
| Function | Give a reusable job a name |
| Exception handler | Respond to a raised exception |

The snippet assumes `text` already exists and `Fraction` has been imported; it is a piece of our larger program.

## 13. Common mistakes and corrections

| Mistake | What to remember |
| --- | --- |
| `if x = y:` | Assignment and comparison differ; use `==` here |
| Missing `:` | `if`, `elif`, `else`, `match`, and `case` need colons |
| Wrong indentation | Indentation decides which block a line belongs to |
| `else score < 60:` | `else` has no condition; use `elif` for another test |
| Independent `if` statements for overlapping grades | Multiple grades can print; use a chain |
| Lowest grade threshold first | Higher scores match it too; check highest first |
| Assuming `else` always means an error | It means none of this chain's earlier conditions matched |
| Printing a result inside `is_even` instead of returning it | The caller needs a Boolean return value |
| Calling `.strip()` on a Boolean | String methods apply to strings; `is_even` returns a Boolean |

An `else` belongs to its corresponding `if` structure. For example, an `else` after the last of several independent `if` statements does not summarize every earlier check.

## 14. Practice and recall

1. What is the difference between `=` and `==`?
2. With score 95, how many bodies run in the correct grade chain?
3. Why can its B branch omit an upper bound?
4. What does `9 % 2` evaluate to?
5. What does `is_even(8)` return in the shortest version?
6. What happens if a name matches no case and there is no `case _`?
7. Does completing an `if` branch end the entire program?

**Answers:**

1. Assignment versus equality comparison.
2. One: the A branch.
3. Reaching it means the A condition already failed, so score is below 90.
4. 1.
5. `True`.
6. No case body runs; execution continues after the match statement.
7. No. Execution continues after the conditional unless something such as `return` exits the current function.

**Hands-on practice:**

- Run the grade program with 59, 60, 69, 70, 79, 80, 89, 90, and 100. These boundary values reveal mistakes better than testing only 95.
- Test the bounds-check extension with -1 and 101.
- Run the parity program with 0, 1, 2, -3, and -4.
- Add a known student to the Hogwarts branches, then test an unknown name.
- Before running each case, write down the expected result and the branch that should produce it.

**Main idea to remember:** ask what each condition means, whether previous checks already ruled something out, and whether you want one outcome or several independent actions.
