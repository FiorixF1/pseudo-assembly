# Pseudo-Assembly
This repository contains a simulator for a ficticious Assembly language used for didactic purposes.

## Architecture
The language runs on a virtual machine providing this architecture:
- An input tape used for reading data from the keyboard
- An output tape used for writing data on the screen
- A central memory for storing data
- A processor with one register called "accumulator"

## Instruction set
Each instruction is composed by the opcode plus a parameter (not present in all instructions).

### I/O
```READ```
    Read an integer value from the input tape and store it in the accumulator.
```WRITE```
    Write the integer value stored in the accumulator on the screen.

### Memory
```LOAD x```
    Load the value stored at memory location x in the accumulator.
```STORE x```
    Store a value from the accumulator to memory location x.

### Arithmetic
```ADD x```
```SUB x```
```MULT x```
```DIV x```
    Perform an arithmetic operation where the first operand is the accumulator, the second operand is the value stored at memory location x and the result is saved in the accumulator.

### Branching
```BR x```
    Unconditional jump to line x (where 1 is the first line).

```BEQ x```
```BNE x```
```BL x```
```BLE x```
```BG x```
```BGE x```
    Jump to line x if accumulator is equal to / not equal to / greater than / greater or equal to / less than / less or equal to 0.

### Other
```END```
    End the program.

### Addressing modes
```OP x```
    Direct addressing: get the value stored at memory location x.

```OP @x``` or ```OP@ x```
    Indirect addressing: get the value stored at the address specified in the memory location x.

```OP =x``` or ```OP= x```
    Explicit addressing: use x as parameter.

Arithmetic and memory instructions can use all of these addressing modes, except ```STORE =x``` since it does not make sense.

## How to use it

Write the program on a text file and then execute the script ```pseudo-assembly.py``` in the Python 3 interpreter giving as command line parameter the created file. For example:
```
    python pseudo-assembly.py test.asm
```

The code must be written with one instruction for each line, without line number.