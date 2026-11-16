from lexer import Lexer
import token

def test_basic():
    lex = Lexer("if (true) {}")
    assert lex.lex()[0] == token.IF
    assert lex.lex()[0] == token.LEFT_PAREN
    assert lex.lex()[0] == token.TRUE
    assert lex.lex()[0] == token.RIGHT_PAREN
    assert lex.lex()[0] == token.LEFT_BRACE
    assert lex.lex()[0] == token.RIGHT_BRACE

def test_complex():
    lex = Lexer("{let foo = 100}")
    assert lex.lex()[0] == token.LEFT_BRACE
    assert lex.lex()[0] == token.LET
    assert lex.lex()[0] == token.IDENTIFIER
    assert lex.lex()[0] == token.EQUAL
    assert lex.lex()[0] == token.INTEGER
    assert lex.lex()[0] == token.RIGHT_BRACE

def test_string():
    lex = Lexer('"string insdide"')
    assert lex.lex()[0] == token.STRING
    lex = Lexer('"string insdide')
    assert lex.lex()[0] == token.STRING



test_basic()
test_complex()
test_string()
