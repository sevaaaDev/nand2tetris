from abc import ABC, abstractmethod

def asm_load_ptr(segment: str, offset: str) -> str:
    match segment:
        case "local":
            var = "LCL"
        case "argument":
            var = "ARG"
        case "this":
            var = "THIS"
        case "that":
            var = "THAT"
    return f"""
@{var}
D=M
@{offset}
A=D+A
"""

class SemanticError(Exception):
    pass

class Command():
    def __init__(self, data: list[str]) -> None:
        pass

    @abstractmethod
    def to_asm(self, filename: str) -> str:
        pass

    def semantic_check(self) -> None:
        return

class PushCommand(Command):
    ASM_PUSH = """
@SP
A=M
M=D
@SP
M=M+1
"""

    def __init__(self, data: list[str]) -> None:
        self.segment = data[1]
        self.arg = data[2]

    def asm_load_ptr_offset(self):
        return f"""
{asm_load_ptr(self.segment, self.arg)}
D=M
"""
    def asm_load_temp(self):
        return f"""
@5
D=A
@{self.arg}
A=D+A
D=M
"""
    def asm_load_constant(self):
        return f"""
@{self.arg}
D=A
"""
    def asm_load_pointer(self):
        return f"""
@{"THIS" if self.arg == "0" else "THAT"}
D=M
"""
    def asm_load_static(self, filename: str):
        return f"""
@{filename}.{self.arg}
D=M
"""
    def to_asm(self, filename: str) -> str:
        match self.segment:
            case "constant":
                load = self.asm_load_constant()
            case "temp":
                load = self.asm_load_temp()
            case "pointer":
                load = self.asm_load_pointer()
            case "static":
                load = self.asm_load_static(filename)
            case _:
                load = self.asm_load_ptr_offset()

        return f"// push {self.segment} {self.arg} {load} {PushCommand.ASM_PUSH}"

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" and self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        return

class PopCommand(Command):
    ASM_POP = """
@SP
M=M-1

A=M
D=M

@R13
A=M
M=D
"""
    def __init__(self, data: list[str]):
        self.segment = data[1]
        self.arg = data[2]

    def asm_ptr(self):
        return f"""
{asm_load_ptr(self.segment, self.arg)}
D=A
@R13
M=D
"""

    def asm_constant(self):
        return f"""
@{self.arg}
D=A

@R13
M=D
"""
    def asm_static(self, filename: str):
        return f"""
@{filename}.{self.arg}
D=A

@R13
M=D
"""
    def asm_pointer(self):
        return f"""
@{"THIS" if self.arg == "0" else "THAT"}
D=A

@R13
M=D
"""
    def asm_temp(self):
        return f"""
@5
D=A
@{self.arg}
D=D+A

@R13
M=D
"""

    def to_asm(self, filename: str) -> str:
        match self.segment:
            case "constant":
                load = self.asm_constant()
            case "temp":
                load = self.asm_temp()
            case "pointer":
                load = self.asm_pointer()
            case "static":
                load = self.asm_static(filename)
            case _:
                load = self.asm_ptr()
        return f"// pop {self.segment} {self.arg} {load} {PopCommand.ASM_POP}"

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" and self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        if self.segment == "constant":
            raise SemanticError("you cant pop into constant")
        return 

def asm_math2(op: str):
    def gen():
        return f"""
@R15
D=A
@R13
M=D

{PopCommand.ASM_POP}

@R14
D=A
@R13
M=D

{PopCommand.ASM_POP}

@R14
D=M
@R15
D={op}

{PushCommand.ASM_PUSH}
"""
    return gen

def asm_math1(op: str):
    def gen():
        return f"""
@R15
D=A
@R13
M=D

{PopCommand.ASM_POP}
@R15
D={op}

{PushCommand.ASM_PUSH}
"""
    return gen

eq_count=0
def asm_math_cond(op: str):
    def gen():
        global eq_count
        eq_count += 1
        return f"""
@R15
D=A
@R13
M=D

{PopCommand.ASM_POP}

@R14
D=A
@R13
M=D

{PopCommand.ASM_POP}

@R14
D=M
@R15
D=D-M
M=-1
@equality{eq_count}
D;{op}
@R15
M=0
(equality{eq_count})
@R15
D=M

{PushCommand.ASM_PUSH}
"""
    return gen

class ArithmeticCommand(Command):
    TYPE_TO_ASM: dict[str, str] = {
        "add": asm_math2("D+M"),
        "sub": asm_math2("D-M"),
        "and": asm_math2("D&M"),
        "or":  asm_math2("D|M"),
        "sub": asm_math2("D-M"),
        "not": asm_math1("!M"),
        "neg": asm_math1("-M"),
        "eq": asm_math_cond("JEQ"),
        "gt": asm_math_cond("JGT"),
        "lt": asm_math_cond("JLT"),
    }
    def __init__(self, data: list[str]):
        self.type = data[0]

    def to_asm(self, filename: str) -> str:
        return f"// {self.type} {ArithmeticCommand.TYPE_TO_ASM[self.type]()}"
        # return ArithmeticCommand.TYPE_TO_ASM[self.type]
