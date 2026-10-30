from pathlib import Path
import pytest
from lexer import Lexer, Scanner
import tokens

def test_lexer_normal_input():
    """Lex a non error line"""
    line = "push constant 7"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() == (tokens.SEGMENT, "constant")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None

def test_lexer_zero_input():
    """Lex a empty string"""
    line = ""
    lex = Lexer(Scanner(line))
    assert lex.eat() is None
    
def test_lexer_one_word():
    """Lex a single word"""
    line = "push"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() is None

def test_lexer_function():
    line = "function Foo.bar 3"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.FUNC, "function")
    assert lex.eat() == (tokens.IDENT, "Foo.bar")
    assert lex.eat() == (tokens.DIGIT, "3")
    assert lex.eat() is None

def test_lexer_call():
    line = "call Foo.bar"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.CALL, "call")
    assert lex.eat() == (tokens.IDENT, "Foo.bar")
    assert lex.eat() is None

def test_lexer_if_goto():
    line = "if-goto goodlabel"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.IF, "if-goto")
    assert lex.eat() == (tokens.IDENT, "goodlabel")
    assert lex.eat() is None

def test_lexer_label():
    line = "label goodlabel"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.LABEL, "label")
    assert lex.eat() == (tokens.IDENT, "goodlabel")
    assert lex.eat() is None

def test_lexer_goto():
    line = "goto goodlabel"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.GOTO, "goto")
    assert lex.eat() == (tokens.IDENT, "goodlabel")
    assert lex.eat() is None

def test_lexer_push():
    line = "push constant 7"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() == (tokens.SEGMENT, "constant")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None

def test_lexer_pop():
    line = "pop local 7"
    lex = Lexer(Scanner(line))
    assert lex.eat() == (tokens.POP, "pop")
    assert lex.eat() == (tokens.SEGMENT, "local")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None

def test_lexer_file():
    filestring = "pop local 7 \npush constant 17\n"
    lex = Lexer(Scanner(filestring))
    assert lex.eat() == (tokens.POP, "pop")
    assert lex.eat() == (tokens.SEGMENT, "local")
    assert lex.eat() == (tokens.DIGIT, "7")
    assert lex.eat() is None

    assert lex.eat() == (tokens.PUSH, "push")
    assert lex.eat() == (tokens.SEGMENT, "constant")
    assert lex.eat() == (tokens.DIGIT, "17")
    assert lex.eat() is None
    
def test_lexer_comment():
    filestring = "// this should be ignored"
    lex = Lexer(Scanner(filestring))
    assert lex.eat() is None

def test_lexer_real_file():
    test_dir = Path(__file__).parent
    file_path = test_dir / 'testfile.vm'
    with open(file_path) as f:
        filestring = f.read()
        lex = Lexer(Scanner(filestring))
        assert lex.eat() == (tokens.PUSH, "push")
        assert lex.eat() == (tokens.SEGMENT, "constant")
        assert lex.eat() == (tokens.DIGIT, "17")
        assert lex.eat() is None

        assert lex.eat() == (tokens.POP, "pop")
        assert lex.eat() == (tokens.SEGMENT, "local")
        assert lex.eat() == (tokens.DIGIT, "1")
        assert lex.eat() is None
        assert lex.eat() == (tokens.ARITHMETIC, "add")
        assert lex.eat() is None
