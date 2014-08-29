#!/usr/bin/python
def hasMoreCommands(line):
	if not line:
		return 0
	else:
		return 1

def advance(rfile,line):
	line=rfile.readline()
	return line

def commandType(line):
	if line.find('@')>=0:
		return 'A_COMMAND'
	elif line.find('=')>=0 or line.find(';')>=0:
		return 'C_COMMAND'
	elif line.find('(')>=0:
		return 'L_COMMAND'

def symbol(line):
	symbolflag=line.strip(' @()\n')
	return symbolflag

def dest(line):
	if line.find('=')>=0:
		destlist=line.split('=')
		return destlist[0].strip(' ')
	elif line.find(';')>=0:
		return 'null'

def comp(line):
	if line.find('=')>=0:
		complist1=line.split('=')
		return complist1[1].strip('\n')
	elif line.find(';')>=0:
		complist2=line.split(';')
		return complist2[0].strip(' ')

def jump(line):
	if line.find('=')>=0:
		return 'null'
	elif line.find(';')>=0:
		jumplist=line.split(';')
		return jumplist[1].strip(' \n')