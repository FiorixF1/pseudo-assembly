import sys

# ---------------------------------------------------- #

CODE = [None]
PROGRAM_COUNTER = 1
ACCUMULATOR = None
MEMORY = dict()

OPCODES = { "READ":      lambda  : read(),
            "WRITE":     lambda  : write(),
            "ADD":       lambda x: math(x, '+'),
            "SUB":       lambda x: math(x, '-'),
            "MULT":      lambda x: math(x, '*'),
            "DIV":       lambda x: math(x, '/'),
            "ADD=":      lambda x: explicit_math(x, '+'),
            "SUB=":      lambda x: explicit_math(x, '-'),
            "MULT=":     lambda x: explicit_math(x, '*'),
            "DIV=":      lambda x: explicit_math(x, '/'),
            "ADD@":      lambda x: indirect_math(x, '+'),
            "SUB@":      lambda x: indirect_math(x, '-'),
            "MULT@":     lambda x: indirect_math(x, '*'),
            "DIV@":      lambda x: indirect_math(x, '/'),
            "LOAD":      lambda x: load(x),
            "LOAD=":     lambda x: explicit_load(x),
            "LOAD@":     lambda x: indirect_load(x),
            "STORE":     lambda x: store(x),
            "STORE@":    lambda x: indirect_store(x),
            "BR":        lambda x: branch(x, ''),
            "BEQ":       lambda x: branch(x, '=='),
            "BNE":       lambda x: branch(x, '!='),
            "BL":        lambda x: branch(x, '<'),
            "BLE":       lambda x: branch(x, '<='),
            "BG":        lambda x: branch(x, '>'),
            "BGE":       lambda x: branch(x, '>='),
            "END":       lambda  : end()
          }

# ---------------------------------------------------- #

def read():
    global ACCUMULATOR
    try:
        ACCUMULATOR = int(input())
    except ValueError:
        error("Input must be an integer")

def write():
    if ACCUMULATOR == None:
        error("Undefined accumulator")
    print(ACCUMULATOR)

def math(param, op):
    global ACCUMULATOR
    try:
        if   param[0] == '=':   value = int(param[1:])
        elif param[0] == '@':   value = MEMORY[MEMORY[int(param[1:])]]
        else:                   value = MEMORY[int(param)]
        
        if   op == '+':         ACCUMULATOR += value
        elif op == '-':         ACCUMULATOR -= value
        elif op == '*':         ACCUMULATOR *= value
        elif op == '/':         ACCUMULATOR /= value
    except ValueError:
        error("Parameter must be an integer")
    except TypeError:
        error("Undefined accumulator")
    except KeyError:
        error("Undefined memory location")
    except ZeroDivisionError:
        error("Division by zero")

def explicit_math(param, op):
    math('=' + param, op)

def indirect_math(param, op):
    math('@' + param, op)

def load(param):
    global ACCUMULATOR
    try:
        if   param[0] == '=':   ACCUMULATOR = int(param[1:])
        elif param[0] == '@':   ACCUMULATOR = MEMORY[MEMORY[int(param[1:])]]
        else:                   ACCUMULATOR = MEMORY[int(param)]
    except ValueError:
        error("Parameter must be an integer")
    except KeyError:
        error("Undefined memory location")

def explicit_load(param):
    load('=' + param)

def indirect_load(param):
    load('@' + param)
    
def store(param):
    global MEMORY
    try:
        if   param[0] == '@':   MEMORY[MEMORY[int(param[1:])]] = ACCUMULATOR
        else:                   MEMORY[int(param)] = ACCUMULATOR
    except ValueError:
        error("Parameter must be an integer")
    except TypeError:
        error("Undefined accumulator")

def indirect_store(param):
    store('@' + param)
    
def branch(param, cond):
    global PROGRAM_COUNTER
    try:
        target = int(param)-1
        # program_counter is automatically incremented by the main loop
        if target < 0 or target >= len(CODE)-1:
            error("Branch to undefined instruction")
        if  cond == ''   or \
            cond == '==' and ACCUMULATOR == 0 or \
            cond == '!=' and ACCUMULATOR != 0 or \
            cond == '<'  and ACCUMULATOR <  0 or \
            cond == '<=' and ACCUMULATOR <= 0 or \
            cond == '>'  and ACCUMULATOR >  0 or \
            cond == '>=' and ACCUMULATOR >= 0:
                PROGRAM_COUNTER = target
    except ValueError:
        error("Parameter must be an integer")

def end():
    exit()
    
def error(msg):
    print("ERROR AT LINE {0} - {1}".format(PROGRAM_COUNTER, msg))
    exit()
    
def execute(instruction):
    try:
        parameters = instruction.split()
        opcode = parameters[0].upper()

        if len(parameters) == 2:
            OPCODES[opcode](parameters[1])
        else:
            OPCODES[opcode]()

    except TypeError:
        error("Wrong number of parameters")
    
# ---------------------------------------------------- #

if len(sys.argv) < 2:
    print("Specify the file to execute as parameter")
    exit()

with open(sys.argv[1]) as program:
    CODE.extend(program.readlines())

while PROGRAM_COUNTER > 0 and PROGRAM_COUNTER < len(CODE):
    instruction = CODE[PROGRAM_COUNTER]
    execute(instruction)
    PROGRAM_COUNTER += 1
