IDENTIFIER = "IDENTIFIER"
INTEGER = "INTEGER"
STRING = "STRING"
EOF = "EOF"

LEFT_PAREN = "("
RIGHT_PAREN = ")"
LEFT_BRACKET = "["
RIGHT_BRACKET = "]"
LEFT_BRACE = "{"
RIGHT_BRACE = "}"
PLUS = "+"
STAR = "*"
MINUS = "-"
SLASH = "/"
AMPERSAND = "&"
PIPE = "|"
GREATER = ">"
LESS = "<"
EQUAL = "="
NEGATE = "~"
COMMA = ","
SEMICOLON = ";"
DOT = "."
DOUBLE_QUOTE = '"'

symbol_map = {
    "(": LEFT_PAREN,
    ")": RIGHT_PAREN,
    "[": LEFT_BRACKET,
    "]": RIGHT_BRACKET,
    "{": LEFT_BRACE,
    "}": RIGHT_BRACE,
    "+": PLUS,
    "*": STAR,
    "-": MINUS,
    "/": SLASH,
    "&": AMPERSAND,
    "|": PIPE,
    ">": GREATER,
    "<": LESS,
    "=": EQUAL,
    "~": NEGATE,
    ",": COMMA,
    ";": SEMICOLON,
    ".": DOT,
    '"': DOUBLE_QUOTE,
}

IF = "if"
ELSE = "else"
WHILE = "while"
RETURN = "return"
LET = "let"
DO = "do"
VAR = "var"
FIELD = "field"
STATIC = "static"
CLASS = "class"
METHOD = "method"
FUNCTION = "function"
CONSTRUCTOR = "constructor"
INT = "int"
CHAR = "char"
BOOLEAN = "boolean"
THIS = "this"
TRUE = "true"
FALSE = "false"
NULL = "null"
VOID = "void"

keyword_map = {
    "if": IF,
    "else": ELSE,
    "while": WHILE,
    "return": RETURN,
    "let": LET,
    "do": DO,
    "var": VAR,
    "field": FIELD,
    "static": STATIC,
    "class": CLASS,
    "method": METHOD,
    "function": FUNCTION,
    "constructor": CONSTRUCTOR,
    "int": INT,
    "char": CHAR,
    "boolean": BOOLEAN,
    "this": THIS,
    "true": TRUE,
    "false": FALSE,
    "void": VOID,
    "null": NULL,
}

