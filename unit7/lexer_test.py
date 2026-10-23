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

def test_lexer_invalid_input():
    """Lex a error line"""
    line = "push ahseah 7"
    lex = Lexer(line)
    assert lex.eat() == (tokens.PUSH, "push")
    with pytest.raises(SyntaxError):
        lex.eat()

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
