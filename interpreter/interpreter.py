import parser.parser as parser
import load_data as load
import sys


class Interpreter:
    
    def __init__(self, file):
        self.variables = {}
        self.currency_variables = {}
        self.functions = {}
        self.currencies = ''
        self.paramlists = {}
        self.tree = ()
        self.currencies = load.get_currencies_from_file("przelicznik.txt")
        
        if '.txt' in file:
            program = load.get_code(file)
        else:
            program = file

        self.tree, self.functions, self.paramlists = parser.get_products(program)
        parser.restart()

    def interprete(self):
            
        def basic_operations(p, if_currency):
    
            value, ifcurr = run(p[1], if_currency)
            value2, ifcurr2 = run(p[2], if_currency)
    
            if p[0] == '*':
                if ifcurr2 is True or ifcurr is True:
                    return value * value2, True
    
                elif ifcurr is False and ifcurr2 is False:
                    return value * value2, False
    
            elif p[0] == '/':
                if ifcurr2 is True or ifcurr is True:
                    return value / value2, True
    
                elif ifcurr is False and ifcurr2 is False:
                    return value / value2, False
    
            elif p[0] == '+':
                if ifcurr == ifcurr2:
                    return value + value2, ifcurr
                else:
                    print("ERROR Interpreter: Adding currency to int:", p[1], " Value:", value, "If currency: ", ifcurr,
                          "  PLUS  ", p[2], "Value:", value2, "If currency: ", ifcurr2)
                    sys.exit(1)
    
            elif p[0] == '-':
    
                if ifcurr == ifcurr2:
                    return value - value2, ifcurr
                else:
                    print("ERROR Interpreter: Subtracting currency and int:", p[1], " Value:", value, "If currency: ",
                          ifcurr,
                          "  PLUS  ", p[2], "Value:", value2, "If currency: ", ifcurr2)
                    sys.exit(1)
    
        def compare_operations(p, if_currency):
    
            value, ifcurr = run(p[1], if_currency)
            value2, ifcurr2 = run(p[2], if_currency)
    
            if ifcurr == ifcurr2:
                if p[0] == '<':
                    return value < value2
                if p[0] == '>':
                    return value > value2
                if p[0] == '==':
                    return value == value2
                if p[0] == '!=':
                    return value != value2
                if p[0] == '<=':
                    return value <= value2
                if p[0] == '>=':
                    return value >= value2
    
            else:
                print("ERROR Interpreter: Cannot compare type int and type currency")
                sys.exit(1)
    
        def is_declared(variable):
            if variable in self.currency_variables:
                return 'currency'
            elif variable in self.variables:
                return 'variable'
            else:
                return False
    
        def run(p, if_currency=False):
            if type(p) == tuple:
                if p[0] == '=':
    
                    value, ifcurr = run(p[2], if_currency)
    
                    if p[1] in self.currency_variables and ifcurr is True or p[1] in self.variables and ifcurr is False and p[1] not \
                            in self.currency_variables:
                        self.variables[p[1]] = value
                        return
                    elif is_declared(p[1]) is False:
                        print("ERROR Interpreter: Using undeclared variable")
                        sys.exit(1)
                    else:
                        print("ERROR IOnterpreter: assigning currency to int or int to currency")
                        sys.exit(1)
    
                if p[0] == '+' or p[0] == '-' or p[0] == '*' or p[0] == '/':
                    return basic_operations(p, if_currency)
    
                if p[0] == 'var':
                    if p[1] not in self.variables:
                        print("ERROR Interpreter: Usage of Undeclared variable: ", p[1])
                        sys.exit(1)
                    else:
                        if p[1] in self.currency_variables:
                            return self.variables[p[1]], True
                        else:
                            return self.variables[p[1]], False
    
                if p[0] == 'ASSIGN':
                    if type(p[2]) is tuple:
                        if p[2][0] in self.currencies:
                            self.currency_variables[p[1]] = p[2][0]
                            self.variables[p[1]], ifcurr = run(p[2], if_currency)
                            return
                        else:
                            print("Interpreter Error: No such currency declared: ", p[2][0])
                            sys.exit(1)
                    else:
                        self.variables[p[1]] = p[2]
                        return
    
                elif p[0] == 'printstring':
                    print(p[1])
                    return
    
                elif p[0] == 'printvar':
                    if p[1] in self.currency_variables:
                        currency = self.currency_variables[p[1]]
                        print(round(self.variables[p[1]] * int(self.currencies[currency]), 1), currency)
                        return
                    elif p[1] in self.variables:
                        print(round(self.variables[p[1]], 1))
                        return
                    else:
                        print("ERROR Interpreter: Used undeclared variable")
                        sys.exit(1)
    
                elif p[0] == 'if':

                    logic_value = run(p[1])
                    if logic_value is True and type(p[2][0]) is tuple:
                        for statement in p[2]:
                            run(statement)
                    elif logic_value is True:
                        run(p[2])
                    return
    
                elif p[0] == '|':
    
                    outcome = False
                    for orstatement in p[1:]:
                        logic_value = run(orstatement)
                        outcome = outcome or logic_value
                    return outcome
    
                elif p[0] == '&':
    
                    outcome = True
                    for andstatement in p[1:]:
                        logic_value = run(andstatement)
                        outcome = outcome and logic_value
                    return outcome
    
                elif p[0] == '<' or p[0] == '>' or p[0] == '==' or p[0] == '!=' or p[0] == '>=' or p[0] == '<=':
                    return compare_operations(p, if_currency)
    
                elif p[0] == 'while':
                    while run(p[1]) is True:
                        if type(p[2][0]) is tuple:
                            for statement in p[2]:
                                run(statement)
                        else:
                            run(p[2])

                    return
    
                elif p[0] == 'functioncall':
                    if p[1] in self.functions:
    
                        if type(self.paramlists[p[1]]) is tuple and type(p[2]) is tuple:
                            if len(p[2]) != len(self.paramlists[p[1]]):
                                print("ERROR Interpreter: No matching function:", p[1])
                                sys.exit(1)
    
                            for var, value in zip(self.paramlists[p[1]], p[2]):
                                if type(value) is tuple and value[0] not in self.currencies:
                                    var_declared = value[1]
                                    if var_declared in self.currency_variables:
                                        value = (self.currency_variables[var_declared],
                                                 self.variables[var_declared] * int(self.currencies[self.currency_variables[var_declared]]))
                                    else:
                                        value = self.variables[var_declared]
                                run(('ASSIGN', var, value))
    
                        elif self.paramlists[p[1]] is not None and p[2] is not None:

                            var = self.paramlists[p[1]]
                            value = p[2]

                            if type(self.paramlists[p[1]]) is tuple or type(p[2]) is tuple and p[2][0] not in self.currencies and p[2][0] != 'var':
                                print("ERROR Interpreter: No matching function", p[1])
                                sys.exit(1)
                            elif type(p[2]) is tuple and p[2][0] == 'var':
                                print("czy to tu")
                                var_declared = p[2][1]
                                var = self.paramlists[p[1]]
                                if var_declared in self.currency_variables:
                                    value = (self.currency_variables[var_declared],
                                             self.variables[var_declared] * int(self.currencies[self.currency_variables[var_declared]]))
                                else:
                                    value = self.variables[var_declared]
                            run(('ASSIGN', var, value))
    
                        elif self.paramlists[p[1]] is None and p[2] is None:
                            pass
                        else:
                            print("ERROR Interpreter: No matching function", p[1])
                            sys.exit(1)

                        statements = self.functions[p[1]]
    
                        if type(statements[0]) is not tuple:
                            statements = (statements,)
    
                        for statement in statements:
                            sth = run(statement)
                            if sth is not None:
                                return sth
    
                        return
                    else:
                        print("ERROR Interpreter: function", p[1], "not defined.")
                        return
    
                if p[0] == 'return':
                    return run(p[1])
    
                if p[0] == 'functionassign':
    
                    from_return, if_currency = run(p[2])
    
                    if is_declared(p[1]) == 'currency' and if_currency is True:
                        run(('=', p[1], (self.currency_variables[p[1]], from_return * int(self.currencies[self.currency_variables[p[1]]]))))
    
                    elif is_declared(p[1]) == 'variable' and if_currency is False:
                        run(('=', p[1], from_return))
                    else:
                        print("ERROR Interpreter: Function returned value assigned to undeclared variable")
                        sys.exit(1)
                    return
    
                if p[0] in self.currencies:
                    return p[1] / int(self.currencies[p[0]]), True
    
                else:
                    print("ERROR Interpreter: No such currency declared: ", p[0])
                    return
            else:
                return p, if_currency

        for x in self.tree:
            run(x)
