# CS50P Study Notes — Loops

**Study session:** October 7, 2026  
**Prepared:** October 10, 2026  
**Sources:** Your supplied David Malan lecture transcript (Loops, approximately 2:46:46–4:07:14) and the available conversation history from our study session. Examples below distinguish lecture concepts from our Hogwarts practice. These are explanations and reconstructed examples, not a verbatim record of your files.

## 1. What a loop does

A loop repeats a block of code. One trip through that block is an **iteration**.

Instead of writing:

```python
print("meow")
print("meow")
print("meow")
```

you can write:

```python
for _ in range(3):
    print("meow")
```

Both print three lines. The loop makes it easier to change how many times the action happens.

**Indentation matters:** the indented statements belong to the loop and repeat. Statements after the loop, at its indentation level, run after it finishes.

## 2. `while`: repeat while a condition is true

David began with a counter:

```python
i = 3

while i != 0:
    print("meow")
    i = i - 1
```

Python checks the condition **before each iteration**.

| Value before the check | Is `i != 0` true? | What happens? |
| --- | --- | --- |
| 3 | Yes | Print; reduce `i` to 2 |
| 2 | Yes | Print; reduce `i` to 1 |
| 1 | Yes | Print; reduce `i` to 0 |
| 0 | No | Leave the loop |

Counting upward works too:

```python
i = 0

while i < 3:
    print("meow")
    i += 1
```

`i += 1` means `i = i + 1`. Python does not use `i++` to increment a counter.

If you forget to change `i`, the condition stays true and the loop keeps running. In a terminal, **Ctrl+C** can interrupt a running program.

## 3. `for`: visit each item

```python
for i in [0, 1, 2]:
    print("meow")
```

Python assigns `0` to `i`, runs the body, assigns `1`, runs it again, then assigns `2` and runs it again. It stops when there are no more items.

You do not have to update `i` yourself in a `for` loop.

### `range()`

Writing a million numbers in a list would be impractical. `range()` describes a sequence of integers:

```python
for i in range(3):
    print(i)
```

Output:

```text
0
1
2
```

**`range(3)` stops before 3.** It produces three values starting at zero. Technically, it is a range object, not a list.

### Why use `_`?

```python
for _ in range(3):
    print("meow")
```

`_` is a variable name. By convention, it tells the reader: “I need to repeat this, but I do not need the current value.” It does not change the loop's behavior.

| Goal | Usual choice |
| --- | --- |
| Repeat until a condition changes | `while` |
| Visit each student in a collection | `for` |
| Repeat a known number of times | `for` with `range()` |
| Keep asking until an answer meets a requirement | Often `while True` with an exit condition |

## 4. `while True`, `break`, `continue`, and `return`

David's positive-number example:

```python
while True:
    n = int(input("What's n? "))
    if n > 0:
        break

for _ in range(n):
    print("meow")
```

`True` always passes the loop's condition. The deliberate exit is `break`, reached when the user provides a positive integer. Zero and negative integers cause another prompt.

**Limit of this lesson's example:** entering something such as `cat` raises `ValueError` at `int(...)`. The later Exceptions lesson adds error handling. A loop alone does not catch that error.

| Statement | Effect |
| --- | --- |
| `break` | Exit the innermost enclosing loop |
| `continue` | Skip the rest of the current iteration and start the next one |
| `return n` | Exit the current function and give `n` back to its caller |

`return` can exit a function directly from inside a loop. You do not need a separate `break` first.

## 5. Combining loops with our own functions

David organized the meowing program into smaller jobs:

```python
def main():
    number = get_number()
    meow(number)


def get_number():
    while True:
        n = int(input("What's n? "))
        if n > 0:
            return n


def meow(n):
    for _ in range(n):
        print("meow")


main()
```

- `main()` connects the steps.
- `get_number()` returns a positive integer.
- `meow(n)` prints that many times.

In `def meow(n):`, `n` is a **parameter**. In `meow(number)`, the value of `number` is the **argument** supplied to the function.

The definitions are processed before the final `main()` call. That is why `main` can call functions whose definitions appear farther down the file.

## 6. Lists: multiple items in order

```python
students = ["Hermione", "Harry", "Ron"]
```

`students` is a variable holding a list. The square brackets create the list; the strings are its items.

| Expression | Value |
| --- | --- |
| `students[0]` | `"Hermione"` |
| `students[1]` | `"Harry"` |
| `students[2]` | `"Ron"` |
| `len(students)` | `3` |

Lists use **zero-based indexes**. Three items have indexes 0, 1, and 2; `students[3]` raises `IndexError` here.

### Looping over the names directly

```python
for name in students:
    print(f"Welcome to Hogwarts, {name}!")
```

During each iteration, `name` holds the next string. `name` is a variable we chose; it is not a special Python keyword.

### Looping over indexes

```python
for i in range(len(students)):
    print(i + 1, students[i])
```

Read the pieces from inside outward:

1. `len(students)` gives 3.
2. `range(3)` provides 0, 1, and 2.
3. `students[i]` retrieves the item at that index.
4. `i + 1` displays a human-friendly position: 1, 2, or 3.

Adding 1 for display does not change the list's indexes. If you only need names, looping over the names directly is easier to read.

## 7. Dictionaries: associate keys with values

```python
students = {
    "Harry Potter": "Gryffindor",
    "Hermione Granger": "Gryffindor",
    "Ron Weasley": "Gryffindor",
    "Draco Malfoy": "Slytherin",
}
```

Each entry associates a **key** on the left with a **value** on the right:

```python
"Draco Malfoy": "Slytherin"
```

Use the key to retrieve the value:

```python
print(students["Draco Malfoy"])  # Slytherin
```

### Your question: how is this different from `name = "Brandon Trigo"`?

```python
name = "Brandon Trigo"
```

This assigns one string to one variable. A dictionary collects several associations inside one object, so you can look up information by a key.

```python
student = {
    "name": "Brandon Trigo",
    "house": "Gryffindor",
}
```

Here, `student` is the variable; `"name"` and `"house"` are string keys inside its dictionary. `student["name"]` retrieves `"Brandon Trigo"`.

### Why braces instead of `dict()`?

Python supports dictionary literals:

```python
student = {"name": "Brandon Trigo"}
```

You can also construct this dictionary with:

```python
student = dict(name="Brandon Trigo")
```

You do not need to call `dict()` when using the literal syntax. `{}` creates an empty dictionary. Braces surrounding key-value pairs create a populated dictionary; braces have other uses too, including expressions inside f-strings.

| Collection | Example | How you retrieve an item |
| --- | --- | --- |
| List | `["Harry", "Ron"]` | Integer index: `students[0]` |
| Dictionary | `{"Harry": "Gryffindor"}` | Key: `students["Harry"]` |

## 8. Your question: where do `name` and `hogwarts_house` come from?

Our practice used:

```python
for name, hogwarts_house in students.items():
    print(f"Welcome to Hogwarts, {name} of {hogwarts_house}!")
```

`.items()` supplies each key-value pair. Python **unpacks** that pair into the two variables you named.

For the first entry, it effectively gives you:

```python
name = "Harry Potter"
hogwarts_house = "Gryffindor"
```

Then it runs the indented body. On the next iteration, it assigns the next pair to those same variables.

These are **loop variables**, not function parameters or arguments. You could name them `student_name` and `house` instead. The order matters: the first receives the key, the second receives the value.

David's transcript also shows direct dictionary iteration:

```python
for name in students:
    print(name, students[name], sep=", ")
```

Looping over a dictionary directly supplies its **keys**. `students[name]` looks up the corresponding value. `.items()` gives you both together.

## 9. A list of dictionaries

When each student has several fields, one dictionary per student keeps related information together:

```python
students = [
    {"name": "Hermione", "house": "Gryffindor", "patronus": "Otter"},
    {"name": "Harry", "house": "Gryffindor", "patronus": "Stag"},
    {"name": "Ron", "house": "Gryffindor", "patronus": "Jack Russell Terrier"},
    {"name": "Draco", "house": "Slytherin", "patronus": None},
]
```

The outer `[...]` is the list. Each inner `{...}` is one dictionary. Each dictionary has the same three keys and that student's values.

```python
for student in students:
    print(student["name"])
```

This time, `student` receives an entire dictionary on each iteration.

```python
students[0]          # Hermione's whole dictionary
students[0]["name"]  # "Hermione"
```

The meaning of a loop depends on what you are looping over:

| Collection after `in` | What the loop variable receives |
| --- | --- |
| List of names | One name string |
| Dictionary | One key |
| Dictionary's `.items()` | One key-value pair, which can be unpacked |
| List of student dictionaries | One student dictionary |

`None` represents the absence of a value in this example. It is not the string `"None"`. Here it records that we have no Patronus value for Draco; it is a data choice, not a claim about every possible interpretation of the character.

## 10. Our Hogwarts output: optional Patronus on the same line

Your preference was to append Patronus information when present and let Draco's greeting stop at Slytherin, with no extra “no Patronus” message.

Using the list above:

```python
for student in students:
    print(
        f"Welcome to Hogwarts, {student['name']} of {student['house']}"
        + (
            f", your patronus is {student['patronus']}"
            if student['patronus']
            else ""
        )
    )
```

Output:

```text
Welcome to Hogwarts, Hermione of Gryffindor, your patronus is Otter
Welcome to Hogwarts, Harry of Gryffindor, your patronus is Stag
Welcome to Hogwarts, Ron of Gryffindor, your patronus is Jack Russell Terrier
Welcome to Hogwarts, Draco of Slytherin
```

The conditional expression follows this pattern:

```python
value_if_true if condition else value_if_false
```

For Hermione, the nonempty Patronus string makes the condition true, so the extra text is selected. For Draco, `None` makes it false, so `""` is selected. Adding an empty string adds no text.

There is one `print()` call per student, so the whole greeting appears on one line. Parentheses let us format the code across several lines without adding newlines to the output.

`.title()` is separate from looping: `"hermione".title()` returns `"Hermione"`. It formats a string; it does not decide which student the loop visits.

## 11. Your question: why does it print horizontally?

```python
print("?" * 4)
```

Output:

```text
????
```

String multiplication first creates one string containing four question marks. There are no newline characters between them. `print()` then prints that string and adds a newline at its end.

Compare:

```python
for _ in range(4):
    print("?")
```

This calls `print()` four times. Each call adds a newline, creating a column.

| Code | Result |
| --- | --- |
| `print("?" * 4)` | One row of four marks |
| Four calls to `print("?")` | Four rows of one mark |
| `print("?", end="")` inside a loop | Marks continue on the same line |
| `print()` | A newline with no text |

David also demonstrated:

```python
print("meow\n" * 3, end="")
```

`\n` supplies a newline after each meow. `end=""` prevents `print()` from adding another newline after that complete string.

## 12. Nested loops: rows and columns

```python
def print_square(size):
    for i in range(size):
        for j in range(size):
            print("#", end="")
        print()


print_square(3)
```

Output:

```text
###
###
###
```

The **outer loop** repeats the job of creating a row. For each outer iteration, the **inner loop** prints every brick in that row.

For size 3:

1. First outer iteration: inner loop prints three bricks; `print()` ends the row.
2. Second outer iteration: a fresh inner loop prints three bricks; `print()` ends the row.
3. Third outer iteration: the same job produces the last row.

Nine bricks are printed: `size * size`.

**The indentation of the empty `print()` is crucial.** It belongs inside the outer loop but outside the inner loop, so it runs once per row. Inside the inner loop it would add a newline after every brick; outside both loops it would add only one newline after all the bricks.

`i` and `j` are names for the current row and column numbers. The code does not use those numbers, so `_` could also be used for these loops.

## 13. Our simpler square using functions

The version we discussed separates “make a row” from “repeat rows”:

```python
def main():
    print_square(4)


def print_square(size):
    for _ in range(size):
        print_row(size)


def print_row(width):
    print("#" * width)


main()
```

`main()` asks for a square of size 4. `print_square` receives that value in its parameter `size`. Each iteration calls `print_row(size)`, which receives 4 in its parameter `width` and prints a row of four bricks.

Output:

```text
####
####
####
####
```

The parameter names can differ because the value is passed in the function call. `size` and `width` are local names belonging to different functions.

This is **abstraction**: give a smaller job a clear name, then use it as a building block. The nested-loop version shows how individual bricks are printed; this version uses string multiplication to build each row.

## 14. Which lesson do these files belong to?

Both the Hogwarts collection examples and the row/square examples belong to **Loops**, even though they also use functions, variables, strings, and conditionals.

Suggested names discussed for organizing them:

```bash
mv loops.py loops_students.py
mv random.py loops_patterns.py
```

These are suggested commands, not a record of completed renames. Run them from the folder containing the files, using the actual current names. `mv` can overwrite an existing destination; `mv -i` asks first.

## 15. Common mistakes to recognize

| Mistake | Why it causes trouble | Correction |
| --- | --- | --- |
| Expecting `range(3)` to include 3 | Its stop value is excluded | Expect 0, 1, 2 |
| Forgetting to update a `while` counter | Condition may never become false | Update the counter or provide an exit |
| Treating a dictionary loop variable as its value | Direct iteration supplies keys | Look up the value or use `.items()` |
| Using `students["name"]` when `students` is a list | A list needs an integer index | Use `student["name"]` inside the loop |
| Using `"None"` for missing data | It is a nonempty string and is truthy | Use `None` |
| Adding a second Patronus print after a full greeting | Extra or duplicated output appears | Build the intended greeting once |
| Putting a row-ending `print()` at the wrong indentation | Newlines occur at the wrong time | End each row after its inner loop |

## 16. Practice and recall

Before running each example, predict the output.

1. What values does `range(4)` supply?
2. In `for student in students:`, how can you tell whether `student` will be a string or a dictionary?
3. What does `.items()` give you that direct dictionary iteration does not?
4. Why does Draco's greeting have no Patronus text in our version?
5. What changes if you remove `end=""` from the nested square's brick print?
6. What is the difference between `break` and `return`?

**Answers:**

1. 0, 1, 2, 3.
2. Inspect the items stored in `students`; the loop supplies each item in turn.
3. Key-value pairs, instead of keys alone.
4. His Patronus value is `None`, so the conditional expression selects an empty string.
5. Each brick gets its own newline; the empty row-ending `print()` also adds blank lines.
6. `break` exits a loop; `return` exits a function and can send a value back.

**Small practice tasks:** add one Hogwarts student with a Patronus and one with `None`; change the square to size 2 and then 5; create a `print_rectangle(height, width)` function that repeats `print_row(width)` exactly `height` times.

**Main idea to remember:** a loop gives you one item or one repetition at a time. Understand what that current item is, then read the indented body as the work done for that one iteration.
