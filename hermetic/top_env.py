import hermetic.hindley_milner_ast as hm_ast
from hermetic.hindley_milner_ast import *

Z = 4
vars_type = [hm_ast.TypeVariable() for i in range(Z)]

TOP_ENV = {
    'map': Multi_Function([Function(vars_type[1], vars_type[2]), List(vars_type[1]), List(vars_type[2])]),
    # map : (g -> h) -> [g] -> [h]
    'h__add__': [
        Multi_Function([Integer, Integer, Integer]),
        # + : Integer -> Integer -> Integer
        Multi_Function([Float, Float, Float])
        # + : Float -> Float -> Float
    ],
    'h__sub__': Multi_Function([Integer, Integer, Integer]),
    # - : Integer -> Integer -> Integer
    'h__divide__': Multi_Function([Integer, Integer, Integer]),
    # / : Integer -> Integer -> Integer
    'h__mult__': Multi_Function([Integer, Integer, Integer]),
    # * : Integer -> Integer -> Integer
    'filter': Multi_Function([Function(vars_type[3], Bool), List(vars_type[3]), List(vars_type[3])]),
    # filter : (g -> Bool) -> [g] -> [g]
}


