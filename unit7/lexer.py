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

class Lexer(ALexer):
    SEGMENT = ["local" , "argument" , "this" , "that" , "static" , "constant" , "temp" , "pointer"]
    MATH = ["add" , "sub" , "neg" , "eq" , "gt" , "lt" , "or" , "and" , "not"]
    def __init__(self, line: str):
        super().__init__()
        self.line = line

    def lex(self) -> Token | None:
        if len(self.line) == 0:
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
            case _:
                raise SyntaxError(f"invalid syntax: {word}")
