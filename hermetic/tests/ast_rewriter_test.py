from nose.tools import assert_equal, assert_raises, raises
from hermetic.ast_rewriter import ASTRewriter
from hermetic import errors

class TestASTRewriter:
    @raises(errors.NotSupportedError)
    def test_validate_varargs(self):
        self.rewrite('def a(*a):pass')

    @raises(errors.NotSupportedError)
    def test_validate_kwargs(self):
        self.rewrite('def z(**z):pass')


    def rewrite(self, source):
        return ASTRewriter(source).rewrite()
