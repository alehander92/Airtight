import copy
import os
from hermetic.ll_ast import *
import hermetic.hindley_milner_ast as hm_ast

def e(obj, attr):
    print('%s: %s' % (attr, str(getattr(obj, attr))))
    input()

class Generator:
    def __init__(self, ast):
        self.ast = ast
        self.out = []
        self.scopes = [{}]
        self.current_actuals = {}
        self.current_function_idents = set()
        self.c = set()
        self.libs = ['stdlib', 'stdbool', 'stddef', 'string', 'stdarg']
        self.functions = {}

    def generate(self):
        methods = [node for node in self.ast.expressions if node.type == 'method']
        main = [node for node in self.ast.expressions if node.type != 'method']
        # methods.append(LLAst(
        #     type='method',
        #     label=LLAst(type='ident', label='main', h_type=CType('void')),
        #     body=LLAst(type='lambda', args=[], body=main, h_type=CType('void')),
        #     h_type=CType('void')))
        for method in methods:
            self.register_func(method)

        for z in self.ast.expressions:
            self.register_apply(z)
        for k, f in self.functions.items():
            print(k, ':', f.__dict__)
            # print(self.functions.keys(), list(self.functions.values())[0].__dict__)
        for method in self.functions.values():
            method.render_all()
            self.nl()

        self.s('int main(){\n')
        for e in main:
            self.write_node(e, 1)
            self.semi()
            self.nl()
        self.offset(1)
        self.s('return 0;\n')
        self.rcurly()
        self.nl()

        l = self.render_c() 
        s = ''.join(self.out)
        return l + '\n' + s

    def render_c(self):
        return self.render_includes() + '\n\n' + self.render_string() + '\n\n' + self.render_l()

    def render_string(self):
        return self.gen_c('string.c')

    def render_l(self):
        input(str(self.c))
        return '\n'.join(self.gen_c('list.c', list_type='HList_' + elem_type, elem_type=elem_type) for elem_type in self.c)

    def render_includes(self):
        return '\n'.join('#include<' + lib_name + '.h>' for lib_name in self.libs)

    def gen_c(self, file, **kwargs):
        with open(os.path.join('core', file), 'r') as f:
            t = f.read()
        for k, v in kwargs.items():
            t = t.replace('%{' + k + '}', v)
        return t  

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

class CType:
    def __init__(self, label):
        self.label = label

class FunctionGenerator:
    def __init__(self, ast, c_generator):
        self.node, self.arg_types, self.return_type = ast, [a.h_type for a in ast.body.args], ast.h_type
        self.c_generator = c_generator

        self.actuals = set()

    def load_registry(self, met, actual_arg_types, actual_return_type):
        for a, actual in zip(met.body.args, actual_arg_types):
            self.load_arg([h.instance.name if h.instance else h.name for h in met.h_vars], a.h_type, actual)
        self.load_arg([h.instance.name if h.instance else h.name for h in met.h_vars], met.body.h_type, actual_return_type)
        print([h.instance.name if h.instance else h.name for h in met.h_vars])
        print(actual_arg_types[0])
        e(self.c_generator, 'registry')

    def load_arg(self, h_vars, met_type, actual_type):
        if h_vars:
            print(hasattr(met_type, 'types'), type(met_type))
            # print(2, 'm type:', met_type, 'a type', actual_type, 'm name', met_type.name, 'h0', h_vars[0], 'h1', h_vars[1]);input()

        if isinstance(met_type, TypeVariable) and met_type.name in h_vars:
            self.c_generator.registry[met_type.name] = actual_type
        elif hasattr(met_type, 'instance') and met_type.instance:
            self.load_arg(h_vars, met_type.instance, actual_type)
        if hasattr(met_type, 'types') and hasattr(actual_type, 'types'):
            for t, z_child in zip(met_type.types, actual_type.types):
                self.load_arg(h_vars, t, z_child)


    def render(self, actual_arg_types, actual_return_type):
        m = copy.copy(self.node)
        m.body.h_type = m.h_type = actual_return_type
        self.c_generator.registry = {}
        self.load_registry(m, actual_arg_types, actual_return_type)
        # for a, actual in zip(m.body.args, actual_arg_types):

        self.c_generator.current_actuals = {v.name : w for v, w in zip(self.node.h_vars, list(actual_arg_types) + [actual_return_type])}
        self.c_generator.current_function_idents = set()
        # print(self.c_generator.current_actuals );input()
        self.c_generator.write_method(m)
        self.c_generator.nl()

    def render_all(self):
        if self.node.h_vars:
            for a in self.actuals:
                self.render(a[0], a[1])
        else:
            self.render(self.arg_types, self.return_type)

class CGenerator(Generator):
    OFFSET = '    '

    def ref(self):
        self.out.append('*')

    def register_func(self, func):
        self.functions[func.label.label] = FunctionGenerator(func, self)

    def register_apply(self, node):
        if node.type == 'apply':
            if node.function.type == 'ident' and\
               not isinstance(node.h_type, hm_ast.TypeVariable) and\
               not any(isinstance(arg.h_type, hm_ast.TypeVariable) for arg in node.args):
                if node.function.label in self.functions:
                    self.functions[node.function.label].actuals.add((tuple(arg.h_type for arg in node.args), node.h_type))
                node._special = True
        # print(node.data, node.__dict__);input()
        for k, v in node.data.items():
            if hasattr(v, 'type'):
                self.register_apply(v)
            elif isinstance(v, list):
                for e in v:
                    if hasattr(e, 'type'):
                        self.register_apply(e)

    def write_node(self, node, depth=0):
        getattr(self, 'write_' + node.type)(node, depth)

    def write_method(self, method, depth=0):
        self.offset(depth)
        q_label = copy.copy(method.label)
        self.write_type(method.body.h_return_type)
        self.ws()
        q_label.h_type = Multi_Function([arg.h_type for arg in method.body.args] + [method.body.h_return_type])

        print(method.body.args[0].h_type, self.to_ctype(method.body.args[0].h_type));input('?')
        self.write_special_ident(q_label, [arg.h_type for arg in method.body.args], method.body.h_return_type)
        # print(method.body.h_return_type, method.body.h_return_type);input()
        # print(q_label, method.body.h_return_type, method.h_vars[1]);input()# print(method.h_type.types[1]);input()
        # if True: #method.h_vars:
        #     self.write_with_type(q_label, special=True, arg_types=[arg.h_type for arg in method.body.args], return_type=q_label.h_type)
        # else:
        #     self.write_with_type(q_label)
        self.lparen()
        self.write_m_args(method.body.args, method.h_type)
        self.rparen()
        self.lcurly()
        self.nl()

        body = method.body.body if isinstance(method.body.body, list) else [method.body.body]
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
        for arg in args[:-1]:
            self.write_with_type(arg)
            self.comma()
            self.ws()
        self.write_with_type(args[-1])

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

    def write_for(self, node, depth=0):
        self.offset(depth)
        self.s('for')
        self.lparen()
        self.s('int')
        self.ws()
        self.s('i=0;i<h_length_{0}_int('.format(self.to_ctype(node.iter.h_type)))
        self.write_node(node.iter)
        self.rparen()
        self.semi()
        self.s('i++){')
        self.nl()
        self.offset(depth + 1)
        self.write_with_type(node.target)
        self.s(' = ')
        self.s('h_index_{0}_int_{1}('.format(self.to_ctype(node.iter.h_type), self.to_ctype(node.target.h_type)))
        self.write_node(node.iter)
        self.s(', i);')
        self.nl()
        body = node.body if isinstance(node.body, list) else [node.body]
        for e in body:
            self.write_node(e, depth + 1)

            self.semi()
            self.nl()
        self.offset(depth)
        self.rcurly()
        self.nl()

    def write_ident(self, node, depth=0):
        self.offset(depth)
        # print(self.current_function_idents);input()
        if node.label in self.current_function_idents:
            self.lparen()
            self.ref()
            self.s('h_' + str(node.label))
            self.rparen()
        else:
            self.s('h_' + str(node.label))

    def write_n(self, node, depth=0):
        self.offset(depth)
        self.s(str(node.label))

    def write_apply(self, node, depth=0):
        self.offset(depth)
        # if node.function.type == 'ident':
        #     f = self.functions[node.name]
        #     if f.h_

        if node.function.type == 'ident' and node.function.label not in self.current_function_idents: # node._special and node.function.type == 'ident':
            print([print(arg, arg.h_type) for arg in node.args])
            print(node.h_type)
            arg_types = []
            for arg in node.args + [node]:
                if hasattr(arg.h_type, 'instance') and arg.h_type.instance:
                    arg.h_type = arg.h_type.instance

                if arg.type == 'apply' and hasattr(arg.h_type, 'types') and len(arg.h_type.types) > 0:
                    arg_types.append(arg.h_type.types[-1])
                else:
                    arg_types.append(arg.h_type)
            for a in arg_types: print(a)

            input(' ')
            self.write_special_ident(node.function, arg_types[:-1], arg_types[-1])
        else:
            input('fun: ' + str(node))
            self.write_node(node.function)
        self.lparen()
        self.write_args(node.args)
        self.rparen()

    def write_special_ident(self, node, arg_types, return_type, depth=0):
        self.offset(depth)
        self.s('h_' + node.label)
        self.s('_')
        for arg_type in arg_types:
            if node.label == 'append':
                input('#')
                input(node.label + str(arg_type) + str(type(arg_type)))
            self.write_type(arg_type)
            self.s('_')

        self.write_type(return_type)

    def write_list(self, node, depth=0):
        if not node.items:
            self.s('{0}Of(0)'.format(self.to_ctype(node.h_type)))
            return
        self.s('{0}Of({1}, '.format(self.to_ctype(node.h_type), len(node.items)))
        for i in node.items[:-1]:
            self.write_node(i)
            self.comma()
            self.ws()
        self.write_node(node.items[-1])
        self.s(')')

    def write_args(self, args, depth=0):
        for arg in args[:-1]:
            if arg.type == 'ident' and arg.label in self.functions:
                self.s('&')
                print([arg.h_type.types[:-1]], arg.h_type.types[-1])
                self.write_special_ident(arg, arg.h_type.types[:-1], arg.h_type.types[-1])
            else:
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
        self.s('HStringFrom("%s")' % node.label)

    def write_type(self, h_type, depth=0):
        self.offset(depth)
        self.s(self.to_ctype(h_type))


    def write_with_type(self, node, special=False, arg_types=None, return_type=None, depth=0):
        self.offset(depth)
        if hasattr(node.h_type, 'instance') and node.h_type.instance:
            node.h_type = node.h_type.instance

        if isinstance(node.h_type, hm_ast.Function):
            self.write_type(node.h_type.types[-1])
            self.ws()
            self.lparen()
            self.ref()
            if special:
                self.write_special_ident(node, arg_types, return_type)
            else:
                self.write_node(node)
            self.rparen()
            self.lparen()
            for a in node.h_type.types[:-2]:
                self.write_type(a)
                self.comma()
            self.write_type(node.h_type.types[-2])
            self.rparen()

            self.current_function_idents.add(node.label)
        elif isinstance(node.h_type, hm_ast.List) or node.h_type.name == 'list':
            print('before write_with_type:', ''.join(self.out))
            i = len(self.out)
            self.s('HList_')
            self.write_type(node.h_type.types[0])
            self.c.add(self.to_ctype(node.h_type.types[0]))
            self.ws()
            print('after write_with_type:', ''.join(self.out))
            if special:
                self.write_special_ident(node, arg_types, return_type)
            else:
                self.write_node(node)
        else:
            self.write_type(node.h_type)
            self.ws()
            if special:
                self.write_special_ident(node, arg_types, return_type)
            else:
                self.write_node(node)


    def write_assignment(self, node, depth=0):
        self.offset(depth)
        if node.label.label not in self.scopes[-1]:
            print('AS', node.label.h_type.types[0], self.registry)
            self.write_type(node.label.h_type)
            self.ws()
            self.scopes[-1][node.label.label] = node.label.h_type
        self.write_node(node.label)
        self.ws()
        self.s('=')
        self.ws()
        self.write_node(node.right)

    def to_ctype(self, h_type):
        native_types = {'Integer': 'int', 'Float': 'float', 'Bool': 'bool'}
                # hm_ast.Integer: 'int',
                # hm_ast.Float: 'float',
                # hm_ast.Bool: 'bool'}
        # if h_type.name != str(h_type):
        #     print(h_type, h_type.name);print(h_type.instance, h_type.instance.name);input()
        if h_type.name == 'list':
            2#print(h_type)
            #input('?')
        if hasattr(h_type, 'instance') and h_type.instance:
            h_type = h_type.instance
        if hasattr(h_type, 'types'):
            for i in range(len(h_type.types)):
                if hasattr(h_type.types[i], 'instance') and h_type.types[i].instance:
                    h_type.types[i] = h_type.types[i].instance

        print(h_type, h_type.__dict__, type(h_type))
        
        if hasattr(h_type, 'name') and h_type.name in native_types:
            return native_types[h_type.name]
        elif hasattr(h_type, 'instance') and h_type.instance and h_type.instance.name in native_types:
            return native_types[h_type.instance.name]
        else:
            return getattr(self, 'to_ctype_' + type(h_type).__name__.lower())(h_type)

    def to_ctype_function(self, h_type):
        return '{0}REF{1}'.format(self.to_ctype(h_type.types[0]), '_'.join(self.to_ctype(h) for h in h_type.types[1:]))
        
    def to_ctype_typeoperator(self, h_type):
        if h_type.name == 'list':
            self.c.add(self.to_ctype(h_type.types[0]))
            return 'HList_{0}'.format(self.to_ctype(h_type.types[0]))
        elif h_type.name == 'function':
            return 'HFunction'
        elif len(h_type.types) == 0:
            return 'H{0}'.format(h_type.name)
        elif h_type.name == '->':
            return '{0}REF{1}'.format(self.to_ctype(h_type.types[0]),
                                      '_'.join(self.to_ctype(h) for h in h_type.types[1:]))

    def to_ctype_typevariable(self, h_type):
        i = h_type.instance
        if i:
            return self.to_ctype(h_type.instance)
        elif h_type.name in self.registry:
            return self.to_ctype(self.registry[h_type.name])
        else:
            return h_type.name

    def to_ctype_list(self, h_type):
        self.c.add(self.to_ctype(h_type.types[0]))
        return 'HList_{0}'.format(self.to_ctype(h_type.types[0]))

    def to_ctype_nonetype(self, h_type):
        return 'None'

    def to_ctype_ctype(self, c_type):
        return c_type.label

