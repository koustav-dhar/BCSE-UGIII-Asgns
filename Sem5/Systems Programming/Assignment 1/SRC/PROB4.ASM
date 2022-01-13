.model small
.stack 100h

.data
prompt0  db  "Enter the number of array elements :",0dh,0ah,"$"
prompt1  db  "Enter the array elements :",0dh,0ah,"$"
prompt2  db  "The 2nd maximum is : $"
prompt3  db  "The 2nd minimum is : $"

array   dw  50 dup(0)    

s dw ?
max dw ?
min dw ?

.code
main proc

		MOV AX, @data                ; initialize ds
		MOV DS, AX

		LEA DX, prompt0             ; load and display the string prompt_0
		MOV AH, 09H     
		INT 21H

		MOV AH, 01H                                    ;for taking input
		INT 21H

		input1:
		CMP AL, 0DH                                  ;compare whether the pressed key is 'enter' or not
		JE line1                                    ;if it is equal to 'enter' then stop taking first value

		AND AL, 0FH                                  ;convert it's ascii value to real value by masking

		SHL BX, 1
		SHL BX, 1
		SHL BX, 1
		SHL BX, 1
		OR BL, AL                                   ;making 'or' will add the current value with previous value

		INT 21H
		JMP input1

		line1:     
		LEA DX, prompt1             ; load and display the string prompt_1
		MOV AH, 09H    
		INT 21H

		LEA SI, array                ; set si=offset address of array
		MOV S,BX
		MOV CX, BX                     ; set cx=bx


		@read_array:                   ; loop label

		MOV AH, 01H                                    ;for taking input
		INT 21H

		XOR DX, DX

		input2:
		CMP AL, 0DH                                  ;compare whether the pressed key is 'enter' or not
		JE line2                                   ;if it is equal to 'enter' then stop taking first value

		AND AL, 0FH                                 ;convert it's ascii value to real value by masking

		SHL DX, 1
		SHL DX, 1
		SHL DX, 1
		SHL DX, 1
		OR DL, AL                                   ;making 'or' will add the current value with previous value

		INT 21H
		JMP input2

		line2:
		MOV [SI], DX                 ; set [si]=ax
		ADD SI, 2                    ; set si=si+2

		MOV DL, 0AH                  ; line feed
		MOV AH, 02H                    ; set output function
		INT 21H                      ; print a character

		loop @read_array               ; jump to label @read_array while cx!=0 
		; array input done

		LEA SI,array
		MOV AX, BX
		DEC AX
		XOR BX, BX
		XOR CX, CX
		MOV BX,word ptr[SI]	;store the maximum
		MOV CX,word ptr[SI]	;store the 2nd
		ADD SI, 2

		; loop to find max and 2nd max
		arrayloop2:

		CMP word ptr[SI],BX
		JL max2
		MOV CX, BX
		MOV BX,word ptr[SI]

		max2:
		CMP word ptr[SI],CX
		JL incre
		CMP word ptr[SI],BX
		JE incre
		MOV CX,word ptr[SI]
		
		incre:
		ADD SI, 2
		DEC AX

		jnz arrayloop2

		; now bx has max cx has 2nd max
		MOV max, BX
		; displaying the prompt
		LEA DX,prompt2
		MOV AH, 09H
		INT 21H

		; display contents of cx
		MOV BX, CX

		MOV DH, BH
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		AND DH, 0FH
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DH, BH
		AND DH, 0FH
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DH, BL
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		AND DH, 0FH
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DH, BL
		AND DH, 0FH
		CMP DH,10
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DL, 0AH                  ; line feed
		MOV AH, 02H	             ; set output function
		INT 21H                      ; print a character

		LEA SI,array
		MOV AX,s
		DEC AX
		MOV BX,max


		; loop to find min and 2nd min
		arrayloop3:

		CMP word ptr[SI],BX
		JG min2
		MOV CX, BX
		MOV BX,word ptr[SI]

		min2:
		CMP word ptr[SI],CX
		JG incre2
		CMP word ptr[SI],BX
		JE incre2
		MOV CX,word ptr[SI]
		
		incre2:
		ADD SI, 2
		DEC AX

		jnz arrayloop3

		; now bx has min cx has 2nd min

		; displaying the prompt
		LEA DX,prompt3
		MOV AH, 09H
		INT 21H

		; display contents of cx
		MOV BX, CX

		MOV DH, BH
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		AND DH, 0FH
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DH, BH
		AND DH, 0FH
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DH, BL
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		SHR DH, 1
		AND DH, 0FH
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H

		MOV DH, BL
		AND DH, 0FH
		CMP DH,10
		ADD DH,'0'                               
		MOV DL, DH
		MOV AH, 02H
		INT 21H


		exit:
		MOV AH, 4CH                               ;return control to dos
		INT 21H

main endp
end main
