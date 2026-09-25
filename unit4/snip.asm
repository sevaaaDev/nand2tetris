// ifthen
D=D-M // condition
@FI
D;JNE

// body

(FI)

// whileloop
(WHILE)
D=D-M
@WHILE_DONE
D;JNE

// body

@WHILE
0;JMP
(WHILE_DONE)

// forloop :: repeat
@i
M=0
(FOR)
@i
D=M
@end // the end digit
D=D-M
@FOR_DONE
D;JNE

// body

@i
M=M+1
@FOR
0;JMP
(FOR_DONE)
