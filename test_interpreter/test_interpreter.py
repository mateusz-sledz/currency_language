import pytest
from interpreter.interpreter import Interpreter


def test_variable_assignment(capsys):
    x = 'var x = 100 '
    y = 'var y = 200 [USD] '
    print = 'print(y) print(x)'

    interpreter = Interpreter(x + y + print)
    interpreter.interprete()

    out, err = capsys.readouterr()

    varss = interpreter.variables

    assert varss['x'] == 100
    assert out == '200.0 USD\n100\n'


def test_operation_plus():
    z = '777'
    t = '666'
    program = 'var z = ' + z + '  var t = ' + t + ' var p = 0  p =  z + t'

    interpreter2 = Interpreter(program)
    interpreter2.interprete()

    vars2 = interpreter2.variables

    assert int(z) + int(t) == vars2['p']


def test_function_call(capsys):

    program = 'def func(x, y, z) {  '   \
              'print(x)  '              \
              'print(y)  '              \
              'print(z) } '             \
              'func(1, 2 ,3)    '

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '1\n2\n3\n'


def test_function_call_currencies(capsys):

    program = 'def func(x, y, z) {  '   \
              'print(x)  '              \
              'print(y)  '              \
              'print(z) } '             \
              'func(1 [USD], 2 [CHF], 3 [DKK])    '

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '1.0 USD\n2.0 CHF\n3.0 DKK\n'


def test_function_return(capsys):
    program = 'def func(x, y){' \
              'return x + y }' \
              'var x = 0' \
              'x = func(10, 10)' \
              'print(x)'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == str(10 + 10) + '\n'


def test_function_return_currency(capsys):
    program = 'def func(x, y, z){' \
              'return x + y + z }' \
              'var result = 0 [USD]' \
              'result = func(1 [USD], 1 [USD] , 1 [USD])' \
              'print(result)'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '3.0 USD\n'


def test_if_condition_true(capsys):
    program = 'var x = 0' \
              'var y = 10' \
              'if( x <= y){' \
              'print(y) }'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '10\n'

    out = ''


def test_if_condition_false(capsys):
    program = 'var x = 0' \
              'var y = 10' \
              'if( x > y){' \
              'print(y) }'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == ''


def test_condition_and_true(capsys):
    program = 'var x = 10' \
              'var y = 1 [USD]' \
              'if( 0 < x & y > 0[USD]){' \
              'print( x) }' \

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '10\n'


def test_condition_and_false(capsys):
    program = 'var x = 10' \
              'var y = 1 [USD]' \
              'if( 0 > x & y > 0[USD]){' \
              'print( x) }' \

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == ''


def test_condition_or_true(capsys):
    program = 'var x = 10' \
              'var y = 1 [USD]' \
              'if( 0 > x | y > 0[USD]){' \
              'print( x) }' \

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '10\n'


def test_condition_or_false(capsys):
    program = 'var x = 10' \
              'var y = 1 [USD]' \
              'if( 0 > x | y < 0[USD]){' \
              'print( x) }' \

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == ''


def test_condition_or_and_true(capsys):
    program = 'var x = 0' \
              'var y = 5 [USD]' \
              'if( 0 == x & y < 10 [USD] | 0 != 0 ){' \
              'print(x) } '

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '0\n'


def test_condition_or_and_false(capsys):
    program = 'var x = 0' \
              'var y = 5 [USD]' \
              'if( 0 != x & y < 10 [USD] | 0 != 0 ){' \
              'print(x) } '

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == ''


def test_while_loop(capsys):
    program = 'var x = 0' \
              'while( 5 > x){' \
              'x = 1 + x }' \
              'print(x)'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '5\n'


def test_while_loop_currency(capsys):
    program = 'var x = 0 [USD]' \
              'while( x < 5 [USD]){' \
              'x = x + 1[USD] }' \
              'print(x)'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == '5.0 USD\n'


def test_basic_operations(capsys):
    program = 'var x = 0' \
              'x = 2 + 2 * 2' \
              'var t = 10' \
              'var y = 10 [CHF]' \
              'y = y /2 + y * 10' \
              'print(y)' \

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    variables = interpreter.variables

    assert variables['x'] == 6
    assert out == '105.0 CHF\n'


def test_print_string(capsys):
    program = 'print("to moj string")'

    interpreter = Interpreter(program)
    interpreter.interprete()

    out, err = capsys.readouterr()

    assert out == 'to moj string\n'


