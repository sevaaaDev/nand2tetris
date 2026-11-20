import tokens
def is_char(c: str) -> bool:
    return c.isalnum() or c == "_"

def is_string(c: str) -> bool:
    return c != '"' and c != "\n" and c != ""

class Lexer():
    def __init__(self, filestr: str):
        self.filestr = filestr
        self.cursor = 0
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
        while (self.hasMoreChar()):
            c: str = self.nextChar()
            # TODO: handle comment // comment /* comment */
            if c == '"':
                while is_string(self.peek()):
                    c = self.nextChar()
                    tok += c
                if self.peek() != '"':
                    raise SyntaxError("missing quotes for string")
                self.nextChar()
                return (tokens.STRING, tok)
            if c == " " or c == '\n':
                continue
            if c in tokens.symbol_map:
                return (tokens.symbol_map[c], c)
            if c.isdigit():
                tok += c
                while self.peek().isdigit():
                    c = self.nextChar()
                    tok += c
                return (tokens.INTEGER, tok)
            if is_char(c):
                tok += c
                while is_char(self.peek()):
                    c = self.nextChar()
                    tok += c
                if tok in tokens.keyword_map:
                    return (tokens.keyword_map[tok], tok)
                return (tokens.IDENTIFIER, tok)
            raise SyntaxError(f"invalid char: {c}")
        return ("EOF", "")
