class TypeChecker:
    def __init__(self, tree):
        self.tree = tree
        self.type_env = {}

    def type_check(self):
        return self._type_check_node(self.tree.body)

    def _type_check_node(self, node):
        method = '_type_check_%s' % type(node).__name__.lower()
        return getattr(self, method)(node)

    def _type_check_list(self, nodes):
        return [self._type_check_node(node) for node in nodes]

