import airtight.hindley_milner_ast as hm_ast
from airtight.hindley_milner_ast import *

Z = 8
vars_type = [hm_ast.TypeVariable() for i in range(Z)]

TOP_ENV = {
    'map': Multi_Function([Function(vars_type[1], vars_type[2]), List(vars_type[1]), List(vars_type[2])]),
    # map : (g -> h) -> [g] -> [h]
    'a__add__': Union(
        Multi_Function([Integer, Integer, Integer]),
        # + : Integer -> Integer -> Integer
        Multi_Function([Float, Float, Float])
        # + : Float -> Float -> Float
    ),
    'a__substract__': Multi_Function([Integer, Integer, Integer]),
    # - : Integer -> Integer -> Integer
    'a__divide__': Multi_Function([Integer, Integer, Integer]),
    # / : Integer -> Integer -> Integer
    'a__mult__': Multi_Function([Integer, Integer, Integer]),
    # * : Integer -> Integer -> Integer
    'filter': Multi_Function([Function(vars_type[3], Bool), List(vars_type[3]), List(vars_type[3])]),
    # filter : (g -> Bool) -> [g] -> [g]
    'print' : Union(
       Function(Integer, String),
       Function(String, String),
       Function(List(Integer), String),
       Function(List(String), String)),
    'prints': Function(String, String),

    # prints : String -> String
    'range': Multi_Function([Integer, Integer, [Integer]]),
    # range: Integer -> Integer -> [Integer]

    'str': Union(
        Function(Integer, String),
        Function(String, String),
        Function(List(Integer), String),
        Function(List(String), String)),
    'a__gt__': Union(
        Multi_Function([Integer, Integer, Bool]),
        # > : Integer -> Integer -> Bool
        Multi_Function([Float, Float, Bool])
        # > : Float -> Float -> Bool
    ),
    'a__lt__': Union(
        Multi_Function([Integer, Integer, Bool]),
        # < : Integer -> Integer -> Bool
        Multi_Function([Float, Float, Bool])
        # < : Float -> Float -> Bool
    ),
    'a__lte__': Union(
        Multi_Function([Integer, Integer, Bool]),
        # <= : Integer -> Integer -> Bool
        Multi_Function([Float, Float, Bool])
        # <= : Float -> Float -> Bool
    ),
    'a__index__': Multi_Function([List(vars_type[4]), Integer, vars_type[4]]),
    # [] : [h] -> Integer -> h
    'a__slice__': Multi_Function([List(vars_type[5]), Integer, Integer, vars_type[5]]),
    # [] : [h] -> Integer -> Integer -> [h]
    'add': Multi_Function([String, String, String]),
    # add: String -> String -> String
    'to_int': Union(
        Function(String, Integer),
        Function(Integer, Integer)),
    # to_int: String -> Integer | Integer -> Integer
    'to_float': Union(
        Function(Integer, Float),
        Function(Float, Float)),
    # to_float: Integer -> Float | Float -> Float,
    'read': Function(String, String),
    # read: String -> String
    'ends_with': Multi_Function([String, String, Bool]),
    # ends_with: String -> String -> Bool
    'split_w': Function(String, List(String)),
    # split_w: String -> [String]
    'count': Multi_Function([List(vars_type[7]), Function(vars_type[7], Bool), Integer]),
    # count: [h] -> (h -> Bool) -> Integer
    'append': Multi_Function([List(vars_type[6]), vars_type[6], List(vars_type[6])])
    # append : [h] -> h -> [h]
}


