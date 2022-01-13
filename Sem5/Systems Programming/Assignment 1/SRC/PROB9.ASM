.model small
.stack 100h
.data
thumbnail db 13,10,"Enter q to exit, anything else to continue.",13,10,"$"
continue db 13,10,"Continuing...$"
.code
main proc
      MOV AX,@data
      MOV DS,AX

      infloop:
           MOV DX, offset continue
           MOV AH,09H
           INT 21H

           MOV DX, offset thumbnail
           MOV AH,09H
           INT 21H

           MOV AH,01H
           INT 21H
           CMP AL,'q'
       JNE infloop
       MOV AH,4CH
       INT 21H
main endp
end
