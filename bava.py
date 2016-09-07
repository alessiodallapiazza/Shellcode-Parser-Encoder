#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Simone Cardona

import codes
import os
import sys
import random

def encode():
	final = ''
	r = random.randrange(2,9)
	i = 0
	instr = ['ADD', 'SUB', 'XOR']
	
	for c in range(r):
		value = random.randrange(1,9)
		encode_i = random.choice(instr)
		if "XOR" in encode_i:
			if i != 1:
				final += "%s BYTE [esi], 0x0f\n" % (encode_i)
				i = 1
		else:
			final += "%s BYTE [esi], %s\n" % (encode_i, value)
	return final
	
def decode(string):
	string = string.split('\n')
	string.pop()
	tmp = ''
	for s in reversed(string):
		if "ADD" in s:
			tmp1 = s[3:]
			tmp += "%s %s\n" % ("SUB", tmp1)
			
		if "XOR" in s:
			tmp += "%s\n" % s
			
		if "SUB" in s:
			tmp1 = s[3:]
			tmp += "%s %s\n" % ("ADD", tmp1)
	return tmp

if __name__ == "__main__":
	if(len(sys.argv) < 3) or sys.argv[1] == '-h':
		print("usage: BAVA.py -e <shellcode> <encoder>")
		print("\nencoder: xor, random, insertion, not")
		sys.exit(0)
	
	if sys.argv[1] == "-e":
		if sys.argv[3] == 'xor':
			encoded = ''	
			buf = sys.argv[2]
			buf = buf.decode('string-escape')
			for x in bytearray(buf):
				y = x ^ 0xaa
			
				encoded += '0x'
				encoded += '%02x,' % (y & 0xff)
			xor = codes.asm_generate_xor(len(buf), encoded)
			file = open("xor.asm", "w")
			file.write(xor)
			file.close()
			os.system("nasm -f elf xor.asm")
			print("[!] Generating xor.asm")
			os.system("ld xor.o -o xor")
			os.system("objdump -D xor > result")
			print("[!] Generating result")
			
			with open('result', 'r') as infile:
				list = []
				for line in infile:
					if "CTOR_LIST__>:" in line:
						break
					tmp = line.split("\t")

					if(len(tmp) > 2):
						list.append(tmp[1])
						print(tmp[1])
					
			string = ''
			list1 = []
			for i in list:
				string += i.replace(' ', '')
			string = '\\x'.join(a+b for a,b in zip(string[::2], string[1::2]))
			new = string[:0] + '\\x' + string[0:]
			print new
			sys.exit(0)
			
		if sys.argv[3] == 'random':
			encoded = ''	
			buf = sys.argv[2]
			buf = buf.decode('string-escape')
			instructions = encode()
			instructions0 = instructions
			instructions = instructions.split('\n')
			for x in bytearray(buf):
				y = x
				for line in instructions:
					if 'ADD' in line:
						y += int(line[-2:])
					if 'SUB' in line:
						y -= int(line[-2:])
					if 'XOR' in line:
						y = y ^ 0x0f
			
				encoded += '0x'
				encoded += '%02x,' % (y & 0xff)
			
			instructions1 = decode(instructions0)
			
			random = codes.asm_generate_random(len(buf), instructions1, encoded)
			file = open("random.asm", "w")
			file.write(random)
			file.close()
			os.system("nasm -f elf random.asm")
			print("[!] Generating random.asm")
			os.system("ld random.o -o random")
			os.system("objdump -D random > result")
			print("[!] Generating result")
			
			with open('result', 'r') as infile:
				list = []
				for line in infile:
					if "CTOR_LIST__>:" in line:
						break
					tmp = line.split("\t")

					if(len(tmp) > 2):
						list.append(tmp[1])
						print(tmp[1])
					
			string = ''
			list1 = []
			for i in list:
				string += i.replace(' ', '')
			string = '\\x'.join(a+b for a,b in zip(string[::2], string[1::2]))
			new = string[:0] + '\\x' + string[0:]
			print new
			sys.exit(0)
			
		if sys.argv[3] == 'insertion':
			encoded = ''	
			buf = sys.argv[2]
			buf = buf.decode('string-escape')
			for x in bytearray(buf):
				encoded += '0x'
				encoded += '%02x,' %x
				encoded += '0x%02x,' % 0xAA
			insertion = codes.asm_generate_insertion(encoded)
			file = open("insertion.asm", "w")
			file.write(insertion)
			file.close()
			os.system("nasm -f elf insertion.asm")
			print("[!] Generating insertion.asm")
			os.system("ld insertion.o -o insertion")
			os.system("objdump -D insertion > result")
			print("[!] Generating result")
			
			with open('result', 'r') as infile:
				list = []
				for line in infile:
					if "CTOR_LIST__>:" in line:
						break
					tmp = line.split("\t")

					if(len(tmp) > 2):
						list.append(tmp[1])
						print(tmp[1])
					
			string = ''
			list1 = []
			for i in list:
				string += i.replace(' ', '')
			string = '\\x'.join(a+b for a,b in zip(string[::2], string[1::2]))
			new = string[:0] + '\\x' + string[0:]
			print new
			sys.exit(0)
			
			
		if sys.argv[3] == 'not':
			encoded = ''	
			buf = sys.argv[2]
			buf = buf.decode('string-escape')
			for x in bytearray(buf):
				y = ~x
				encoded += '0x'
				encoded += '%02x,' %(y & 0xff)
			no = codes.asm_generate_not(len(buf), encoded)
			file = open("not.asm", "w")
			file.write(no)
			file.close()
			os.system("nasm -f elf not.asm")
			print("[!] Generating not.asm")
			os.system("ld not.o -o not")
			os.system("objdump -D not > result")
			print("[!] Generating result")
			
			with open('result', 'r') as infile:
				list = []
				for line in infile:
					if "CTOR_LIST__>:" in line:
						break
					tmp = line.split("\t")

					if(len(tmp) > 2):
						list.append(tmp[1])
						print(tmp[1])
					
			string = ''
			list1 = []
			for i in list:
				string += i.replace(' ', '')
			string = '\\x'.join(a+b for a,b in zip(string[::2], string[1::2]))
			new = string[:0] + '\\x' + string[0:]
			print new
			sys.exit(0)
