import tokens

class Lexer():
    def __init__(self):
        self.tok = None

    def lex(self) -> Token | None:
        pass

    def peek(self) -> Token | None:
        if self.tok is None:
            self.tok = self.lex()
        return self.tok

    def eat(self) -> Token:
        tok = self.tok
        self.tok = None
        return tok

class MOCK_Lexer(Lexer):
    def __init__(self, tokens):
        super().__init__()
        self.tokens = tokens

    def lex(self) -> Token:
        return self.tokens.pop(0)
