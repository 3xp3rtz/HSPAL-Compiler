From https://esolangs.org/wiki/Hexadecimal_Stacking_Pseudo-Assembly_Language:
"The Hexadecimal Stacking Pseudo-Assembly Language (HSPAL) is a programming language...in which a program is represented by a list of six-digit [hexadecimal] numbers separated by line breaks".
By taking a look at the documentation of the language (found here https://docs.google.com/document/d/1YkG501LjlcrESdrlddE5qEb157w9W0_BeS-zngQJEP4/edit), we can write our own compiler to run HSPAL instructions.

The manner in which I did so was (unnecessarily inefficient but nonetheless) by maintaining a dictionary of arrays indexed hexadecimally to represent stacks, pushing and popping using *append()* and *pop()*, respectively. By running the compiler with print statements denoting the command bring run, we can see that the first segment of code can be shown as:
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
15 300100 - push equals (stack[01] == stack[01]) to stack[01]
16 030000 - skip if (pop stack 00)
17 011234 - go to 1234
3 10ff00 - push one char to stack ff
4 410100 - register = pop stack[01]
5 400200 - push register to stack[02], register = 0
...
```
