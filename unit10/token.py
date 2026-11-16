IDENTIFIER = "IDENTIFIER"
INTEGER = "INTEGER"
STRING = "STRING"

LEFT_PAREN = "LEFT_PAREN"
RIGHT_PAREN = "RIGHT_PAREN"
LEFT_BRACKET = "LEFT_BRACKET"
RIGHT_BRACKET = "RIGHT_BRACKET"
LEFT_BRACE = "LEFT_BRACE"
RIGHT_BRACE = "RIGHT_BRACE"
PLUS = "PLUS"
STAR = "STAR"
MINUS = "MINUS"
SLASH = "SLASH"
AMPERSAND = "AMPERSAND"
PIPE = "PIPE"
GREATER = "GREATER"
LESS = "LESS"
EQUAL = "EQUAL"
NEGATE = "NEGATE"
COMMA = "COMMA"
SEMICOLON = "SEMICOLON"
DOT = "DOT"
DOUBLE_QUOTE = "DOUBLE_QUOTE"

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

IF = "IF"
ELSE = "ELSE"
WHILE = "WHILE"
RETURN = "RETURN"
LET = "LET"
DO = "DO"
VAR = "VAR"
FIELD = "FIELD"
STATIC = "STATIC"
CLASS = "CLASS"
METHOD = "METHOD"
FUNCTION = "FUNCTION"
CONSTRUCTOR = "CONSTRUCTOR"
INT = "INT"
CHAR = "CHAR"
BOOLEAN = "BOOLEAN"
THIS = "THIS"
TRUE = "TRUE"
FALSE = "FALSE"
NULL = "NULL"
VOID = "VOID"

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

