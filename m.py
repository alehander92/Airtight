def m(a: Integer) -> Integer:
	b = [a, a]
	return map(lambda f: f + 2, b)

def call(a: Integer >> Integer) -> Integer:
	return a(2)

