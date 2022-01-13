.model small
.stack 100h
.data
buff    db 26
        db ?
        db 26 dup('$')
msgname db"Name - $"
msgtitle db"Program Title - Assignment 1 Problem 1$"
linefeed db 13, 10, "$"
.code
main proc
        MOV AX,@data
        MOV DS,AX

        MOV AH,0AH
        MOV DX, offset buff
        INT 21H
        MOV SI, offset buff + 1
        MOV CL, [ SI ]
        MOV CH, 0
        INC CX
        ADD SI, CX
        MOV AL, '$'
        MOV [ SI ], AL

        MOV AH, 09H
        MOV DX, offset buff + 2
        INT 21H
        MOV AH, 09H
        MOV DX, offset linefeed
        INT 21H

        LEA DX,msgname
        MOV AH,09H
        INT 21H

        MOV AH, 09H
        MOV DX, offset buff + 2
        INT 21H
        MOV AH, 09H
        MOV DX, offset linefeed
        INT 21H

        MOV AH, 09H
        MOV DX, offset linefeed
        INT 21H

        LEA DX,msgtitle
        MOV AH,09H
        INT 21H

        MOV AH,4CH
        INT 21H
main endp
end

