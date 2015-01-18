import ast


def dump(node, annotate_fields=True, include_attributes=False):
    """
    A patched ast.dump function which shows the atypical type annotations and indents
    """
    def _format(node, adjust):
        if isinstance(node, ast.AST):
            fields = [(a, _format(b, adjust + 1)) for a, b in ast.iter_fields(node)]
            a_data = ['typeclass', 'type', 'native', 'template', 'wtf']
            for bnm in a_data:
                if hasattr(node, 'a_%s' % bnm):
                    fields.append(('a_%s' % bnm, str(getattr(node, 'a_%s' % bnm))))

            if len(fields) > 0:
                rv = '%s(\n%s' % (node.__class__.__name__, '\n'.join(
                    ('%s%s=%s' % tuple(['  ' * (adjust + 1)] + list(field)) for field in fields)
                    if annotate_fields else
                    (b for a, b in fields)
                ))
            else:
                rv = '%s()' % (node.__class__.__name__)
            if include_attributes and node._attributes:
                rv += fields and '\n' or ''
                rv += '\n'.join('%s%s=%s' % ('  ' * (adjust + 1), a, _format(getattr(node, a), adjust + 1))
                                for a in node._attributes)
            return rv + ')'
        elif isinstance(node, list):
            if len(node) <= 0:
                return '[%s]' % ', '.join(_format(x, 0) for x in node)
            else:
                return '[\n%s]' % ('\n'.join('%s%s' % ('  ' * (adjust + 1), _format(x, adjust + 1))
                                   for x in node))
        return repr(node)
    if not isinstance(node, ast.AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node, 0)
