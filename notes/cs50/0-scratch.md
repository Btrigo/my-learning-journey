# notes - lecture 0 - scratch 





## Escape Sequences in C

When writing strings in C, some characters cannot be typed directly (like a newline or a tab).  
Escape sequences are special combinations that begin with a backslash `\` and represent a single character.

### Common Escape Sequences

| Escape | Meaning | What It Does |
|--------|---------|----------------|
| `\n` | Newline | Moves cursor to the next line (like pressing Enter) |
| `\t` | Horizontal tab | Inserts a tab space |
| `\\` | Backslash | Prints an actual backslash character (`\`) |
| `\"` | Double quote | Allows quotes inside a string literal |
| `\'` | Single quote | Prints a single quote character |
| `\0` | Null terminator | Marks the end of a string in memory |
| `\r` | Carriage return | Moves cursor to the beginning of the current line |
| `\b` | Backspace | Moves cursor one position back |
| `\f` | Form feed | Advances to next “page” on old printers |
| `\v` | Vertical tab | Moves cursor down but not to the start of line (rarely used) |

### Examples

```c
printf("Hello\nWorld");  
// prints:
// Hello
// World
```

```c
printf("1\t2\t3\n");
// prints: 1    2    3
```

```c
printf("She said \"hi\" to me.\n");
// prints: She said "hi" to me.

```

```c
printf("Path: C:\\Users\\Brandon\n");
// prints: Path: C:\Users\Brandon
```