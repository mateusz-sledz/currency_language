from interpreter.interpreter import Interpreter
import sys


if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    file = 'program.txt'

interpreter = Interpreter(file)

interpreter.interprete()


