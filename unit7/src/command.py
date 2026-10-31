from abc import ABC, abstractmethod
from codegen import push, pop, Load, SEGMENT_LOADER, MATH_CMD, seg_any, seg_constant, seg_local
from typing import Callable, TextIO

class Counter:
    def __init__(self):
        self.i = 0

    def inc(self) -> int:
        i = self.i
        self.i+=1
        return i

    def reset(self):
        self.i = 0

G_Counter = Counter()

class SemanticError(Exception):
    pass

class Command():
    def __init__(self, data: list[str]) -> None:
        pass

    @abstractmethod
    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        pass

    def semantic_check(self) -> None:
        return

class PushCommand(Command):

    def __init__(self, data: list[str]) -> None:
        self.segment = data[1]
        self.arg = data[2]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"// push {self.segment} {self.arg}" + push(SEGMENT_LOADER[self.segment](Load.CONTENT, self.arg, filename)))

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" and self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        return

class PopCommand(Command):
    def __init__(self, data: list[str]):
        self.segment = data[1]
        self.arg = data[2]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"// pop {self.segment} {self.arg}" + pop(SEGMENT_LOADER[self.segment](Load.ADDRESS, self.arg, filename)))

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" and self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        if self.segment == "constant":
            raise SemanticError("you cant pop into constant")
        return 

class ArithmeticCommand(Command):
    def __init__(self, data: list[str]):
        self.type = data[0]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"// {self.type}" + MATH_CMD[self.type]())

class IfCommand(Command):
    def __init__(self, data: list[str]):
        self.label = data[1]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"// if-goto {self.label}"
        + pop(seg_any(Load.ADDRESS, "R14"))
        + f"""@R14
D=M
@{funcname}${self.label}
D;JNE
""")

class LabelCommand(Command):
    def __init__(self, data: list[str]):
        self.label = data[1]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"""// label {self.label}
({funcname}${self.label})
""")

class GotoCommand(Command):
    def __init__(self, data: list[str]):
        self.label = data[1]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"""// goto {self.label}
@{funcname}${self.label}
0;JMP
""")

class FuncCommand(Command):
    def __init__(self, data: list[str]):
        self.name = data[1]
        self.nlocal = data[2]
        self.body: list[Command] = []

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"""// function {self.name} {self.nlocal}
({self.name})
{"\n".join([push(seg_constant(Load.CONTENT, "0")) for i in range(int(self.nlocal))])}
""")
        for c in self.body:
            c.to_asm(filename, self.name, o)
        G_Counter.reset()

class CallCommand(Command):
    def __init__(self, data: list[str]):
        self.name = data[1]
        self.nargs = data[2]

    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        i = G_Counter.inc()
        o.write(f"// call {self.name} {self.nargs}"
        + push(seg_any(Load.ADDRESS, f"{funcname}$ret.{str(i)}"))
        + push(seg_any(Load.CONTENT, "LCL"))
        + push(seg_any(Load.CONTENT, "ARG"))
        + push(seg_any(Load.CONTENT, "THIS"))
        + push(seg_any(Load.CONTENT, "THAT"))
        + f"""@SP
D=M
@5
D=D-A
@{self.nargs}
D=D-A

@ARG
M=D

@SP
D=M

@LCL
M=D

@{self.name}
0;JMP
({funcname}$ret.{str(i)})
"""
        )
        # push *LCL
        # push *ARG
        # push *THIS
        # push *THAT
        # *ARG = *SP - 5 - nargs
        # *LCL = *SP
        # goto functionname
        # (func$ret.i)

class ReturnCommand(Command):
    def to_asm(self, filename: str, funcname: str, o: TextIO) -> None:
        o.write(f"""// return
@LCL
D=M
@5
A=D-A
D=M

@R15
M=D
"""
        + pop(seg_any(Load.CONTENT, "ARG"))
        + """
@ARG
D=M+1
@SP
M=D

@LCL
D=M
@1
A=D-A
D=M

@THAT
M=D

@LCL
D=M
@2
A=D-A
D=M

@THIS
M=D

@LCL
D=M
@3
A=D-A
D=M

@ARG
M=D

@LCL
D=M
@4
A=D-A
D=M

@LCL
M=D

@R15
A=M
0;JMP
""")
        # endframe = LCL
        # retaddr = *(endframe - 5)
        # *ARG = pop()
        # *SP = *ARG + 1
        # *THAT = *(endframe - 1)
        # *THIS = *(endframe - 2)
        # *ARG = *(endframe - 3)
        # *LCL = *(endframe - 4)
        # goto retaddr
