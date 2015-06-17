# hermetic

an experimental frankenstein

what if guido was a type theory fan?

a python-like language with hindley-milner-like type system, which is compiled to c.

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
        2
    return out

def wtf(a: Integer) -> String:
    return str(a)

print(f_map(wtf, [2, 4])) # [2 4]
```

However we just reuse Python3's syntax. We try to preserve the spirit and semantics
in many cases, but look at it like a different language.


Implementation
---------------

* hermetic code -> python3 ast (using python3 ast module)
* python3 ast   -> hindley milner ast (easier for type inference, taken from [Robert Smallshire](http://smallshire.org.uk/sufficientlysmall/2010/04/11/a-hindley-milner-type-inference-implementation-in-python/comment-page-1/), with some more Hermetic-specific stuff
* hindley milner ast -> hindley milner typed ast (running type inference and annotating the tree with types)
* hindley milner typed ast -> lower level python-like typed ast (converting back to python/c like multiarg functions and assignment nodes)
* lower level python-like typed ast -> c code (generate c code recursively for each node and based on the core library)

the core library contains some predefined functions, accessible from hermetic and
some template files which implement generic hermetic functions in c
(for example `core/list.c` has placeholders like `%{list_type}` and `%{elem_type}` and
different copies of the functions are generated for each `%{elem_type}` in a program})

options for the compiler:

```bash
bin/hermetic filename.py # compiles it to filename.py.c
bin/hermetic filename.py --to-binary # compiles it to filename.py.c and then invokes
                                     # c99 and generates a binary filename
bin/hermetic filename.py --hm-ast    # show the hindley milner ast
bin/hermetic filename.py --typed-hm-ast # show the typed hindley milner ast
bin/hermetic filename.py --typed-c-ast # show the lower level typed ast
```

the resulting c code is quite amusing:
```c
h_print_HList_HString_HString(
  h_f_map_intREFHString_HList_int_HList_HString(
    &h_wtf_int_HString,
    HList_intOf(2, 2, 4)));
```
yeah, you need a shower now, doncha

syntactic sugar : `[Integer]` for list types, `y >> z` for function types,
`Integer | Float` for union types. we have some extensions to the hindley milner
inference algorithm, so the current type system is probably unsound and weird, but
you have haskell/idris for that

hermetic is just a little kid now and its quite buggy and a proof of concept
however if you're interested, you have some ideas/questions, or you just wanna
hack on it, feel free to use the issues tab here

Alexander Ivanov
