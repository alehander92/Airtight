#!/usr/bin/env python
'''
.. module:: hindley_milner
   :synopsis: An implementation of the Hindley Milner type checking algorithm
              based on the Scala code by Andrew Forrest, the Perl code by
              Nikita Borisov and the paper "Basic Polymorphic Typechecking"
              by Cardelli.
.. moduleauthor:: Robert Smallshire
'''
'''adapted for hermetic from Alexander Ivanov
   original version from
   http://smallshire.org.uk/sufficientlysmall/2010/04/11/a-hindley-milner-type-inference-implementation-in-python/comment-page-1/
'''

import copy

# from __future__ import print_function

#=======================================================#
# Class definitions for the abstract syntax tree nodes
# which comprise the little language for which types
# will be inferred

class Top:
    h_type = None
    h_native = False
    def annotate(self, h_type):
        self.h_type = h_type
        return h_type

class Lambda(Top):
    """Lambda abstraction"""

    def __init__(self, v, body, expected=None, return_expected=None):
        self.v = v
        self.body = body
        self.expected = expected
        self.return_expected = return_expected

    def __str__(self):
        return "(fn {v}@{t} => {body})".format(v=self.v,
                                             t=self.h_type.types[0] if self.h_type else '',
                                             body=self.body)

class LambdaNoArgs(Top):
    '''Lambda with no args'''

    def __init__(self, body):
        self.body = body

    def __str__(self):
        return "(fn => {body})".format(body=self.body)

class aList(Top):
    """List"""

    def __init__(self, items):
        self.items = items

    def __str__(self):
        return "[{items}]".format(
                items=', '.join(str(item) for item in self.items))

class If(Top):
    def __init__(self, test, body, orelse):
        self.test = test
        self.body = body
        self.orelse = orelse

    def __str__(self):
        return 'If({0}) {1} {2}'.format(str(self.test), str(self.body), str(self.orelse))

class Body(Top):
    """A list of expressions"""

    def __init__(self, expression, other):
        self.expression = expression
        self.other = other

    def __str__(self):
        return "(@{expression}\n  {other})".format(
            expression=str(self.expression),
            other=str(self.other))

class Ident(Top):
    """Identifier"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{name}@{type}'.format(name=str(self.name), type=str(self.h_type))

class anInteger(Ident):
    pass

class aString(Ident):
    def __init__(self, name):
        self.name = "'%s'" % name

class aBoolean(Ident):
    pass

class aFloat(Ident):
    pass

class Apply(Top):
    """Function application"""

    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg

    def __str__(self):
        return "({fn} {arg})".format(fn=self.fn, arg=self.arg)


class Let(Top):
    """Let binding"""

    def __init__(self, v, defn, body):
        self.v = v
        self.defn = defn
        self.body = body

    def __str__(self):
        return "(let {v} = {defn} in {body})".format(v=self.v, defn=self.defn, body=self.body)

def Letmany(vs, defns, body):
    if len(vs) == 1:
        return Let(vs[0], defns[0], body)
    else:
        return Let(vs[0], defns[0], Letmany(vs[1:], defns[1:], body))

class Letrec(Top):
    """Letrec binding"""

    def __init__(self, v, defn, body):
        self.v = v
        self.defn = defn
        self.body = body

    def __str__(self):
        return "(letrec {v} = {defn} in {body})".format(v=self.v, defn=self.defn, body=self.body)



#=======================================================#
# Exception types

class NotUnifiedError(Exception):
    """Raised if the unification didn't happen"""

    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)

class TypeError(Exception):
    """Raised if the type inference algorithm cannot infer types successfully"""

    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)


class ParseError(Exception):
    """Raised if the type environment supplied for is incomplete"""
    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)



#=======================================================#
# Types and type constructors

class TypeVariable(object):
    """A type variable standing for an arbitrary type.

    All type variables have a unique id, but names are only assigned lazily,
    when required.
    """

    next_variable_id = 0

    def __init__(self):
        self.id = TypeVariable.next_variable_id
        TypeVariable.next_variable_id += 1
        self.instance = None
        self.__name = None

    next_variable_name = 'a'

    def _getName(self):
        """Names are allocated to TypeVariables lazily, so that only TypeVariables
        present
        """
        if self.__name is None:
            self.__name = TypeVariable.next_variable_name
            TypeVariable.next_variable_name = chr(ord(TypeVariable.next_variable_name) + 1)
        return self.__name

    name = property(_getName)

    def __str__(self):
        if self.instance is not None:
            return str(self.instance)
        else:
            return str(self.name)

    def __repr__(self):
        return "TypeVariable(id = {0})".format(self.id)


class TypeOperator(object):
    """An n-ary type constructor which builds a new type from old"""

    def __init__(self, name, types):
        self.name = name
        self.types = types

    def __str__(self):
        num_types = len(self.types)
        # print(self.__class__.__name__, self.postfix, len(self.types))

        if num_types == 0:
            return str(self.name)
        elif num_types == 1:
            return '[{0}]'.format(str(self.types[0]))
        # elif num_types == 2 and expected:
        #     return "({0}:{3} {1} {2}:{4})".format(str(self.types[0]), str(self.name), str(self.types[1]), str(self.expected[0]), str(self.expected[1]))
        elif num_types == 2:
            return "({0} {1} {2})".format(str(self.types[0]), str(self.name), str(self.types[1]))
        else:
            return "{0} {1}" % (str(self.name), ' '.join(map(str, self.types)))


class Function(TypeOperator):
    """A binary type constructor which builds function types"""

    def __init__(self, from_type, to_type):
        super(Function, self).__init__("->", [from_type, to_type])

class Union(object):
    def __init__(self, *types):
        self.types = types

    def __str__(self):
        return ' | '.join(str(t) for t in self.types)

def Multi_Apply(ident, args):
    # print(ident, args)
    # input()
    if len(args) == 1:
        return Apply(ident, args[0])
    else:
        return Apply(Multi_Apply(ident, args[:-1]), args[-1])

def Multi_Lambda(args, body, expected=None):
    if not expected:
        expected = None
        rest_expected = []
    else:
        rest_expected = expected[1:]
        expected = expected[0]

    if len(args) > 1:
        return Lambda(
            args[0],
            Multi_Lambda(args[1:], body, expected=rest_expected),
            expected=expected)
    elif len(args) == 0:
        return LambdaNoArgs(body)
    else:
        return Lambda(args[0], body, expected=expected, return_expected=None if rest_expected == [] else rest_expected[0])

def Multi_Function(types):
    if len(types) == 2:
        return Function(types[0], types[1])
    else:
        return Function(types[0], Multi_Function(types[1:]))

class List(TypeOperator):
    """Builds list types"""

    def __init__(self, element_type):
        super(List, self).__init__("list", [element_type])

    def __str__(self):
        return '[{0}]'.format(str(self.types[0]))

# Basic types are constructed with a nullary type constructor
Integer = TypeOperator("Integer", [])  # Basic integer
Bool    = TypeOperator("Bool", []) # Basic bool
Float   = TypeOperator("Float", []) # Basic float
String  = TypeOperator("String", []) # Basic string




#=======================================================#
# Type inference machinery

def analyse(node, env, non_generic=None):
    """Computes the type of the expression given by node.

    The type of the node is computed in the context of the context of the
    supplied type environment env. Data types can be introduced into the
    language simply by having a predefined set of identifiers in the initial
    environment. environment; this way there is no need to change the syntax or, more
    importantly, the type-checking program when extending the language.

    Args:
        node: The root of the abstract syntax tree.
        env: The type environment is a mapping of expression identifier names
            to type assignments.
            to type assignments.
        non_generic: A set of non-generic variables, or None

    Returns:
        The computed type of the expression.

    Raises:
        TypeError: The type of the expression could not be inferred, for example
            if it is not possible to unify two types such as Integer and Bool
        ParseError: The abstract syntax tree rooted at node could not be parsed
    """

    print(node, type(node))
    # input()

    if non_generic is None:
        non_generic = set()

    if isinstance(node, Ident):
        return node.annotate(getType(node.name, env, non_generic))
    elif isinstance(node, If):
        unify(analyse(node.test, env, non_generic), Bool)
        node.test.annotate(Bool)
        body_type = analyse(node.body, env, non_generic)
        orelse_type = analyse(node.body, env, non_generic)
        unify(body_type, orelse_type)
        return node.annotate(body_type)
    elif isinstance(node, Apply):
        fun_type = analyse(node.fn, env, non_generic)
        arg_type = analyse(node.arg, env, non_generic)
        result_type = TypeVariable()
        if not isinstance(fun_type, Union):
            fun_types = [fun_type]
        else:
            fun_types = fun_type.types
        backup = Function(arg_type, result_type)
        #if hasattr(node.fn, 'name') and node.fn.name == 'h__add__':
        # print(node, arg_type, result_type, [str(f) for f in fun_type])
        found = False
        print(backup, fun_type);input()
        unify(backup, fun_type)
        node.fn.annotate(backup)

        # for f in fun_types:
        #     # print('s', f)
        #     try:
        #         # function_type = Function(copy.copy(arg_type), copy.copy(result_type))
        #         # unify(function_type, f)
        #         unify(backup, f)
        #         node.fn.annotate(f)
        #         found = True
        #         break
        #     except TypeError:
        #         print('t', arg_type, result_type)
        #         continue
        # if not found:
            # exit(0)
        return node.annotate(result_type)
    elif isinstance(node, Body):
        analyse(node.expression, env, non_generic)
        return node.annotate(
                    analyse(node.other, env, non_generic))
    elif isinstance(node, Lambda):
        arg_type = TypeVariable()
        new_env = env.copy()
        new_env[node.v] = arg_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(arg_type)
        if node.expected:
            expected_type = find_type(node.expected, env)
            print('UNIFY ARG', expected_type, arg_type)
            unify(expected_type, arg_type)
            print('UN', expected_type, arg_type)
        result_type = analyse(node.body, new_env, new_non_generic)
        if node.return_expected:
            print(node.return_expected)
            expected_type = find_type(node.return_expected, env)
            print('UNIFY RET', expected_type, result_type)
            unify(expected_type, result_type)
            print('UN', expected_type, result_type)
        return node.annotate(Function(arg_type, result_type))
    elif isinstance(node, LambdaNoArgs):
        return node.annotate(analyse(node.body, env, non_generic))
    elif isinstance(node, aList):
        if not node.items:
            item_type = TypeVariable()
        else:
            item_type = find_type(node.items[0], env)
            print(item_type, node.items[0], type(node.items[0]));input()
            node.items[0].annotate(item_type)
            for j in node.items[1:]:
                unify(item_type, find_type(j, env))
                j.annotate(item_type)
        return node.annotate(List(item_type))
    elif isinstance(node, Let):
        defn_type = analyse(node.defn, env, non_generic)
        new_env = env.copy()
        print('LALALALA', node.v, defn_type)

        if node.v in new_env:
            if isinstance(new_env[node.v], Function):
                new_env[node.v] = Union(new_env[node.v], defn_type)
            elif isinstance(new_env[node.v], Union):
                new_env[node.v].types.append(defn_type)
        else:
            new_env[node.v] = defn_type
        node.defn.annotate(new_env[node.v])
        return node.annotate(analyse(node.body, new_env, non_generic))
    elif isinstance(node, Letrec):
        new_type = TypeVariable()
        new_env = env.copy()
        new_env[node.v] = new_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(new_type)
        defn_type = analyse(node.defn, new_env, new_non_generic)
        unify(new_type, defn_type)
        node.defn.annotate(defn_type)
        return node.annotate(analyse(node.body, new_env, non_generic))
    assert 0, "Unhandled syntax node {0}".format(node)

def find_type(expected, env):
    if isinstance(expected, Function):
        print(expected)
        for i in range(len(expected.types)):
            expected.types[i] = find_type(expected.types[i], env)
        return expected
    elif isinstance(expected, Union):
        for i in range(len(expected.types)):
            expected.types[i] = find_type(expected.types[i], env)
        return expected
    elif isinstance(expected, List):
        expected.types[0] = find_type(expected.types[0], env)
        return expected
    elif isinstance(expected, Ident):
        return getType(expected, env, set())
    elif isinstance(expected, TypeOperator) and not expected.types:
        return env.get(expected.name, expected)

def getType(name, env, non_generic):
    """Get the type of identifier name from the type environment env.

    Args:
        name: The identifier name
        env: The type environment mapping from identifier names to types
        non_generic: A set of non-generic TypeVariables

    Raises:
        ParseError: Raised if name is an undefined symbol in the type
            environment.
    """
    if name in env:
        type_ = env[name]
        if isinstance(type_, list):
            return [fresh(t, non_generic) for t in type_]
        else:
            return fresh(type_, non_generic)
    else:
        if isinstance(name, Ident):
            name = name.name
        types_of_name = {
            int: Integer,
            float: Float,
            bool: Bool
        }
        if type(name) in types_of_name:
            return types_of_name[type(name)]
        elif len(name) != 0 and name[0] == "'" and name[-1] == "'":
            return String
        else:
            raise ParseError("Undefined symbol {0}".format(name))


def fresh(t, non_generic):
    """Makes a copy of a type expression.

    The type t is copied. The the generic variables are duplicated and the
    non_generic variables are shared.

    Args:
        t: A type to be copied.
        non_generic: A set of non-generic TypeVariables
    """
    mappings = {} # A mapping of TypeVariables to TypeVariables

    def freshrec(tp):
        p = prune(tp)
        if isinstance(p, TypeVariable):
            if isGeneric(p, non_generic):
                if p not in mappings:
                    mappings[p] = TypeVariable()
                return mappings[p]
            else:
                return p
        elif isinstance(p, TypeOperator):
            return TypeOperator(p.name, [freshrec(x) for x in p.types])
        elif isinstance(p, Union):
            return Union(*[freshrec(x) for x in p.types])
    return freshrec(t)


def unify(t1, t2):
    """Unify the two types t1 and t2.

    Makes the types t1 and t2 the same.

    Args:
        t1: The first type to be made equivalent
        t2: The second type to be be equivalent

    Returns:
        None

    Raises:
        TypeError: Raised if the types cannot be unified.
    """

    a = prune(t1)
    b = prune(t2)
    if isinstance(a, TypeVariable):
        if a != b:
            if occursInType(a, b):
                raise TypeError("recursive unification")
            a.instance = b
    elif isinstance(a, (TypeOperator, Union)) and isinstance(b, TypeVariable):
        unify(b, a)
    elif isinstance(a, TypeOperator) and isinstance(b, TypeOperator):
        if (a.name != b.name or len(a.types) != len(b.types)):
            raise TypeError("Type mismatch: {0} != {1}".format(str(a), str(b)))
        for p, q in zip(a.types, b.types):
            unify(p, q)
    elif isinstance(a, TypeOperator) and isinstance(b, Union):
        for z in b.types:
            try:
                unify(a, z)
                return
            except (NotUnifiedError, TypeError) as e:
                continue
        raise NotUnifiedError('{0} x {1}'.format(str(a), str(b)))
    elif isinstance(a, Union) and isinstance(b, TypeOperator):
        for z in a.types:
            try:
                unify(z, b)
                return
            except (NotUnifiedError, TypeError) as e:
                continue
        raise NotUnifiedError('{0} x {1}'.format(str(a), str(b)))
    elif isinstance(a, Union) and isinstance(b, Union):
        for y in a.types:
            for z in b.types:
                try:
                    unify(y, z)
                    return
                except (NotUnifiedError, TypeError) as e:
                    continue
        raise NotUnifiedError('{0} x {1}'.format(str(a), str(b)))
    else:
        raise NotUnifiedError('{0} x {1}'.format(str(a), str(b)))


def prune(t):
    """Returns the currently defining instance of t.

    As a side effect, collapses the list of type instances. The function Prune
    is used whenever a type expression has to be inspected: it will always
    return a type expression which is either an uninstantiated type variable or
    a type operator; i.e. it will skip instantiated variables, and will
    actually prune them from expressions to remove long chains of instantiated
    variables.

    Args:
        t: The type to be pruned

    Returns:
        An uninstantiated TypeVariable or a TypeOperator
    """
    if isinstance(t, TypeVariable):
        if t.instance is not None:
            t.instance = prune(t.instance)
            return t.instance
    return t


def isGeneric(v, non_generic):
    """Checks whether a given variable occurs in a list of non-generic variables

    Note that a variables in such a list may be instantiated to a type term,
    in which case the variables contained in the type term are considered
    non-generic.

    Note: Must be called with v pre-pruned

    Args:
        v: The TypeVariable to be tested for genericity
        non_generic: A set of non-generic TypeVariables

    Returns:
        True if v is a generic variable, otherwise False
    """
    return not occursIn(v, non_generic)


def occursInType(v, type2):
    """Checks whether a type variable occurs in a type expression.

    Note: Must be called with v pre-pruned

    Args:
        v:  The TypeVariable to be tested for
        type2: The type in which to search

    Returns:
        True if v occurs in type2, otherwise False
    """
    pruned_type2 = prune(type2)
    if pruned_type2 == v:
        return True
    elif isinstance(pruned_type2, TypeOperator):
        return occursIn(v, pruned_type2.types)
    return False


def occursIn(t, types):
    """Checks whether a types variable occurs in any other types.

    Args:
        v:  The TypeVariable to be tested for
        types: The sequence of types in which to search

    Returns:
        True if t occurs in any of types, otherwise False
    """
    return any(occursInType(t, t2) for t2 in types)

def isIntegerLiteral(name):
    """Checks whether name is an integer literal string.

    Args:
        name: The identifier to check

    Returns:
        True if name is an integer literal, otherwise False
    """
    result = True
    try:
        int(name)
    except ValueError:
        result = False
    return result

#==================================================================#
# Example code to exercise the above


def tryExp(env, node):
    """Try to evaluate a type printing the result or reporting errors.

    Args:
        env: The type environment in which to evaluate the expression.
        node: The root node of the abstract syntax tree of the expression.

    Returns:
        None
    """
    print(str(node) + " : ", end=' ')
    try:
        t = analyse(node, env)
        print(str(t))
    except (ParseError, TypeError) as e:
        print(e)


def main():
    """The main example program.

    Sets up some predefined types using the type constructors TypeVariable,
    TypeOperator and Function.  Creates a list of example expressions to be
    evaluated. Evaluates the expressions, printing the type or errors arising
    from each.

    Returns:
        None
    """

    var1 = TypeVariable()
    var2 = TypeVariable()
    pair_type = TypeOperator("*", (var1, var2))
    var4 = TypeVariable()
    var5 = TypeVariable()
    var6 = TypeVariable()
    var7 = TypeVariable()
    # List = TypeOperator("list", (var4,))
    list_type = List(var4)
    var3 = TypeVariable()

    my_env = { "pair" : Function(var1, Function(var2, pair_type)), # var1 -> var2 -> (* var1 var2)
               "true" : Bool,
               "list" : list_type, # (list var4)
               "map"  : Function(Function(var5, var6),
                                 Function(List(var5), List(var6))), # (var5 -> var6) -> (list var5)-> (list var6)
               "append":
                        Multi_Function([List(var7), var7, List(var7)]),
               "cond" : Function(Bool, Function(var3, Function(var3, var3))),
               "zero" : Function(Integer, Bool),
               "pred" : Function(Integer, Integer),
               "times": Function(Integer, Function(Integer, Integer)) }

    pair = Apply(Apply(Ident("pair"), Apply(Ident("f"), Ident("4"))), Apply(Ident("f"), Ident("true")))

    examples = [
            #list
            Let("e0", # let f = [1]
                aList([]),
                Let("e",
                    Apply(
                        Apply(Ident("append"),
                              Ident("e0")),
                              Ident("0")),
                    Ident("e"))),

            Let("e0",  # let e0 = (append [0] 0)
                Apply(
                    Apply(Ident("append"),
                          aList([Ident("0")])), Ident("0")),
                Ident("e0")),

            # factorial
            Letrec("factorial", # letrec factorial =
                Lambda("n",    # fn n =>
                    Apply(
                        Apply(   # cond (zero n) 1
                            Apply(Ident("cond"),     # cond (zero n)
                                Apply(Ident("zero"), Ident("n"))),
                            Ident("1")),
                        Apply(    # times n
                            Apply(Ident("times"), Ident("n")),
                            Apply(Ident("factorial"),
                                Apply(Ident("pred"), Ident("n")))
                        )
                    )
                ),      # in
                Apply(Ident("factorial"), Ident("5"))
            ),

            # Should fail:
            # fn x => (pair(x(3) (x(true)))
            Lambda("x",
                Apply(
                    Apply(Ident("pair"),
                        Apply(Ident("x"), Ident("3"))),
                    Apply(Ident("x"), Ident("true")))),

            # pair(f(3), f(true))
            Apply(
                Apply(Ident("pair"), Apply(Ident("f"), Ident("4"))),
                Apply(Ident("f"), Ident("true"))),


            # let f = (fn x => x) in ((pair (f 4)) (f true))
            Let("f", Lambda("x", Ident("x")), pair),

            # fn f => f f (fail)
            Lambda("f", Apply(Ident("f"), Ident("f"))),

            # let g = fn f => 5 in g g
            Let("g",
                Lambda("f", Ident("5")),
                Apply(Ident("g"), Ident("g"))),

            # example that demonstrates generic and non-generic variables:
            # fn g => let f = fn x => g in pair (f 3, f true)
            Lambda("g",
                   Let("f",
                       Lambda("x", Ident("g")),
                       Apply(
                            Apply(Ident("pair"),
                                  Apply(Ident("f"), Ident("3"))
                            ),
                            Apply(Ident("f"), Ident("true"))))),


            # Function composition
            # fn f (fn g (fn arg (f g arg)))
            Lambda("f", Lambda("g", Lambda("arg", Apply(Ident("g"), Apply(Ident("f"), Ident("arg"))))))
    ]

    for example in examples:
        tryExp(my_env, example)


if __name__ == '__main__':
    main()
