from lexer import Lexer
import tokens

def test_string():
    assert tokens.STRING == Lexer('"hello world"').lex()[0]

# def test_comment():
#     assert tokens.EOF == Lexer('/* comment out */').lex()[0]
#     assert tokens.EOF == Lexer('// comment out').lex()[0]
#     assert tokens.LET == Lexer('/* comment out */ let').lex()[0]

