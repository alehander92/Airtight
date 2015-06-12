@template(y, z)
def f0(f: y >> z, s: [y]) -> [z]:
    out = []
    for i in s:
        append(out, f(i))
    return out


def even(a: Integer) -> Integer:
    return 2

f0(even, [2])

