# we can set addr symbol to unresolved
# then after finish parsing, we traverse the ast and resolve the symbol

# command is class
# method eval()

import sys
from abc import ABC, abstractmethod

DEST_TO_BIN = {
    "": "000",
    "A": "100",
    "AD": "110",
    "AM": "101",
    "ADM": "111",
    "D": "010",
    "MD": "011",
    "M": "001",
}
JUMP_TO_BIN = {
    "": "000",
    "JLT": "100",
    "JEQ": "010",
    "JGT": "001",
    "JLE": "110",
    "JGE": "011",
    "JMP": "111",
    "JNE": "101",
}

COMP_TO_BIN = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "M": "1110000",
    "A": "0110000",
    "!D": "0001101",
    "!M": "1110001",
    "!A": "0110001",
    "-D": "0001111",
    "-M": "1110011",
    "-A": "0110011",
    "D+1": "0011111",
    "M+1": "1110111",
    "A+1": "0110111",
    "D-1": "0001110",
    "M-1": "1110010",
    "A-1": "0110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

class Symbol_Table():
    def __init__(self):
        self.next_var_addr = 16
        self.sym = {
            "R0": 0,
            "R1": 1,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
        }

    def get(self, label: str) -> int:
        if label not in self.sym:
            self.sym[label] = self.next_var_addr
            self.next_var_addr += 1
        return self.sym[label]

    def set(self, label: str, val: int) -> None:
        self.sym[label] = val

class Token(ABC):
    def __init__(self, val:str):
        self.val = val

class DestToken(Token):
    pass

class JumpToken(Token):
    pass

class CompToken(Token):
    pass

class AddrToken(Token):
    pass

class Command(ABC):
    @abstractmethod
    def toBinary(self, symbol_table: Symbol_Table) -> str:
        pass

class AddrCmd(Command):
    def __init__(self, sym: str):
        self.sym = sym

    def toBinary(self, symbol_table: Symbol_Table) -> str:
        addr: int
        try:
            addr = int(self.sym)
        except:
            addr = symbol_table.get(self.sym)
        return '0' + bin(addr & 0xFFFF)[2:].rjust(15, "0")

class CompCmd(Command):
    def __init__(self, dest: str, comp: str, jump: str):
        self.dest = dest
        self.comp = comp
        self.jump = jump

    def toBinary(self, symbol_table: Symbol_Table) -> str:
        return '111' + COMP_TO_BIN[self.comp] + DEST_TO_BIN[self.dest] + JUMP_TO_BIN[self.jump]

class Lexer():
    def __init__(self, line):
        self.line = line
        self.tok = None

    def lex(self) -> Token | None:
        if len(self.line) == 0:
            return None
        if self.line[0] == "@":
            val = self.line[1:]
            self.line = ""
            return AddrToken(val)
        if "=" in self.line:
            val, self.line = self.line.split("=", 1)
            return DestToken(val)
        if ";" in self.line:
            self.line, val = self.line.split(";", 1)
            return JumpToken(val)
        return CompToken(self.line)

    def peek(self) -> Token | None:
        if self.tok is None:
            self.tok = self.lex()
        return self.tok

    def eat(self) -> None:
        self.tok = None


def parseComp(line: str) -> Command:
    dest = DestToken("")
    jump = JumpToken("")
    comp: CompToken
    lexer = Lexer(line)
    # [Comp]
    tok = lexer.peek()
    if isinstance(tok, DestToken):
        lexer.eat()
        if tok.val not in DEST_TO_BIN:
            raise SyntaxError(f"invalid destination: {tok.val}")
        dest = tok
    tok = lexer.peek()
    if isinstance(tok, JumpToken):
        lexer.eat()
        if tok.val not in JUMP_TO_BIN:
            raise SyntaxError(f"invalid jump: {tok.val}")
        jump = tok
    tok = lexer.peek()
    if isinstance(tok, CompToken):
        lexer.eat()
        if tok.val not in COMP_TO_BIN:
            raise SyntaxError(f"invalid computation: {tok.val}")
        comp = tok
    else:
        raise SyntaxError("missing computation")

    return CompCmd(dest.val, comp.val, jump.val)

def parseAddr(line: str) -> Command | None:
    tok = Lexer(line).peek()
    return AddrCmd(tok.val) if isinstance(tok, AddrToken) else None

def parse(line: str, symbol_table: dict[str, int]) -> Command:
    cmd = parseAddr(line)
    return cmd if cmd is not None else parseComp(line)

def parseLabel(line: str) -> str:
    splitted = line[1:].split(')', 1)
    if len(splitted) == 1:
        raise SyntaxError(f"invalid label '{line}'")
    label, rest = splitted
    if len(rest) != 0:
        raise SyntaxError(f"invalid label '{line}'")
    return label

def main():
    symbol_table: Symbol_Table = Symbol_Table()
    err: bool = False
    with open(sys.argv[1], 'r') as file:
        commands: list[Command] = []
        line_num: int = 1
        for line in file:
            line = line.strip()
            if len(line) == 0 or line[0:2] == "//":
                continue
            try:
                if line[0] == '(':
                    label = parseLabel(line)
                    symbol_table.set(label, line_num-1)
                    continue
                cmd: Command = parse(line, symbol_table)
                commands.append(cmd)
            except SyntaxError as e:
                print(f"{line_num}: error: " + str(e))
                return
            line_num += 1
        for cmd in commands:
            print(cmd.toBinary(symbol_table))

def test():
    line = "@addr"
    lex = Lexer(line)
    tok = lex.peek()
    assert isinstance(tok, AddrToken)

    line = "ADM=D+A;JMP"
    lex = Lexer(line)
    tok = lex.peek()
    assert isinstance(tok, DestToken)
    lex.eat()
    tok = lex.peek()
    assert isinstance(tok, JumpToken)
    lex.eat()
    tok = lex.peek()
    assert isinstance(tok, CompToken)

    cmd = parseComp(line)
    print(cmd.dest.val)
    print(cmd.comp.val)
    print(cmd.jump.val)

    line = "D;JGT"
    cmd = parseComp(line)
    print(cmd.dest.val)
    print(cmd.comp.val)
    print(cmd.jump.val)

    line = "D=A"
    cmd = parseComp(line)
    print(cmd.dest.val)
    print(cmd.comp.val)
    print(cmd.jump.val)

           
if __name__ == "__main__":
    main()
