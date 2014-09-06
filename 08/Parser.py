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
	elif line.startswith('label'):
		return 'C_LABEL'
	elif line.startswith('goto'):
		return 'C_GOTO'
	elif line.startswith('if-goto'):
		return 'C_IF'
	elif line.strip() in Arith:
		return 'C_ARITHMATIC'
	elif line.startswith('function'):
		return 'C_FUNCTION'
	elif line.startswith('return'):
		return 'C_RETURN'
	elif line.startswith('call'):
		return 'C_CALL'

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

