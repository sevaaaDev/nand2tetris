import pytest
from lexer import Lexer
import tokens

def test_lexer_normal_input():
    """Lex a non error line"""
    line = "push constant 7"
    lex = Lexer(line)
    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() == (tokens.SEGMENT, "constant")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None

def test_lexer_zero_input():
    """Lex a empty string"""
    line = ""
    lex = Lexer(line)
    assert lex.eat() is None
    
def test_lexer_one_word():
    """Lex a single word"""
    line = "push"
    lex = Lexer(line)
    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() is None

def test_lexer_function():
    line = "function Foo.bar 3"
    lex = Lexer(line)
    assert lex.eat() == (tokens.FUNC, "function")
    assert lex.eat() == (tokens.IDENT, "Foo.bar")
    assert lex.eat() == (tokens.DIGIT, "3")
    assert lex.eat() is None

def test_lexer_call():
    line = "call Foo.bar"
    lex = Lexer(line)
    assert lex.eat() == (tokens.CALL, "call")
    assert lex.eat() == (tokens.IDENT, "Foo.bar")
    assert lex.eat() is None

def test_lexer_if_goto():
    line = "if-goto goodlabel"
    lex = Lexer(line)
    assert lex.eat() == (tokens.IF, "if-goto")
    assert lex.eat() == (tokens.IDENT, "goodlabel")
    assert lex.eat() is None

def test_lexer_label():
    line = "label goodlabel"
    lex = Lexer(line)
    assert lex.eat() == (tokens.LABEL, "label")
    assert lex.eat() == (tokens.IDENT, "goodlabel")
    assert lex.eat() is None

def test_lexer_goto():
    line = "goto goodlabel"
    lex = Lexer(line)
    assert lex.eat() == (tokens.GOTO, "goto")
    assert lex.eat() == (tokens.IDENT, "goodlabel")
    assert lex.eat() is None

def test_lexer_push():
    line = "push constant 7"
    lex = Lexer(line)
    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() == (tokens.SEGMENT, "constant")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None

def test_lexer_pop():
    line = "pop local 7"
    lex = Lexer(line)
    assert lex.eat() == (tokens.POP, "pop")
    assert lex.eat() == (tokens.SEGMENT, "local")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None
