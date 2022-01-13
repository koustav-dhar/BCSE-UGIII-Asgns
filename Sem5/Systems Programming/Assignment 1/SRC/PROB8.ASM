.model small
.stack 100h

.data
prompt0 db "Enter the number of array elements: ",0dh,0ah,"$"
prompt1 db "Enter the array elements: ",0dh,0ah,"$"
prompt2 db "The maximum is: $"
prompt3 db "The minimum is: $"

array dw 50 dup(0)

s dw ?

.code
main proc
        MOV AX,@data
        MOV DS,AX

        LEA DX,prompt0
        MOV AH,09H
        INT 21H

        MOV AH,01H
        INT 21H

        input1:
        CMP AL,0DH   ;check for enter
        JE line1
        CMP AL,0AH
        JE line1
        AND AL,0FH   ;convert ascii to real value by masking

        SHL BX,1
	SHL BX,1
	SHL BX,1
	SHL BX,1

        OR BL,AL     ;add current value with previous value

        INT 21H
        JMP input1

        line1:
        LEA DX,prompt1
        MOV AH,09H
        INT 21H

        LEA SI,array
        MOV CX,BX

        @read_array:  ;loop label

        MOV AH,01H
        INT 21H

        XOR DX,DX

        input2:
        CMP AL,0DH
        JE line2
        CMP AL,0AH
        JE line2
        AND AL,0FH
        SHL DX,1
	SHL DX,1
	SHL DX,1
	SHL DX,1
        OR DL,AL

        INT 21H
        JMP input2

        line2:
        MOV [SI],DX
        ADD SI,2

        MOV DL,0AH
        MOV AH,02H
        INT 21H

        loop @read_array

        LEA SI,array
        MOV AX,BX
        DEC AX
        XOR BX,BX
        XOR CX,CX
        MOV BX,word ptr[SI]   ;store the maximum
        MOV CX,word ptr[SI]   ;store the minimum
        ADD SI,2
        ;loop to find max and min
        arrayLoop:

        CMP word ptr[SI],BX
        JG maximum
        CMP word ptr[SI],CX
        JL minimum

        JMP incre
        maximum:
        MOV BX,word ptr[SI]
        JMP incre

        minimum:
        MOV CX,word ptr[SI]

        incre:
        ADD SI,2
        DEC AX

        JNZ arrayLoop

        LEA DX,prompt2
        MOV AH,09H
        INT 21H

        output:

        MOV DH,BH
        SHR DH,1
	SHR DH,1
	SHR DH,1
	SHR DH,1
        AND DH,0FH
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DH,BH
        AND DH,0FH
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DH,BL
       	SHR DH,1
	SHR DH,1
	SHR DH,1
	SHR DH,1
        AND DH,0FH
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DH,BL
        AND DH,0FH
        CMP DH,10
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DL,0AH
        MOV AH,02H
        INT 21H

        LEA DX,prompt3
        MOV AH,09H
        INT 21H

        MOV BX,CX

        MOV DH,BH
        SHR DH,1
	SHR DH,1
	SHR DH,1
	SHR DH,1
        AND DH,0FH
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DH,BH
        AND DH,0FH
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DH,BL
        SHR DH,1
	SHR DH,1
	SHR DH,1
	SHR DH,1
        AND DH,0FH
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV DH,BL
        AND DH,0FH
        CMP DH,10
        ADD DH,'0'
        MOV DL,DH
        MOV AH,02H
        INT 21H

        MOV AH,4CH
        INT 21H
main endp
end
