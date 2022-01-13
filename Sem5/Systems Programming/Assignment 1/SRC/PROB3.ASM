.model small
.stack 100h
.data
inputPrompt db 13,"Enter a 16 bit hexadecimal number: $"
num1 dw ?
num2 dw ?
num dw ?
sum dw ?
sumCarry dw 00h
sumPrompt db 10,"The sum is: $"
.code
MOV AX,@data
MOV DS,AX
CALL main
MOV AH,4CH
INT 21H

main proc
    ;input first number
    LEA DX,inputPrompt
    MOV AH,09H
    INT 21H
    CALL getNum
    MOV num1,AX

    ;input second number
    LEA DX,inputPrompt
    MOV AH,09H
    INT 21H
    CALL getNum
    MOV num2,AX

    ;add them
    MOV AX,num1
    ADD AX,num2
    JNC noCarry
    INC sumCarry
    noCarry:
       MOV sum,AX

    ;output sum
    LEA DX,sumPrompt
    MOV AH,09H
    INT 21H
    MOV AX,sumCarry
    MOV num,AX
    CALL outputNum
    MOV AX,sum
    MOV num,AX
    CALL outputNum

    RET
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

;function to output 16-bit hexadecimal number stored in decimal format
outputNum proc
    PUSH CX
    PUSH DX

    MOV CL,4
    MOV DX,num
    MOV DL,DH
    SHR DL,CL
    AND DL,0FH
    CMP DL,0AH
    JL isNumber4
    ADD DL,7
    isNumber4:
        ADD DL,48
    MOV AH,02H
    INT 21H

    MOV DX,num
    MOV DL,DH
    AND DL,0FH
    CMP DL,0AH
    JL isNumber3
    ADD DL,7
    isNumber3:
        ADD DL,48
    MOV AH,02H
    INT 21H

    MOV CL,4
    MOV DX,num
    SHR DL,CL
    AND DL,0FH
    CMP DL,0AH
    JL isNumber2
    ADD DL,7
    isNumber2:
        ADD DL,48
    MOV AH,02H
    INT 21H

    MOV DX,num
    AND DL,0FH
    CMP DL,0AH
    JL isNumber1
    ADD DL,7
    isNumber1:
         ADD DL,48
    MOV AH,02H
    INT 21H

    POP DX
    POP CX
    RET
outputNum endp

end

