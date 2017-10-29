# airtight

an experimental frankenstein

what if guido was a type theory fan?
what if we went to an alternate dimension, where python starts like a typed functional language, 
instead of a class-based oop one?

a python-like language with hindley-milner-like type system, which is compiled to c.

With the help of
---------
code by [Robert Smallshire](http://smallshire.org.uk/sufficientlysmall/2010/04/11/a-hindley-milner-type-inference-implementation-in-python/comment-page-1/)
(see below)

Language
---------------

We use the new syntax for annotations in Python3

You can add optional annotations to args and returns:

```python
@template(y, z)
def f_map(f: y >> z, s: [y]) -> [z]:
    out = []
    for i in s:
        out = append(out, f(i))
    return out

def nope(a: Integer) -> Integer:
    return a + 4

print(f_map(nope, [2, 4]))
```

```python
def sum(n: Integer) -> Integer:
    '''sum of the numbers from 0 to n inclusively'''
    result = 0
    for i in range(0, n + 1):
        result += i
    return result

print(sum(2000))
```

owever we just reuse Python3's syntax. We try to preserve the spirit and semantics
in many cases, but look at it like a different language.

you can install it and use it like that
```bash
git clone https://github.com/alehander42/airtight.git
cd airtight
bin/airtight # and
```

Implementation
---------------

* airtight code -> python3 ast (using python3 ast module)
* python3 ast   -> hindley milner ast (easier for type inference, taken from [Robert Smallshire](http://smallshire.org.uk/sufficientlysmall/2010/04/11/a-hindley-milner-type-inference-implementation-in-python/comment-page-1/), with some more Airtight-specific stuff
* hindley milner ast -> hindley milner typed ast (running type inference and annotating the tree with types)
* hindley milner typed ast -> lower level python-like typed ast (converting back to python/c like multiarg functions and assignment nodes)
* lower level python-like typed ast -> c code (generate c code recursively for each node and based on the core library)

The core library contains some predefined functions, accessible from airtight and
some template files which implement generic airtight functions in c
(for example `core/list.c` has placeholders like `%{list_type}` and `%{elem_type}` and
different copies of the functions are generated for each `%{elem_type}` in a program})

options for the compiler:

```bash
bin/airtight filename.py # compiles it to filename.py.c
bin/airtight filename.py --to-binary # compiles it to filename.py.c and then invokes
                                     # c99 and generates a binary filename
bin/airtight filename.py --hm-ast    # show the hindley milner ast
bin/airtight filename.py --typed-hm-ast # show the typed hindley milner ast
bin/airtight filename.py --typed-c-ast # show the lower level typed ast
```

the resulting c code is quite amusing:
```c
a_print_AList_AString_AString(
  a_f_map_intREFAString_AList_int_AList_AString(
    &a_wtf_int_AString,
    AList_intOf(2, 2, 4)));
```
yeah, you need a shower now, doncha

syntactic sugar : `[Integer]` for list types, `y >> z` for function types,
`Integer | Float` for union types. we have some extensions to the hindley milner
inference algorithm, so the current type system is probably unsound and weird, but
you have haskell/idris for that

airtight is just a little kid now and its quite buggy and a proof of concept
however if you're interested, you have some ideas/questions, or you just wanna
hack on it, feel free to use the issues tab here

Alexander Ivanov
