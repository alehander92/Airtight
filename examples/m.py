@template(y, z)
def a(f: y >> z, other: [y]) -> [z]:
    return [f(other[0])]

def even(a: Integer) -> Float:
	return 2.2

a(even, [2])
