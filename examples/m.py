@template(y, z)
def f_map(f: y >> z, s: [y]) -> [z]:
    out = []
    for i in s:
        out = append(out, f(i))
    return out

def nope(a: Integer) -> Integer:
    return a + 4

print(f_map(nope, [2, 4]))

