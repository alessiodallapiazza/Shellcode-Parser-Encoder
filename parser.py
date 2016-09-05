#!/usr/bin/python

import sys
import re

if(len(sys.argv) != 2):
        print("Usage: %s <objdump_shellcode>" % sys.argv[0])
        sys.exit(1)

with open(sys.argv[1], 'r') as infile:
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
