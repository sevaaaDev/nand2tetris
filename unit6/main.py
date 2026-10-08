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
    "ADM": "111",
    "D": "010",
    "DM": "011",
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
        self.sym = {}

    def get(self, label: str) -> int:
        if label not in self.sym:
            self.sym[label] = self.next_var_addr
            self.next_var_addr += 1
        return self.sym[label]

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
        try:
            addr: int = int(self.sym)
        except:
            addr: int = symbol_table.get(self.sym)
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

def main():
    symbol_table: Symbol_Table = Symbol_Table()
    err: bool = False
    with open(sys.argv[1], 'r') as file:
        commands: list[Command] = []
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '(':
                # addLabel
                continue
            try:
                cmd: Command = parse(line, symbol_table)
                commands.append(cmd)
            except SyntaxError as e:
                print(f"{line_num}: error: " + str(e))
                err = True
        if err:
            return
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
