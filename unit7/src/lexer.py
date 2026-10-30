from tokens import Token
import tokens
from abc import ABC, abstractmethod

class ALexer(ABC):
    def __init__(self) -> None:
        self.tok: Token | None = None

    def lex(self) -> Token | None:
        pass

    def peek(self) -> Token | None:
        if self.tok is None:
            self.tok = self.lex()
        return self.tok

    def eat(self) -> Token | None:
        self.peek()
        tok = self.tok
        self.tok = None
        return tok

class MOCK_Lexer(ALexer):
    def __init__(self, tokens: list[Token]) -> None:
        super().__init__()
        self.tokens = tokens

    def lex(self) -> Token | None:
        return self.tokens.pop(0) if len(self.tokens) != 0 else None

class Scanner:
    def __init__(self, filestr: str):
        self.content = filestr

    def nextLine(self) -> str:
        line = ""
        while len(line) == 0:
            if len(self.content) == 0:
                return ""
            splitted: tuple[str, str] | list[str] = (self.content, "")
            if "\n" in self.content:
                splitted = self.content.split("\n", 1)
            line, self.content = splitted
            if "//" in line:
                line, _ = line.split("//", 1)
            line = line.strip()

        return line

class Lexer(ALexer):
    SEGMENT = ["local" , "argument" , "this" , "that" , "static" , "constant" , "temp" , "pointer"]
    MATH = ["add" , "sub" , "neg" , "eq" , "gt" , "lt" , "or" , "and" , "not"]
    def __init__(self, f: Scanner):
        super().__init__()
        self.f = f
        self._linenum = 0
        self._CURRENT_LINE = ""
        self.line = ""
        self.advanceLine()

    @property
    def current_line(self):
        return self._CURRENT_LINE

    @property
    def linenum(self):
        return self._linenum

    def advanceLine(self):
        self._CURRENT_LINE = self.f.nextLine()
        self.line = self._CURRENT_LINE
        self._linenum+=1

    def lex(self) -> Token | None:
        if len(self.line) == 0:
            self.advanceLine()
            return None
        splitted: tuple[str, str] | list[str] = (self.line, "")
        if " " in self.line:
            splitted = self.line.split(" ", 1)
        word, self.line = splitted
        match word:
            case w if w.isdigit():
                return (tokens.DIGIT, word) 
            case w if w in Lexer.SEGMENT:
                return (tokens.SEGMENT, word) 
            case "push":
                return (tokens.PUSH, word) 
            case "pop":
                return (tokens.POP, word)
            case w if w in Lexer.MATH:
                return (tokens.ARITHMETIC, word)
            case "function":
                return (tokens.FUNC, word)
            case "call":
                return (tokens.CALL, word)
            case "return":
                return (tokens.RETURN, word)
            case "if-goto":
                return (tokens.IF, word)
            case "goto":
                return (tokens.GOTO, word)
            case "label":
                return (tokens.LABEL, word)
            case _:
                return (tokens.IDENT, word)
