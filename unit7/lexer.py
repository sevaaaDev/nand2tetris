from tokens import Token
import tokens
from abc import ABC, abstractmethod

class Lexer(ABC):
    def __init__(self) -> None:
        self.tok: Token | None = None

    @abstractmethod
    def lex(self) -> Token | None:
        pass

    def peek(self) -> Token | None:
        if self.tok is None:
            self.tok = self.lex()
        return self.tok

    def eat(self) -> Token | None:
        tok = self.tok
        self.tok = None
        return tok

class MOCK_Lexer(Lexer):
    def __init__(self, tokens: list[Token]) -> None:
        super().__init__()
        self.tokens = tokens

    def lex(self) -> Token | None:
        return self.tokens.pop(0)
