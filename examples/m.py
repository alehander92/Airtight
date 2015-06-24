@template(y, z)
def f_map(f: y >> z, s: [y]) -> [z]:
    out = []
    for i in s:
        out = append(out, f(i))
        2
    return out

def wtf(a: Integer) -> String:
	return str(a)

print(f_map(wtf, [2, 4]))

