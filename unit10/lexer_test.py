from lexer import Lexer
import token

def test_string():
    lex = Lexer('"string insdide"')
    assert lex.lex()[0] == token.STRING

def test_again():
    lex = Lexer('if (x = "hello") { return 1; }')
    tok = lex.lex()
    while tok is not None:
        print(tok)
        tok = lex.lex()

def test_newline():
    lex = Lexer("""
if (x = 10) {
    return 1;
}""")
    tok = lex.lex()
    while tok is not None:
        print(tok)
        tok = lex.lex()


test_string()
print("test_again()")
test_again()
print("test_newline()")
test_newline()
