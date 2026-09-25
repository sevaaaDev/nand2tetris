
@i
M=0

(LOOP)
    // if (M[i] > M[R1]) then stop

    @R1
    D=M
    @i
    D=M-D

    // jumpto(END, GE)
    @END
    D;JGE

    // M[R2] += M[R0]
    @R0
    D=M
    @R2
    M=D+M

    @i
    M=M+1

    @LOOP
    0;JMP

(END)
    @END
    0;JMP

