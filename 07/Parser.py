#!/usr/bin/python
Arith=('add','sub','neg','eq','gt','lt','and','or','not')

def hasMoreCommands(line):
	if not line:
		return 0
	else:
		return 1

def advance(rfile):
	line=rfile.readline()
	return line

def commandType(line):
	if line.find('push')>=0:
		return 'C_PUSH'
	elif line.find('pop')>=0:
		return 'C_POP'
	elif line.strip() in Arith:
		return 'C_ARITHMATIC'

def arg1(line):
	if commandType(line) is 'C_ARITHMATIC':
		return line.strip()
	else:
		spline=line.split(' ')
		return spline[1]

def arg2(line):
	if commandType(line) in ('C_POP','C_PUSH','C_FUNCTION','C_CALL'):
		spline=line.split(' ')
		return spline[2]

