#!/usr/bin/python
import sys
import Parser
import Code
import SymbolTable

filename=sys.argv[1]
#The first Loop, aiming to decide the lables' addresses
symboldict=SymbolTable.Constructor()
rfile = open(filename,'r')
i=0 #i is the sum of the construction numbers above lables
linepre=rfile.readline()
flag=Parser.hasMoreCommands(linepre)
while flag:
	#clean the line which starts with // or blank lines
	while linepre == '\n' or linepre.startswith('//'):
		linepre=rfile.readline()

	if linepre.find('(')>=0:
		symbol=linepre.strip('()\n')
		if not SymbolTable.contains(symbol,symboldict):
			symboldict=SymbolTable.addEntry(symbol,i,symboldict)
	else: 
		i+=1

	linepre=Parser.advance(rfile,linepre)
	flag=Parser.hasMoreCommands(linepre)

rfile.close()

#The second Loop
j=0 #j records the total number of previous variables
rfile = open(filename,'r')
wfile = open('prog.hack','w')
#main loop
line=rfile.readline()
flag=Parser.hasMoreCommands(line)
while flag:
	while line == '\n' or line.startswith('//'):
		line=rfile.readline()

	ctype=Parser.commandType(line)
	#compare command type
	if ctype is 'A_COMMAND':
		AS=Parser.symbol(line)
		if not AS.isdigit():
			if not SymbolTable.contains(AS,symboldict):
				symboldict=SymbolTable.addEntry(AS,j+16,symboldict)
				j+=1
			binAS=bin(SymbolTable.GetAddress(AS,symboldict))[2:]
		else:
			binAS=bin(int(AS))[2:]
		AString=binAS.zfill(15)
		wfile.write('0'+AString+'\n')

	#L_COMMAND should be deleted

	elif ctype is 'C_COMMAND':
		DestString=Code.dest(line)
		CompString=Code.comp(line)
		JumpString=Code.jump(line)
		wfile.write('111'+CompString+DestString+JumpString+'\n')

	line=Parser.advance(rfile,line)
	flag=Parser.hasMoreCommands(line)

rfile.close()
wfile.close()