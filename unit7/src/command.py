from abc import ABC, abstractmethod
from codegen import push, pop, Load, SEGMENT_LOADER, MATH_CMD
from typing import Callable

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

    def __init__(self, data: list[str]) -> None:
        self.segment = data[1]
        self.arg = data[2]

    def to_asm(self, filename: str) -> str:
        return f"// push {self.segment} {self.arg}" + push(SEGMENT_LOADER[self.segment](Load.CONTENT, self.arg, filename))

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" and self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        return

class PopCommand(Command):
    def __init__(self, data: list[str]):
        self.segment = data[1]
        self.arg = data[2]

    def to_asm(self, filename: str) -> str:
        return f"// pop {self.segment} {self.arg}" + pop(SEGMENT_LOADER[self.segment](Load.ADDRESS, self.arg, filename))

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

    def to_asm(self, filename: str) -> str:
        return f"// {self.type}" + MATH_CMD[self.type]()
        # return ArithmeticCommand.TYPE_TO_ASM[self.type]

class IfCommand(Command):
    def __init__(self, data: list[str]):
        self.label = data[1]

    def to_asm(self, filename: str) -> str:
        return f"// if-goto {self.label}"
        pop(R14)
        @R14
        D=M+1
        @{self.label}
        D;JEQ

class LabelCommand(Command):
    def __init__(self, data: list[str]):
        self.label = data[1]

    def to_asm(self, filename: str) -> str:
        return f"// label {self.label}"

class GotoCommand(Command):
    def __init__(self, data: list[str]):
        self.label = data[1]

    def to_asm(self, filename: str) -> str:
        return f"// goto {self.label}"

class FuncCommand(Command):
    def __init__(self, data: list[str]):
        self.name = data[1]
        self.nlocal = data[2]

    def to_asm(self, filename: str) -> str:
        return f"// function {self.name} {self.nlocal}"

class CallCommand(Command):
    def __init__(self, data: list[str]):
        self.name = data[1]
        self.nargs = data[2]

    def to_asm(self, filename: str) -> str:
        return f"// call {self.name} {self.nargs}"

class ReturnCommand(Command):
    def to_asm(self, filename: str) -> str:
        return f"// return"
