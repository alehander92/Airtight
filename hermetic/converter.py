import ast
import hermetic.hindley_milner_ast as hm_ast

class PythonConverter:
    ''' converts the python ast
        to a lambda-like ast
        used for type inference
    '''

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
        ast.Not:  '__not__',
        ast.Index: '__index__',
        ast.Slice: '__slice__'
    }

    def __init__(self):
        pass

    def convert(self, python_ast):
        self.type_vars = []
        return self.convert_node(python_ast)

    def _unique_type_var(self):
        return hm_ast.TypeVariable()

    def node_dict(self, node):
        return {field : getattr(node, field) for field in node._fields}

    def convert_node(self, node, context=None):
        return getattr(self, 'convert_' + str(node.__class__.__name__).lower())(
                       context=context, **self.node_dict(node))

    def convert_module(self, body, context):
        return self.convert_body(body, context)

    def convert_assign(self, targets, value, context):
        '''
        var = 'a'
        ..context
        =>
        Let('var'
            String('a'),
            context)

        var, z = 'a', 'b'
        ..context
        =>
        Letmany(['var', 'z'],
            [String('a'), String('b')],
            context)
        '''


        if len(targets) == 1:
            return hm_ast.Let(
                        targets[0].id,
                        self.convert_node(value),
                        context)
        else:
            return hm_ast.Letmany(
                        [t.id for t in targets],
                        [self.convert_node(node) for node in value.elts],
                        context)

    def convert_str(self, s, context):
        return hm_ast.aString(s)

    def convert_num(self, n, context):
        if type(n) == float:
            return hm_ast.aFloat(n)
        else:
            return hm_ast.anInteger(n)

    def convert_functiondef(self, name, args, body, decorator_list, returns, context):
        '''
        def name(arg, arg2):
            return arg
        ..context
        =>
        Let('name',
            Multi_Lambda(['arg', 'arg2'],
                [Ident('arg')]),
            context)
        '''
        expected = []
        vars = {}
        for arg in args.args:
            expected.append(self.convert_annotation(arg.annotation, vars))
        expected.append(self.convert_annotation(returns, vars))
        result = hm_ast.Let(
                name,
                hm_ast.Multi_Lambda(
                    [arg.arg for arg in args.args],
                    self.convert_body(body, None),
                    expected=expected),
                context)
        result.h_native = False
        result.h_vars = []
        if decorator_list:
            if isinstance(decorator_list[0], ast.Name) and decorator_list[0].id == 'native':
                result.h_native = True
            if isinstance(decorator_list[-1], ast.Call) and decorator_list[-1].func.id == 'template':
                # result.h_vars = vars.keys
                result.h_vars = [vars[arg.id] for arg in decorator_list[-1].args] # vars.keys()
        return result

    def convert_annotation(self, annotation, vars):
        if isinstance(annotation, ast.Name) and annotation.id.islower():
            if annotation.id not in vars:
                vars[annotation.id] = hm_ast.TypeVariable()
            return vars[annotation.id]
        elif isinstance(annotation, ast.Name):
            return hm_ast.TypeOperator(annotation.id, [])
        elif isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.RShift):
            if isinstance(annotation.left, ast.Name):
                # A >> B
                left = [annotation.left, annotation.right]
            else:
                # (A, Z) >> B
                left = annotation.left.elts + [annotation.right]
            return hm_ast.Multi_Function([self.convert_annotation(l, vars) for l in left])
        elif isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BinOr):
            # A | B
            left, right = [self.convert_annotation(a, vars) for a in [annotation.left, annotation.right]]
            return hm_ast.Union(left, right)
        elif isinstance(annotation, ast.List):
            # [A]
            return hm_ast.List(self.convert_annotation(annotation.elts[0], vars))
        else:
            return None

    def convert_expr(self, value, context):
        return self.convert_node(value, context)

    def convert_body(self, body, context):
        if len(body) == 1:
            converted = self.convert_node(body[0], context)
            if not isinstance(converted, (hm_ast.Let, hm_ast.Letrec)):
                return converted
            elif context is None:
                converted.body = hm_ast.Ident(converted.v)
                return converted
        else:
            current = len(body) - 1
            # context = context or hm_ast.anInteger(2)
            while current >= 0:
                next_node = self.convert_node(body[current], context)
                if isinstance(next_node, (hm_ast.Let, hm_ast.Letrec)):
                    context = next_node
                elif context:
                    context = hm_ast.Body(next_node, context)
                else:
                    context = next_node
                current -= 1
            return context

    def convert_return(self, value, context):
        return self.convert_node(value, context)

    def convert_binop(self, left, right, op, context):
        '''
        2 / 2
        =>
        Multi_Apply(
            Ident('h_divide'),
            [Integer(2), Integer(2)])
        '''
        return hm_ast.Multi_Apply(
            hm_ast.Ident('h' + self.OPERATOR_MAGIC_FUNCTIONS[type(op)]),
            [self.convert_node(left, context), self.convert_node(right, context)])

    def convert_compare(self, ops, left, comparators, context):
        return hm_ast.Multi_Apply(
            hm_ast.Ident('h' + self.OPERATOR_MAGIC_FUNCTIONS[type(ops[0])]),
            [self.convert_node(left, context), self.convert_node(comparators[0], context)])

    def convert_if(self, test, body, orelse, context):
        return hm_ast.If(
            self.convert_node(test, context),
            self.convert_body(body, context),
            self.convert_body(orelse, context))

    def convert_for(self, target, body, iter, orelse, context):
        return hm_ast.For(
            self.convert_node(iter, context),
            self.convert_node(target, context),
            self.convert_body(body, context))

    def convert_subscript(self, value, slice, ctx, context):
        if isinstance(slice, ast.Index):
            return hm_ast.Multi_Apply(
                hm_ast.Ident('h' + self.OPERATOR_MAGIC_FUNCTIONS[type(slice)]), [
                self.convert_node(value, context),
                self.convert_node(slice.value)])
        else:
            return hm_ast.Multi_Apply(
                hm_ast.Ident('h' + self.OPERATOR_MAGIC_FUNCTIONS[type(slice)]), [
                self.convert_node(value, context),
                self.convert_node(slice.lower) if slice.lower else hm_ast.anInteger(0),
                self.convert_node(slice.upper) if slice.upper else hm_ast.Multi_Apply(
                    self.OPERATOR_MAGIC_FUNCTIONS[ast.Sub], [
                    hm_ast.Apply(hm_ast.Ident('len'), self.convert_node(value, context)),
                    hm_ast.anInteger(1)])])

    def convert_name(self, id, ctx, context):
        '''
        alexander
        =>
        Ident("alexander")
        '''
        return hm_ast.Ident(id)

    def convert_nameconstant(self, value, context):
        if value in [True, False]:
            return hm_ast.aBoolean(value)
        else:
            return hm_ast.Ident(str(value))

    def convert_list(self, elts, ctx, context):
        '''
        [e]
        =>
        aList(Ident("e"))
        '''
        return hm_ast.aList([self.convert_node(elt) for elt in elts])

    def convert_call(self, func, args, keywords, starargs, kwargs, context):
        '''
        a(2)
        =>
        Apply(Ident("a"), anInteger(2))
        '''
        return hm_ast.Multi_Apply(self.convert_node(func), [self.convert_node(arg) for arg in args])

    def convert_lambda(self, args, body, context):
        '''
        lambda s: s
        =>
        Lambda(Ident("s"), Ident("s"))
        '''
        return hm_ast.Multi_Lambda([arg.arg for arg in args.args], self.convert_node(body))


