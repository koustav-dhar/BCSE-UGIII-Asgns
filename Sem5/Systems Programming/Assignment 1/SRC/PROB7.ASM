.model small
.stack 100h
.data
mes1 db 0ah,0dh,"Enter 1st number:$"
mes2 db 0ah,0dh,"Enter 2nd number:$"
mes3 db 0ah,0dh,"First number is greater than second number$"
mes4 db 0ah,0dh,"Second number is greater than first number$"
mes5 db 0ah,0dh,"The two numbers are equal$"
.code
main proc
	MOV AX,@data
	MOV DS,AX
	LEA DX,mes1
	MOV AH,09H
	INT 21H
	CALL getNum
	MOV BX,AX
	LEA DX,mes2
	MOV AH,09H
	INT 21H
	CALL getNum
	CMP BX,AX
	JG cond1
	JL cond2
	LEA DX,mes5
	MOV AH,09H
	INT 21H
	JMP exit
	cond1:
		LEA DX,mes3
		MOV AH,09H
		INT 21H
		JMP exit
	cond2:
		LEA DX,mes4
		MOV AH,09H
		INT 21H
	exit:
	MOV AH,4CH
	INT 21H
main endp

;function to take 16 bit hexadecimal number input
getNum proc
    PUSH CX
    PUSH DX

    MOV DX,0000
    MOV AX,0000
    MOV CL,4

    getNumber:
        CALL getChar
        CMP AL,13
        JE inputDone
        CMP AL,10
        JE inputDone

        SHL DX,CL ;left shifting 4 bits
        SUB AL,48 ;finding the numerical value from character
        CMP AL,9
        JLE isNumber   ;check if 0-9 or A-F
        SUB AL,7  ;for A-F

        isNumber:
           OR DL,AL
           JMP getNumber

    inputDone:
        MOV AX,DX
    POP DX
    POP CX
    RET
getNum endp

;function to input character
getChar proc
    MOV AH,01H
    INT 21H
    RET
getChar endp

end
