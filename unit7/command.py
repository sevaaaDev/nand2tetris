from abc import ABC, abstractmethod
class SemanticError(Exception):
    pass

class Command():
    def __init__(self, data: list[str]) -> None:
        pass

    @abstractmethod
    def to_asm(self) -> str:
        pass

    def semantic_check(self) -> None:
        return

class PushCommand(Command):
    ASM_PUSH = """@SP
A=M
M=D
@SP
M=M+1
"""
    def __init__(self, data: list[str]) -> None:
        self.segment = data[1]
        self.arg = data[2]

    def to_asm(self) -> str:
        return f"// push {self.segment} {self.arg}"

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" or self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        return

class PopCommand(Command):
    ASM_POP = """"""
    def __init__(self, data: list[str]):
        self.segment = data[1]
        self.arg = data[2]

    def to_asm(self) -> str:
        return f"// pop {self.segment} {self.arg}"

    def semantic_check(self) -> None:
        if self.segment == "pointer":
            if self.arg != "0" or self.arg != "1":
                raise SemanticError(f"pointer must be 1 or 0, cant be '{self.arg}'")
        if self.segment == "constant":
            raise SemanticError("you cant pop into constant")
        return 

class ArithmeticCommand(Command):
    TYPE_TO_ASM: dict[str, str] = {}
    def __init__(self, data: list[str]):
        self.type = data[0]

    def to_asm(self) -> str:
        return f"// {self.type}"
        # return ArithmeticCommand.TYPE_TO_ASM[self.type]
