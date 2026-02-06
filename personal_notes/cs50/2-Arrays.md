# Notes - lecture 2 - Arrays 

### What is assembly?

- The computer **does not understand C code directly**.
- C code is first compiled into **assembly** (a low-level, human-readable representation of CPU instructions).
- That assembly is then translated into **machine code (binary)**, which the CPU actually executes.
- Assembly is useful to look at because it shows what the CPU is *really* doing under the hood.

#### Example: C vs. assembly

C code:
```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string name = get_string("What's your name? ");
    printf("hello, %s\n", name);
}
```


assembly code:
```asm
...
main:                                   # label for the main function
    .cfi_startproc                      # debug/unwinding metadata (not core logic)

# BB#0:                                 # "basic block 0" – compiler’s internal label
    pushq   %rbp                        # save old base pointer on the stack
.Ltmp0:
    .cfi_def_cfa_offset 16              # more debug info
.Ltmp1:
    .cfi_offset %rbp, -16               # debug: where %rbp is saved
    movq    %rsp, %rbp                  # set new base pointer for this function frame
.Ltmp2:
    .cfi_def_cfa_register %rbp          # debug info

    subq    $16, %rsp                   # make 16 bytes of space on the stack for locals

    xorl    %eax, %eax                  # set %eax = 0
    movl    %eax, %edi                  # first argument to get_string (in %rdi / %edi)
    movabsq $.L.str, %rsi               # load address of "What's your name? " into %rsi
    movb    $0, %al                     # varargs / calling convention detail
    callq   get_string                  # call get_string("What's your name? ")

    movabsq $.L.str.1, %rdi             # load address of "hello, %s\n" into %rdi
    movq    %rax, -8(%rbp)              # store return value (name pointer) at [rbp-8]
    movq    -8(%rbp), %rsi              # load that pointer back into %rsi (2nd arg)
    movb    $0, %al                     # again, calling convention detail
    callq   printf                      # call printf("hello, %s\n", name)
...
```
- prototype = first line of a function ;
    - e.g. the function get_string will be included in the cs50.h library (#include cs50.h)

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string name = get_string("What's your name? ");
    printf("hello, %s\n", name);
}
```
```bash 
make hello
./hello
```

- 'clang' and 'make' are basically the same thing. they are **COMPILERS**
    - make hello
    - clang hello.c
        - creates default file = a.out
    - ./hello = run the program
    - ./ = run the program
    - ./a.out = run the program 

- compiling code = convert source code into machine code
    - make and clang will make *four* things happen
        1. preprocessing - 
        2. compiling - translated from one language (c) into ***assembly*** code 
        3. assembling - assemble into 0's and 1's 
        4. linking - link all he files that are in this program together so that the program can work
- debugging
    - debug50 = popular debugger 

- bools - 1 byte
- int - 4 bytes - whole numbers 
- long - 8 bytes 
- float - 4 bytes 
- double - 8 bytes 
- char - 1 byte - storese single characters - e.g. '!' 'A' 'B' 
- string - ? bytes - can be equivalent to an array of characters - a string will use an extra byte and install a "0" as a placeholder to indicate where the string ends 

### arrays = data structure
    - an *array* is a sequence of values contiguous in memory
    - use square brackets for arrays []
        - scores[0] = 72;
        - scores[1] = 73;
        - scores[2] = 33;


### characters (char)

- characters get single quotes
- 1 byte in size 


### strings 
- 4 bytes in size 
- strings get double quotes 
- its basically just a sequence of characters 
    - it could also be an *array* - a string can be considered a more precise type *array* specifically containing *chars*
    - an array is a sequence of values 
    the last byte value in a string will be indicated as a *0* because that will signify for the cpu where the string ends 


- keep in mind there will be potential garbage values because it might be remnants of memory that was used prior or other things too. 
- 0 = nul ---- ASCII 
- in C, characters can be stored as intengers 



### what is this program doing?

- Strings are arrays → s[i] accesses the i-th character
- ASCII arithmetic → lowercase to uppercase = subtract 32
- Character comparison using ranges: 'a' to 'z'
- Looping through a string using strlen()

Printing characters one at a time
```c
#include <cs50.h>      // get_string()
#include <stdio.h>     // printf()
#include <string.h>    // strlen()

int main(void)
{
    // Prompt the user for input
    string s = get_string("Before: ");

    // Print label
    printf("After: ");

    // Loop through each character in the string
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // Check if character is lowercase (ASCII 'a' to 'z')
        if (s[i] >= 'a' && s[i] <= 'z')
        {
            // Convert lowercase → uppercase by subtracting 32 in ASCII
            // Example: 'a' (97) becomes 'A' (65)
            printf("%c", s[i] - 32);
        }
        else
        {
            // If not lowercase, print the character unchanged
            printf("%c", s[i]);
        }
    }

    // Move to the next line after output
    printf("\n");
}
```

```
'a' = 97  
'z' = 122  
'A' = 65  
Subtract 32 converts lowercase → uppercase  
``` 

### changing "int main(void)"

```c
#include <cs50.h>    // provides the string type
#include <stdio.h>   // provides printf()

// main now accepts command-line arguments
// argc = argument count
// argv = argument vector (array of strings)
int main(int argc, string argv[])
{
    // Loop over all command-line arguments
    // i starts at 0
    // i < argc ensures we don't read past the array
    for (int i = 0; i < argc; i++)
    {
        // Print the i-th argument (argv[i])
        printf("%s\n", argv[i]);
    }
}
```

- argv = argument value 
- argc = argument count 
```
echo $?  # show me the status code 
```


```c
#include <cs50.h>    // Provides string type
#include <stdio.h>   // Provides printf()

int main(int argc, string argv[])
{
    // Check if the user provided exactly ONE command-line argument
    // argc counts *all* arguments, including the program name
    // So argc should be 2: "./program" + "argument"
    if (argc != 2)
    {
        printf("Missing command-line argument\n");
        return 1;   // Return a non-zero value to signal an error
    }

    // If we reach this line, we know the user gave exactly one argument
    printf("hello, %s\n", argv[1]);

    return 0;       // Return 0 to signal successful execution
}
```

