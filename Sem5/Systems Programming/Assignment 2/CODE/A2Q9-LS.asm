;Program to Implement Linear search.
new_line macro
	mov ah,02h
	mov dl,0dh
	int 21h
	mov dl,0ah
	int 21h
endm

;macro to print space
space macro
	mov ah,02h
	mov dl,' '
	int 21h
endm

;macro to print a message
printm macro mess
	lea dx,mess
	mov ah,09h
	int 21h
endm

;macro to exit
exitp macro
	mov ah,4ch
	int 21h
endm
pushall macro
	push ax
	push bx
	push cx
	push dx
endm

popall macro
	pop dx
	pop cx
	pop bx
	pop ax
endm

; macro for decimal input
dec_input macro
	local input,skip
	; output: bx
	xor bx,bx
	mov ah,01h
	int 21h
	;if \r
	cmp al,0dh
	je skip
	input:
		and ax,000fh
		push ax
		; bx=bx*10+ax
		mov ax,10
		mul bx
		mov bx,ax
		pop ax
		add bx,ax
		; take input
		mov ah,01h
		int 21h
		cmp al,0dh
		jne input
	skip:
endm

; macro for decimal output
dec_output macro
	local start,repeat,display
	start:                        ; jump label
		mov ax, bx                     ; set ax=bx
		xor cx, cx                     ; clear cx
		mov bx, 10                     ; set bx=10
	repeat:                       ; loop label
		xor dx, dx                   ; clear dx
		div bx                       ; divide ax by bx
		push dx                      ; push dx onto the stack
		inc cx                       ; increment cx
		or ax, ax                    ; take or of ax with ax
		jne repeat                    ; jump to label repeat if zf=0
		mov ah, 2                      ; set output function
	display:                      ; loop label
		pop dx                       ; pop a value from stack to dx
		or dl, 30h                   ; convert decimal to ascii code
		int 21h                      ; print a character
		loop display
endm
.model small
.stack 100h
.data
	inpmsg1 db 10,13,"Enter size of array: $"
	inpmsg2 db 10,13,"Enter elements of array: $"
	inpmsg3 db 10,13,"Enter element to be searched: $"
	oupmsg1 db 10,13,"element found at: $"
	oupmsg2 db 10,13,"element not found $"
	arr dw 50 dup(?)
	s dw ?
.code
	main proc
		mov ax,@data
		mov ds,ax
		;input size
		printm inpmsg1		
		dec_input
		;input elements
		printm inpmsg2
		new_line
		mov s,bx
		lea si,arr
		mov cx,bx
		@array_input:
			pushall
			dec_input
			mov word ptr[si],bx
			popall
			inc si
			inc si
		loop @array_input
		; enter element to search
		printm inpmsg3
		dec_input
		lea si,arr
		mov cx,s
		@linear_search:
			cmp bx,word ptr[si]
			je @found
			inc si
			inc si
		loop @linear_search
		;if not found
		printm oupmsg2
		jmp @exit
		@found:
			printm oupmsg1
			mov bx,s
			sub bx,cx
			inc bx
			dec_output
		@exit:
			exitp
	main endp
end main