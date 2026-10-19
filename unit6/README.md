# HACK Assembler
```
python main.py file.asm > file.hack
```

## Summary of the Assembler
the symbolic syntax of the HACK machine language add variable and label abstraction.
the assembler handle label mapping

## Macro
memory handling
```
D=M[i] // i can be label or int
// same as
@i
D=M

M[i]=D
// same as
@i
M=D
```

jump handling
```
comp;JMP label // comp is any computation
// same as
@label
comp;JMP // JMP can be any jump variant
```
