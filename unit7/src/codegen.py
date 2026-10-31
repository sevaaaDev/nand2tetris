from enum import Enum
from typing import Callable
# the push and pop have 2 stage
# - load stage
# - push/pop stage
#
# the load stage prepare the content or an address to push or pop data.
# the push/pop stage put the data to the stack or put the stack data to an address
#
# because other command also uses push pop mechanism, we can reuse it.

def push(load):
    """the push mechanism take input from D register. it will push it to the stack"""
    return f"""
{load}

@SP
A=M
M=D
@SP
M=M+1
"""

def pop(load):
    """the pop mechanism take memory address from D register. it will pop the data to that address"""
    return f"""
{load}
@R13
M=D

@SP
M=M-1

A=M
D=M

@R13
A=M
M=D
"""
# from here, we can define other command using push and pop

# here are the segment accesor
def seg_offset_type(label: str, offset: str):
    return f"""
@{label}
D=M
@{offset}
A=D+A
"""

def load_content():
    return """
D=M
"""

def load_address():
    return """
D=A
"""

class Load(Enum):
    ADDRESS = load_address()
    CONTENT = load_content()

def seg_local(load: Load, offset: str, *_):
    return seg_offset_type("LCL", offset) + load.value

def seg_argument(load: Load, offset: str, *_):
    return seg_offset_type("ARG", offset) + load.value

def seg_this(load: Load, offset: str, *_):
    return seg_offset_type("THIS", offset) + load.value

def seg_that(load: Load, offset: str, *_):
    return seg_offset_type("THAT", offset) + load.value

def seg_constant(load: Load, value: str, *_):
    return f"""@{value}
D=A
"""

def seg_temp(load: Load, offset: str, *_):
    return f"""
@5
D=A
@{offset}
A=D+A
""" + load.value

def seg_pointer(load: Load, offset: str, *_):
    return f"@{'THIS' if offset == '0' else 'THAT'}" + load.value

def seg_static(load: Load, offset: str, *arg):
    filename = arg[0]
    return f"@{filename}.{offset}" + load.value

def seg_any(load: Load, addr: str, *_):
    return f"@{addr}" + load.value

SEGMENT_LOADER = {
    "local": seg_local, 
    "argument": seg_argument, 
    "this": seg_this, 
    "that": seg_that,
    "temp": seg_temp,
    "constant": seg_constant,
    "static": seg_static,
    "pointer": seg_pointer,
}

## Example usage
# pop(seg_local(Load.ADDRESS, "5"))

# push(SEGMENT_LOADER[self.segment](Load.CONTENT, self.arg, filename))
# pop(SEGMENT_LOADER[self.segment](Load.ADDRESS, self.arg, filename))

def op2(op: str):
    return f"""
@R14
D=M
@R15
D={op}
"""

def op1(op: str):
    return f"""
@R14
D={op}
"""

def math2_gen(op: str):
    def gen():
        return pop(seg_any(Load.ADDRESS, "R15")) + pop(seg_any(Load.ADDRESS, "R14")) + push(op2(op))
    return gen

def math1_gen(op: str):
    def gen():
        return pop(seg_any(Load.ADDRESS, "R14")) + push(op1(op))
    return gen

eq_count = 0

def cond_op(jmp: str):
    global eq_count
    return f"""
@R14
D=M
@R15
D=D-M
M=-1
@equality{eq_count}
D;{jmp}
@R15
M=0
(equality{eq_count})
@R15
D=M
"""

def cond_gen(jmp: str):
    def gen():
        global eq_count
        eq_count += 1
        return pop(seg_any(Load.ADDRESS, "R15")) + pop(seg_any(Load.ADDRESS, "R14")) + push(cond_op(jmp))
    return gen

MATH_CMD = {
    "add": math2_gen("D+M"),
    "sub": math2_gen("D-M"),
    "and": math2_gen("D&M"),
    "or": math2_gen("D|M"),
    "not": math1_gen("!M"),
    "neg": math1_gen("-M"),
    "eq": cond_gen("JMP"),
    "gt": cond_gen("JGT"),
    "lt": cond_gen("JLT"),
}

