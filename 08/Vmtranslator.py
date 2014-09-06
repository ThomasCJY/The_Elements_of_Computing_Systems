#!/usr/bin/python
import sys,os
import Parser
import CodeWriter
DELETEFLAG=0

def Main(rfile,wfile,filename):
	line=Parser.advance(rfile)
	flag=Parser.hasMoreCommands(line)
	while flag:
		while line == '\n' or line.startswith('//'):
			line=rfile.readline()
		if '//' in line:
			line=line[:line.find('//')]
		ctype=Parser.commandType(line)
		if ctype == 'C_ARITHMATIC':
			attribute1=Parser.arg1(line).strip()
			CodeWriter.writeArithmatic(wfile,attribute1)
		elif ctype in ('C_PUSH','C_POP'):
			attribute1=Parser.arg1(line).strip()
			attribute2=Parser.arg2(line).strip()
			CodeWriter.writePushPop(wfile,ctype,attribute1,attribute2,filename)
		elif ctype =='C_LABEL':
			attribute1=Parser.arg1(line).strip()
			CodeWriter.writeLabel(wfile,attribute1)
		elif ctype =='C_GOTO':
			attribute1=Parser.arg1(line).strip()
			CodeWriter.writeGoto(wfile,attribute1)
		elif ctype =='C_IF':
			attribute1=Parser.arg1(line).strip()
			CodeWriter.writeIf(wfile,attribute1)	
		elif ctype =='C_FUNCTION':
			attribute1=Parser.arg1(line).strip()
			attribute2=Parser.arg2(line).strip()
			CodeWriter.writeFunction(wfile,attribute1,attribute2)
		elif ctype =='C_RETURN':
			CodeWriter.writeReturn(wfile)
		elif ctype =='C_CALL':
			attribute1=Parser.arg1(line).strip()
			attribute2=Parser.arg2(line).strip()
			CodeWriter.writeCall(wfile,attribute1,attribute2)		
		line=Parser.advance(rfile)
		flag=Parser.hasMoreCommands(line)





filename=sys.argv[1]
#if filename exists in the dir, open the file directly
if os.path.isfile(filename):
	rfile = open(filename,'r')
	wfile = CodeWriter.setFileName(filename)
	wfile.write('@256\nD=A\n@SP\nM=D\n')
	Main(rfile,wfile,filename)
#if filename doesn't exist, find all the .vm files
elif os.path.isfile('Sys.vm'):
	wfile = CodeWriter.setFileName(filename)
	wfile.write('@256\nD=A\n@SP\nM=D\n')
	wfile.write('@return_address0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@0\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\
		\n@Sys.init\n0;JMP\n(return_address0)\n')
	#check all the files in the dir
	for i in os.walk(os.getcwd()):
		filelist=i[2]
	for j in range(0,len(filelist)):
		if filelist[j].endswith('.vm'):
			#readfile, copy to the end
			filename=filelist[j]
			rfile = open(filename,'r')
			Main(rfile,wfile,filename)
	DELETEFLAG=1
else:
	print 'Wrong Instruction!'
	exit()

rfile.close()
CodeWriter.Close(wfile)

if DELETEFLAG == 1:
	os.remove(filename)


