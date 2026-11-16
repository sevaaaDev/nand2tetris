import token
def is_char(c: str) -> bool:
    return c.isalnum() or c == "_"

def is_string(c: str) -> bool:
    return c != '"' and c != "\n"

class Lexer():
    def __init__(self, filestr: str):
        self.filestr = filestr
        self.cursor = 0;
        return

    def hasMoreChar(self):
        return len(self.filestr) > self.cursor

    def nextChar(self):
        cur = self.cursor
        self.cursor += 1
        return self.filestr[cur]

    def peek(self) -> str:
        return self.filestr[self.cursor] if self.hasMoreChar() else ""

    def lex(self) -> str:
        tok: str = ""
        # THE char need peeking else gets eaten from the previous consume
        while (self.hasMoreChar()):
            c: str = self.nextChar()
            if c == " ":
                continue
            # BUG: make the string return as token.STRING. ignore quotes
            if c == '"':
                while is_string(self.peek()):
                    c = self.nextChar()
                    tok += c
                return (token.STRING, tok)
            if c in token.symbol_map:
                return (token.symbol_map[c], c)
            if c.isdigit():
                tok += c
                while self.peek().isdigit():
                    c = self.nextChar()
                    tok += c
                return (token.INTEGER, tok)
            if is_char(c):
                tok += c
                while is_char(self.peek()):
                    c = self.nextChar()
                    tok += c
                if tok in token.keyword_map:
                    return (token.keyword_map[tok], tok)
                return (token.IDENTIFIER, tok)





