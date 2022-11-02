# Writeup for `Heard you like stacks`, UDCTF 2022
From the [`esolangs.org`](https://esolangs.org/wiki/Hexadecimal_Stacking_Pseudo-Assembly_Language) page on HSPAL:

*"The Hexadecimal Stacking Pseudo-Assembly Language (HSPAL) is a programming language...in which a program is represented by a list of six-digit [hexadecimal] numbers separated by line breaks".*

By taking a look at the [documentation](https://docs.google.com/document/d/1YkG501LjlcrESdrlddE5qEb157w9W0_BeS-zngQJEP4/edit) of the language, we can write our own compiler to run HSPAL instructions.

The manner in which I did so was ~~using stdin instead of reading files but nonetheless~~ by maintaining a dictionary of arrays indexed hexadecimally to represent stacks, pushing and popping using *append()* and *pop()*, respectively. 

# Going through the code

By running the compiler with print statements denoting the command bring run, we can see that the first segment of code can be shown as:
```
0 200027 - r = 0027
1 400100 - push register to stack[01], register = 0
2 001234 - make label 1234
3 10ff00 - push one char to stack ff
4 410100 - register = pop stack[01]
5 400200 - push register to stack[02], register = 0
6 200001 - r = 0001
7 400100 - push register to stack[01], register = 0
8 410200 - register = pop stack[02]
9 400100 - push register to stack[01], register = 0
10 220100 - push sub stack[01], stack[01] to stack[01]
11 420100 - register = last elem of stack[01]
12 400100 - push register to stack[01], register = 0
13 200000 - r = 0000
14 400100 - push register to stack[01], register = 0
15 300100 - push equals (stack[01] == stack[01]) to stack[00]
16 030000 - skip if (pop stack 00)
17 011234 - go to 1234
3 10ff00 - push one char to stack ff
4 410100 - register = pop stack[01]
5 400200 - push register to stack[02], register = 0
...
```
The program loops after reaching instruction #17, which jumps back to instruction #3 if #16 results in not skipping the following command. Reading the code more closely, #15 pushes a value to `stack[00]` which is non-zero if the top two elements on `stack[01]` are the same. #13 and #14 pushes an element of `0x0` onto `stack[01]`, #11-12 duplicate the top element of `stack[01]`, #8-10 subtracts the the top element of `stack[01]` from `stack[02]`, pushing the result back onto `stack[01]`, #6-7 pushes `0x1` onto `stack[01]`, #4-5 moves the top element of `stack[01]` to `stack[02]`, and finally #3 simply adds a character from input to `stack[ff]`. Not within the loop is #0-1 which adds `27` to the top of `stack[01]` and #2 which labels an instruction.
Reordering these and simplifying it leaves us with:
```
0-1   Add 0x27 to stack[01]
2     Mark loop
3     Add input char to stack[ff]
4-5   Move top of stack[01] into stack[02]
6-7   Push 1 onto stack[01]
8-10  Subtract stack[01] from stack[02]
11-12 Duplicate top of stack[01]
13-14 Add 0 to stack[01]
15    Check if top two elements on stack[01] are equal, push result to stack[01]
16    Loop if stack[01] is non-zero
```
Simplifying further and running through the first loop with the we can attain:
```
0-1   Add 0x27 to stack[01]
Loop: 
3     Get input
4-5   Move 0x27 to stack[02]
6-10  Subtract 1 from stack[02], move result to stack[01]
11-12 Duplicate stack[01]
13-15 Check if top element of stack[01] is equal to 0
16    If not, jump back to beginning of loop
```
This seems very much like a for loop, once we simplify one final time. (I've removed unrelated commands for readability.)
```
0-1   Add 0x27 to stack[01]   Iterator
Loop:
4-5   Move iterator to stack[02]
6-10  Subtract 1 from iterator
13-16 If iterator == 0, jump to beginning of loop
```
From this, we can gather that we will read in `0x27` or 39 characters onto `stack[ff]`, but in reverse order, as we are pushing onto a stack. Looking past the input, we can read through #17-33:
```
18 410100 - register = pop stack[01]
19 200048 - r = 0048
20 40ff00 - push register to stack[ff], register = 0
21 22ff00 - push sub stack[ff], stack[ff] to stack[ff]
22 21ff00 - push add stack[ff], stack[ff] to stack[ff]
23 200000 - r = 0000
24 40ff00 - push register to stack[ff], register = 0
25 30ff01 - push equals (stack[ff] == stack[ff]) to stack[ff]
26 030100 - skip if (pop stack 01)
27 04d34d - exited with status code d34d
28 42ff00 - register = last elem of stack[ff]
29 40ff00 - push register to stack[ff], register = 0
30 23ff00 - push mult stack[ff], stack[ff] to stack[ff]
31 202971 - r = 2971
32 40ff00 - push register to stack[ff], register = 0
33 30ff01 - push equals (stack[ff] == stack[ff]) to stack[ff]
34 030100 - skip if (pop stack 01)
35 04d34d - exited with status code d34d
```
Roughly translating this, we attain:
```
18    Pop iterator off of stack[01]
19-21 Set top of stack[ff] to 0x48 - top of stack[ff]
22    Sum top two elements of stack[ff]
23-25 Set top of stack[01] to whether top of stack[ff] is equal to 0
26-27 If stack[01] is 0, exit the program
28-30 Square last element of stack[ff]
31-32 Push 0x2971 onto stack[ff]
33-35 Exit if last two elements of stack[ff] are not equal
```
Looking at lines #26-27, the program will exit if the top of `stack[01]` is `0x0`, which is set by whether the top two elements of `stack[ff]` are equal. 
Let's try simplifying the code again:
```
18    Remove for loop iterator from stack[01]
19-22 Set stack[ff] to (0x48 - top of stack[ff] + second from top of stack[ff])
23-27 Exit if top element of stack[ff] is not 0
28-35 Exit if stack[ff]^2 != 0x2971
```
From the flag format of `UDCTF{flag}`, we know that the last character of the flag should be `}`, also known as character `125`/`0x7b`. Using this, we can calculate what the second last character of the flag will be. As the top element of the stack after the operations `0x48 - top of stack[ff] (which is 125/0x7b) + second on stack[ff]` must equal 0, we can get that `0x48 - 0x7b + second on stack[ff] = 0`. Solving this leaves us with `second on stack[ff] = 0x33`. This resolves #18-27, so let's take a look at #28-35.

Since the last element of the stack squared must equal, we can calculate the square root in order to get what `stack[ff]` should be: `103`, or `g`. 

Let's look briefly at the next several lines.
```
35 20001b - r = 001b
36 400300 - push register to stack[03], register = 0
37 20000e - r = 000e
38 401f00 - push register to stack[1f], register = 0
39 200009 - r = 0009
40 407c00 - push register to stack[7c], register = 0
41 200015 - r = 0015
42 40e600 - push register to stack[e6], register = 0
...
```
These all seem to be pushing random numbers on to seemingly random stacks. Let's just put these all aside for now, keeping track of what is added to which stack in a separate document, such as in `stacks.content`. Take a look at the code after these `r = x, push register to...` instructions up until the next `exit` command:
```
109 226c00 - push sub stack[6c], stack[6c] to stack[6c]
110 41ff00 - register = pop stack[ff]
111 406c00 - push register to stack[6c], register = 0
112 306c01 - push equals (stack[6c] == stack[6c]) to stack[6c]
113 030100 - skip if (pop stack 01)
114 04dead - exited with status code dead
```
Looking through our document of stacks, we find that `stack[6c] = ['0x2', '0x70']`. As #109 subtracts the second from the top from the top, or `0x70 - 0x2`, the pushed result will be `0x6e`. In lines #110 to 114, we skip the `exit` command only if the register set from the top of `stack[ff]` is equal to the top of `stack[6c]`, which we know to be `0x6e`, therefore we know the next last character in the flag is `0x6e`, or `n`.

The rest of the operations check in a similar manner, where a register is pushed onto a stack with a value, an operation is performed between them, and equated to the next last character of the flag. If they match, the program continues, thus the next last character of the flag must be the result of the operation between the register and the existing element on the stack in question.

Running through the entire code, we finally reach the end after calculating the correct flag and get a fun easter egg of the register being set to `0x1337` before exiting the program with exit code `0000` instead of `dead` or `d34d` and yielding our flag: `UDCTF{h4v1ng_s0_much_fun_w1th_350l4ng5}`.
