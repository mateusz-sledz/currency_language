
def get_currencies_from_file(toread: str)->dict:
	with open(toread, 'r') as file:
		lines = file.read().splitlines()

	values = {}

	for line in lines:
		x = line.split(' ')
		values[x[0]] = x[1]

	assert len(values) != 0

	return values


def get_code(file):
	with open(file, 'r') as program:
		lines = program.read()

	return lines
