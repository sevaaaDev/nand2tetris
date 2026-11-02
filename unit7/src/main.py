import tokens
import sys
from pathlib import Path
from parser import parse
from lexer import Lexer, Scanner
from command import SemanticError
from typing import TextIO
import argparse

def error(msg: str, filename: str, linenum: int, line: str):
    print(f"{filename}:{linenum}: {msg}", file=sys.stderr)
    print(f"in expression:", file=sys.stderr)
    print(f"\t{line}", file=sys.stderr)

def translate(filename: str, output: TextIO):
    cmds = []
    err = False
    linenum = 0
    with open(filename) as f:
        filestr = f.read()
        lexer = Lexer(Scanner(filestr))
        while True:
            try:
                cmd = parse(lexer)
                cmd.semantic_check()
                cmds.append(cmd)
            except EOFError as e:
                break
            except SyntaxError as e:
                error(f"syntax error: {str(e)}", filename, lexer.linenum, lexer.current_line)
                err = True
            except SemanticError as e:
                error(f"semantic error: {str(e)}", filename, lexer.linenum, lexer.current_line)
                err = True
    if err:
        sys.exit(1)
    for c in cmds:
        c.to_asm(Path(filename).stem, "", output)

def write_init(o: TextIO):
    o.write(""" // Bootstrap
@256
D=A
@SP
M=D

@Sys.init
0;JMP
""")
    
def main() -> None:
    parse = argparse.ArgumentParser()
    parse.add_argument('files', nargs='+')
    parse.add_argument('-o', '--output', default='out.asm')
    args = parse.parse_args()

    files = args.files
    outfile = args.output
    # TODO: handle multi file
    # main.py file1 file2 file3 -o out.asm
    with open(outfile, mode="w") as o:
        write_init(o)
        for filename in files:
            translate(filename, o)

main()
