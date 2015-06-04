import ast
from . import errors

class ASTRewriter:
    '''
    Rewrites builtin ast to hermetic ast
    Checks for unsupported python syntax
    '''

    NOT_SUPPORTED = set([
        ast.With,
        ast.ListComp])

    OPERATOR_MAGIC_FUNCTIONS = {
        ast.Add: '__add__',
        ast.Sub: '__substract__',
        ast.Mult: '__multiply__',
        ast.FloorDiv: '__real_divide__',
        ast.Div: '__divide__',
        ast.Mod: '__percent__',
        ast.Pow: '__power__',
        ast.Eq: '__equals__',
        ast.NotEq: '__not_equals__',
        ast.Lt: '__lt__',
        ast.LtE: '__lte__',
        ast.Gt: '__gt__',
        ast.GtE: '__gte',
        ast.And: '__and__',
        ast.Or: '__or__',
        ast.Not:  '__not__'
    }
    def __init__(self, source):
        self.source = source

    def rewrite(self):
        tree = ast.parse(self.source)
        return self._rewrite_node(tree)

    def _rewrite_node(self, node):
        if isinstance(node, (list, tuple)):
            return list(map(self._rewrite_node, node))
        elif hasattr(self, '_rewrite_' + type(node).__name__.lower()):
            node = getattr(self, '_rewrite_' + type(node).__name__.lower())(node)
        elif not isinstance(node, ast.AST):
            return node
        elif type(node) in self.NOT_SUPPORTED:
            raise errors.NotSupportedError(
                '%s is not supported in hermetic' % type(node).__name__)

        for c, child in node.__dict__.items():
            setattr(node, c, self._rewrite_node(child))
        return node

    def _rewrite_arguments(self, node):
        if node.vararg:
            raise errors.NotSupportedError(
                "vararg *%s is not supported in hermetic" % node.vararg.arg)
        elif node.kwarg:
            raise errors.NotSupportedError(
                "kwarg **%s is not supported in hermetic" % node.kwarg.arg)
        else:
            return node

    def _rewrite_unaryop(self, node):
        '''
        rewrite not var as __not__(var) etc
        '''
        return ast.Call(
            func=ast.Name(self.OPERATOR_MAGIC_FUNCTIONS[type(node.op)], None),
            args=[node.operand],
            keywords=[],
            starargs=None,
            kwargs=None)

    def _rewrite_binop(self, node):
        '''
        rewrite a + b as __add__(a, b) etc
        '''
        return ast.Call(
            func=ast.Name(self.OPERATOR_MAGIC_FUNCTIONS[type(node.op)], None),
            args=[node.left, node.right],
            keywords=[],
            starargs=None,
            kwargs=None)

    def _rewrite_compare(self, node):
        '''
        rewrite a == b as __eq__(a, b) etc
        '''
        if len(node.comparators) > 1:
            raise errors.NotSupportedError(
                "compare is supported only for 2 elements")
        return ast.Call(
            func=ast.Name(self.OPERATOR_MAGIC_FUNCTIONS[type(node.ops[0])], None),
            args=[node.left, node.comparators[0]],
            keywords=[],
            starargs=None,
            kwargs=None)

    def _rewrite_classdef(self, node):
        '''
        rewrite compile-time decorators to annotations

        is_native
        '''
        node.a_typeclass = []
        if node.decorator_list:
            decorators = []
            for m in node.decorator_list:
                if isinstance(m, ast.Call) and m.func.id == 'typeclass':
                    r = [arg.id for arg in m.args]
                    node.a_typeclass += r
                else:
                    decorators.append(m)
            node.decorator_list = decorators
        return node

    def _rewrite_functiondef(self, node):
        '''
        rewrite compile-time decorators to annotations

        native a_native, a flag specifying if the body should be visited or
                         the function has a native implementation
        template  a_template, a list of tuples with the type and its typeclass

        '''
        node.a_native = False
        node.a_template = []
        if node.decorator_list:
            decorators = []
            for m in node.decorator_list:
                if isinstance(m, ast.Name) and m.id == 'native':
                    node.a_native = True
                elif isinstance(m, ast.Call) and m.func.id == 'template':
                    for child in m.args:
                        typeclass, q = child.comparators[0].func.id, [
                            arg.id for arg in child.comparators[0].args]
                        node.a_template.append((child.left.id, [typeclass, q]))
                else:
                    decorators.append(m)
            node.decorator_list = decorators
        return node

    def _rewrite_nameconstant(self, node):
        if node.id == 'None':
            raise self.NotSupportedError('None isn\'t used in hermetic')
        return node
