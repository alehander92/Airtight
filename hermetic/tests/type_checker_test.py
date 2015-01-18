from nose.tools import assert_equal, assert_raises, raises
from hermetic.type_checker import TypeChecker
import ast

class TestTypeChecker:
    def test_accepts_ast(self):
        checker = TypeChecker(ast.parse('def php():pass'))
        assert_equal(checker.tree.body[0].name, 'php')

    def test_checks_a_list(self):
        checker = TypeChecker(ast.parse(''))
        assert_equal(checker.type_check(), [])

