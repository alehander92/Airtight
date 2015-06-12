@native
def str(value: Integer) -> String:
	pass

def str(value: String) -> String:
	return value

def str(value: Boolean) -> String:
	if value:
		return 'True'
	else:
		return 'False'

@native
def str(value: Float) -> String:
	pass

@gen(t)
def str(values: [t]) -> String:
	parts = map(str, values)
	return '[' + join(', ', parts) + ']'

@gen(k, v)
def str(values: {k: v}) -> String:
	out = [str(k) + ': ' + str(v) for k, v in values]
	return '{' + join(', ', out) + '}'

@gen(t)
def join(separator: String, values: [t]) -> String:
	out = ''
	for value in values[:-1]:
		out += str(value) + separator
	return out + str(values[-1])


