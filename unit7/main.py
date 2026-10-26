import tokens
import sys
from pathlib import Path
from parser import parse
from lexer import Lexer
from command import SemanticError

# TODO: test parser
# TODO: implement to_asm()

def translate(filename: str):
    cmds = []
    err = False
    linenum = 0
    with open(filename) as f:
        for line in f:
            linenum+=1
            if "//" in line:
                line, _ = line.split("//", 1)
            line = line.strip()
            if len(line) == 0:
                continue
            lexer = Lexer(line)
            try:
                cmd = parse(lexer)
                cmd.semantic_check()
                cmds.append(cmd)
            except SyntaxError as e:
                print(f"{filename}:{linenum}: syntax error: {str(e)}", file=sys.stderr)
                print(f"\t{line}", file=sys.stderr)
                err = True
            except SemanticError as e:
                print(f"{filename}:{linenum}: semantic error: {str(e)}", file=sys.stderr)
                print(f"\t{line}", file=sys.stderr)
                err = True
    if err:
        sys.exit(1)
    for c in cmds:
        print(c.to_asm(Path(filename).stem))
    
def main() -> None:
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: missing filename", file=sys.stderr)
        print(f"Example:", file=sys.stderr)
        print(f"\tpython {sys.argv[0]} filename.vm", file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    translate(filename)

main()
