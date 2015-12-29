import re
import sys
import os

"""
bin -> num
num -> bin

getHighBit
getLenght

"""

def getValuefromBin(string):
	res = 0
	for char in string:
		bit = 1 if char == "1" else 0
		res = (res << 1) + bit
	return res

def getBinfromValue(value):
	if value == 0:
		return 0
	res = ""
	while value != 0:
		if value % 2 == 1:
			res = "1" + res
		else:
			res = "0" + res
		value = value / 2
	return res

def splitValuetoLenghtandOffset(value):
	binstring = getBinfromValue(value)
	HighLen = len(binstring) - 1
	Offset = binstring[1:]
	return HighLen, Offset

def unary_encode_High(HighLen):
	return "1" * (HighLen) + "0"

def unary_decode_Highlen(string):
	res = 0
	for (i, char) in enumerate(string):
		if char == "1":
			res += 1
		elif char == "0":
			break
	return res

def Gamma_encode(value):
	HighLen, Offset = splitValuetoLenghtandOffset(value)
	HighLen_string = unary_encode_High(HighLen)
	return HighLen_string+Offset

def Gamma_decode(string):
	HighLen = unary_decode_Highlen(string)
	Highnumber = (1 << HighLen)
	Offset = string[HighLen+1:]
	Offset_number = getValuefromBin(Offset)
	return Highnumber+Offset_number

if __name__ == '__main__':
	it = 8
	#print "Input a number to get the GammaCode:%d"%it
	value = int(input("Input a number to get the GammaCode: "))
	print Gamma_encode(value)

	#print "Input a Gamma_string to get the number:"
	string = str(input("Input a Gamma_string to get the number: "))
	print Gamma_decode(string)









