from hermetic.ll_ast import *

class Generator:
    def __init__(self, ast):
        self.ast = ast
        self.out = []
        self.scopes = [{}]

    def generate(self):
        for node in self.ast.expressions:
            self.write_node(node)
            if node.type != 'method':
                self.semi()
            self.nl()
        return ''.join(self.out)

    def offset(self, depth):
        self.out.append(self.OFFSET * depth)

    def ws(self):
        self.out.append(' ')

    def nl(self):
        self.out.append('\n')

    def lparen(self):
        self.out.append('(')

    def rparen(self):
        self.out.append(')')

    def lcurly(self):
        self.out.append('{')

    def rcurly(self):
        self.out.append('}')

    def s(self, s, depth=0):
        self.out.append(s)

    def comma(self):
        self.out.append(',')

    def semi(self):
        self.out.append(';')


class CGenerator(Generator):
    OFFSET = '    '

    def ref(self):
        self.out.append('*')

    def write_node(self, node, depth=0):
        getattr(self, 'write_' + node.type)(node, depth)

    def write_method(self, node, depth=0):
        self.offset(depth)
        self.write_type(node.h_type)
        self.ref()
        self.ws()
        self.write_ident(node.label)
        self.lparen()
        self.write_m_args(node.body.args, node.h_type)
        self.rparen()
        self.lcurly()
        self.nl()
        body = node.body.body if isinstance(node.body.body, list) else [node.body.body]
        for e in body[:-1]:
            self.write_node(e, depth + 1)
            self.semi()
            self.nl()
        if body[-1].type != 'if':
            self.offset(depth + 1)
            self.s('return')
            self.ws()
            self.write_node(body[-1])
        else:
            self.write_if(body[-1], depth + 1, with_return=True)
        self.semi()
        self.nl()
        self.offset(depth)
        self.rcurly()

    def write_m_args(self, args, h_type, depth=0):
        for arg, t in zip(args[:-1], h_type.types[:-2]):
            self.write_type(t)
            self.ref()
            self.ws()
            self.write_node(arg)
            self.comma()
            self.ws()
        print(h_type)
        self.write_type(h_type.types[-2])
        self.ref()
        self.ws()
        self.write_node(args[-1])

    def write_if(self, node, depth=0, with_return=False):
        self.offset(depth)
        self.s('if')
        self.lparen()
        self.write_node(node.test)
        self.rparen()
        self.lcurly()
        self.nl()
        body = node.body if isinstance(node.body, list) else [node.body]
        for e in body[:-1]:
            self.write_node(e, depth + 1)
            self.semi()
            self.nl()
        if with_return:
            self.offset(depth + 1)
            self.s('return')
            self.ws()
            self.write_node(body[-1])
        else:
            self.write_node(body[-1], depth + 1)
        self.semi()
        self.nl()

        self.offset(depth)
        self.rcurly()
        self.nl()
        self.offset(depth)
        self.s('else')
        self.lcurly()
        self.nl()
        orelse = node.orelse if isinstance(node.orelse, list) else [node.orelse]
        for e in orelse[:-1]:
            self.write_node(e, depth + 1)
            self.semi()
            self.nl()
        if with_return:
            self.offset(depth + 1)
            self.s('return')
            self.ws()
            self.write_node(orelse[-1])
        else:
            self.write_node(orelse[-1], depth + 1)
        self.semi()
        self.nl()

        self.offset(depth)
        self.rcurly()
        self.nl()

    def write_ident(self, node, depth=0):
        self.offset(depth)
        self.s('h_' + str(node.label))

    def write_n(self, node, depth=0):
        self.offset(depth)
        self.s(str(node.label))

    def write_apply(self, node, depth=0):
        self.offset(depth)
        self.write_node(node.function)
        self.lparen()
        self.write_args(node.args)
        self.rparen()

    def write_list(self, node, depth=0):
        self.s('HListOf{0}('.format(len(node.items)))
        for i in node.items[:-1]:
            self.write_node(i)
            self.comma()
            self.ws()
        self.write_node(node.items[-1])
        self.s(')')

    def write_args(self, args, depth=0):
        for arg in args[:-1]:
            self.write_node(arg)
            self.comma()
            self.ws()
        self.write_node(args[-1])

    write_integer = write_float = write_n

    def write_bool(self, node, depth=0):
        self.offset(depth)
        self.s(node.label.lower())

    def write_string(self, node, depth=0):
        self.offset(depth)
        self.s('"%s"' % node.label)

    def write_type(self, h_type, depth=0):
        self.offset(depth)
        self.s(self.to_ctype(h_type))

    def write_assignment(self, node, depth=0):
        self.offset(depth)
        if node.label.label not in self.scopes[-1]:
            self.write_type(node.label.h_type)
            self.ws()
            self.scopes[-1][node.label.label] = node.label.h_type
        self.write_node(node.label)
        self.ws()
        self.s('=')
        self.ws()
        self.write_node(node.right)

    def to_ctype(self, h_type):
        return getattr(self, 'to_ctype_' + type(h_type).__name__.lower())(h_type)

    def to_ctype_function(self, h_type):
        return self.to_ctype(h_type.types[1])

    def to_ctype_typeoperator(self, h_type):
        if h_type.name == 'List':
            return 'HList_{0}'.format(self.to_ctype(h_type.types[0]))
        elif h_type.name == 'Function':
            return 'HFunction'
        elif len(h_type.types) == 0:
            return 'H{0}'.format(h_type.name)
        else:
            return 'WTF'

    def to_ctype_typevariable(self, h_type):
        return self.to_ctype(h_type.instance)

    def to_ctype_list(self, h_type):
        print(h_type)
        return 'HList_{0}'.format(self.to_ctype(h_type.types[0]))

    def to_ctype_nonetype(self, h_type):
        return 'None'
