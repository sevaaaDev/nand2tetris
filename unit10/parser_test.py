from parser import Parser
from lexer import Lexer

fstr ="""
foo 
""" 
l = Lexer(fstr)
p = Parser(l)
p.jack_expr()

fstr ="""
foo.call() 
""" 
l = Lexer(fstr)
p = Parser(l)
p.jack_expr()

fstr ="""
(5 + 1) * 5 
""" 
l = Lexer(fstr)
p = Parser(l)
p.jack_expr()
