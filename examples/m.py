def filter(f: y >> z, s: y) -> z:
    return f(s)

def even(a: Integer) -> Integer:
    return a + 2

filter(even, 2)
