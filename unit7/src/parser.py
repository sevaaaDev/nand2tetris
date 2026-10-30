import tokens
from lexer import ALexer
import command

PUSH_RULES = (command.PushCommand, [tokens.PUSH, tokens.SEGMENT, tokens.DIGIT])
POP_RULES = (command.PopCommand, [tokens.POP, tokens.SEGMENT, tokens.DIGIT])
ARITH_RULES = (command.ArithmeticCommand, [tokens.ARITHMETIC])
FUNC_RULES = (command.FuncCommand, [tokens.FUNC, tokens.IDENT, tokens.DIGIT])
CALL_RULES = (command.CallCommand, [tokens.CALL, tokens.IDENT, tokens.DIGIT])
RETURN_RULES = (command.ReturnCommand, [tokens.RETURN])
IF_RULES = (command.IfCommand, [tokens.IF, tokens.IDENT])
GOTO_RULES = (command.GotoCommand, [tokens.GOTO, tokens.IDENT])
LABEL_RULES = (command.LabelCommand, [tokens.LABEL, tokens.IDENT])

def parse_cmd(lex: ALexer, rules: tuple[type[Command], list[str]]) -> Command:
    data: list[str] = []
    for r in rules[1]:
        tok = lex.peek()
        if tok is None:
            raise SyntaxError(f"expected {r}, got nothing")
        if tok[0] != r:
            raise SyntaxError(f"expected {r}, got '{tok[0]}'")
        lex.eat()
        data.append(tok[1])
    if lex.peek() is not None:
        raise SyntaxError(f"expected newline, got something else")
    return rules[0](data)

# TODO: this only work if lexer loop thru whole file.
def parse_function(lex: ALexer) -> Command:
    func: Command = parse_cmd(lex, FUNC_RULES)
    cmds: list[Command] = []
    while True:
        try:
            cmd = parse(lex)
            cmds.append(cmd)
            if isinstance(cmd, command.ReturnCommand):
                break
        except EOFError:
            break
    func.body = cmds
    return func


def parse(lex: ALexer) -> Command:
    tok = lex.peek()
    if tok is None:
        raise EOFError()
    match tok[0]:
        case tokens.PUSH:
            return parse_cmd(lex, PUSH_RULES)
        case tokens.POP:
            return parse_cmd(lex, POP_RULES)
        case tokens.ARITHMETIC:
            return parse_cmd(lex, ARITH_RULES)
        case tokens.FUNC:
            return parse_function(lex)
        case tokens.CALL:
            return parse_cmd(lex, CALL_RULES)
        case tokens.RETURN:
            return parse_cmd(lex, RETURN_RULES)
        case tokens.IF:
            return parse_cmd(lex, IF_RULES)
        case tokens.GOTO:
            return parse_cmd(lex, GOTO_RULES)
        case tokens.LABEL:
            return parse_cmd(lex, LABEL_RULES)
        case _:
            raise SyntaxError(f"this should not happen: {tok[0]} fail to match any rules")
