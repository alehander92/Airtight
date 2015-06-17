from hermetic.hindley_milner_ast import *

def convert_ast(hm_ast):
    '''converts hindley-milner typed scheme-like ast to a
    lower level ast
    '''
    return LLAstGenerator(hm_ast).generate()

class LLAstGenerator:
    def __init__(self, hm_ast):
        self.hm_ast = hm_ast

    def generate(self):
        node = self.generate_node(self.hm_ast)
        if isinstance(node, list):
            return LLAst(type='source',expressions=node, h_type=node[-1].h_type)
        else:
            return node

    def generate_node(self, node):
        return getattr(self, 'generate_%s' % str(type(node).__name__).lower())(node)

    def generate_body(self, node):
        other = self.generate_node(node.other)
        if isinstance(other, list):
            return [self.generate_node(node.expression)] + other
        else:
            return [self.generate_node(node.expression), other]


    def generate_let(self, node):
        if isinstance(node.defn, Lambda):
            let_ast = LLAst(
                type    = 'method',
                label   = LLAst(type='ident', label=node.v, h_type=node.defn.h_type),
                body    = self.generate_lambda(node.defn),
                h_type  = node.defn.h_type,
                h_native = node.h_native,
                h_vars  = node.h_vars,
                h_return_type = node.defn.h_return_type)
        else:
            let_ast = LLAst(
                type    = 'assignment',
                label   = LLAst(type='ident', label=node.v, h_type=node.defn.h_type),
                right   = self.generate_node(node.defn),
                h_type  = node.h_type)
        body_ast = self.generate_node(node.body)
        return [let_ast] + body_ast if isinstance(body_ast, list) else [let_ast, body_ast]

    def generate_lambda(self, node):
        if isinstance(node.body, Lambda):
            lambda_ast = self.generate_lambda(node.body)
        else:
            lambda_ast = LLAst(
                type    = 'lambda',
                args    = [],
                body    = self.generate_node(node.body),
                h_type  = node.h_type,
                h_return_type = node.h_return_type)
        lambda_ast.args = [LLAst(type='ident', label=node.v, h_type=node.h_type.types[0])] + lambda_ast.args
        return lambda_ast

    def generate_ident(self, node):
        type_label = str(type(node).__name__)
        if type_label[:2] == 'an':
            type_label = type_label[2:]
        elif type_label[0] == 'a':
            type_label = type_label[1:]
        return LLAst(type=type_label.lower(), label=node.name, h_type=node.h_type)

    generate_aninteger = generate_afloat = generate_aboolean = generate_astring = generate_ident

    def generate_apply(self, node):
        if isinstance(node.fn, Apply):
            apply_ast = self.generate_apply(node.fn)
            apply_ast.args.append(self.generate_node(node.arg))
        else:
            apply_ast = LLAst(type='apply', function=self.generate_node(node.fn), args=[self.generate_node(node.arg)], h_type=node.h_type, _special=False)
        return apply_ast

    def generate_alist(self, node):
        return LLAst(type='list', items=[self.generate_node(e) for e in node.items], h_type=node.h_type)

    def generate_if(self, node):
        return LLAst(type='if', test=self.generate_node(node.test), body=self.generate_node(node.body), orelse=self.generate_node(node.orelse), h_type=node.h_type)

    def generate_for(self, node):
        return LLAst(type='for', target=self.generate_node(node.target), iter=self.generate_node(node.iter), body=self.generate_node(node.body), h_type=node.h_type)

class LLAst:
    def __init__(self, **kwargs):
        for label, arg in kwargs.items():
            setattr(self, label, arg)
        self.data = kwargs

    def __str__(self):
        return self.render(0)

    def render(self, depth=0):
        if self.type == 'method':
            return '{offset}method {label}({args}) @ {h_type}\n{body}'.format(
                offset=self.offset(depth),
                label=str(self.label),
                args=', '.join(str(arg) for arg in self.body.args),
                h_type=self.h_type,
                body=str(self.body.body))
        elif self.type == 'assignment':
            return '{offset}assignment[{label} : {value}] @ {h_type}'.format(
                offset=self.offset(depth),
                label=str(self.label),
                value=str(self.right),
                h_type=self.h_type)
        elif len(self.data) == 3 and 'label' in self.data:
            return '{offset}{type}[{label}] @ {h_type}'.format(
                offset=self.offset(depth),
                type=self.type,
                label=str(self.label),
                h_type=self.h_type)
        elif self.type == 'source':
            return '{offset}source: @ {h_type}\n{body}'.format(
                offset=self.offset(depth),
                h_type=self.h_type,
                body='\n'.join(s.render(depth + 1) for s in self.expressions))
        elif self.type == 'apply':
            return '{offset}call {label}({args}) @ {h_type}'.format(
                offset=self.offset(depth),
                label=str(self.function),
                args=', '.join(str(arg) for arg in self.args),
                h_type=self.h_type)
        else:
            return '{offset}{label}: @{h_type}\n'.format(offset=self.offset(depth), label=self.type, h_type=self.h_type) +\
               '\n'.join('{offset}{label} = {value}'.format(offset=self.offset(depth + 1), label=label, value=self.render_value(value)) for label, value in self.data.items() if label != 'type')

    def render_value(self, value, depth=0):
        if isinstance(value, LLAst):
            return value.render(depth + 1)
        elif isinstance(value, list):
            return '[' + ', '.join(self.render_value(v, depth + 1) for v in value) + ']'
        else:
            return str(value)

    def offset(self, depth):
        return '  ' * depth
