.model small
.stack 100h
.data
.code
main proc
           MOV CX,26
           MOV DL,'A'
           whileloop:
               MOV AH,02H
               INT 21H
               INC DL
           loop whileloop
           MOV AH,4CH
           INT 21H
main endp
end
