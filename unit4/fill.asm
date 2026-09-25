// while true do
//     while true do
//         key = read()
//         cmd = 0
//         if key != 0 then cmd = -1
//         setScreen(cmd)
//     done
// done


@MAIN
0;JMP

(SETSCREEN)
@i
M=0

(LOOP_SETSCREEN)
@i
D=M
@SCREEN
D=D+A

@KBD
D=D-A
@LOOP_END_SETSCREEN
D;JEQ

@i
D=M
@SCREEN
D=D+A
@cur
M=D

@KBD
D=M
@IF_CLEAR
D;JEQ // if jump, that mean D == 0
D=-1 // we set D = -1 when not jumping
(IF_CLEAR)
@cur
A=M
M=D // here D default to 0 if jumped
// cool trick huh?

@i
M=M+1
@LOOP_SETSCREEN
0;JMP
(LOOP_END_SETSCREEN)
@return
A=M
0;JMP

(MAIN)
// setScreen()
@MAIN
D=A
@return
M=D

@SETSCREEN
0;JMP
// ===

