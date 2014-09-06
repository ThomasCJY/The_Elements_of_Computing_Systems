#!/usr/bin/python
import sys,os
import Parser
CODEFLAG1=0
CODEFLAG2=0
RETURNFLAG=1

def setFileName(filename):
	filetuple=os.path.splitext(filename)
	wfile = open(filetuple[0]+'.asm','w')
	return wfile

def writeArithmatic(wfile,command):
	global CODEFLAG1,CODEFLAG2
	if command == 'add':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n')
	elif command == 'sub':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n')
	elif command == 'neg':
		wfile.write('@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n')
	elif command == 'and':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1\n')
	elif command == 'or':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n')
	elif command == 'not':
		wfile.write('@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n')
	elif command == 'eq':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n@RET_TRUE'+str(CODEFLAG1)+'\
			\nD;JEQ\nD=0\n@CONTINUE'+str(CODEFLAG2)+'\n0;JMP\n(RET_TRUE'+str(CODEFLAG1)+')\nD=-1\
			\n(CONTINUE'+str(CODEFLAG2)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		CODEFLAG1+=1
		CODEFLAG2+=1
	elif command == 'gt':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@RET_TRUE'+str(CODEFLAG1)+'\
			\nD;JGT\nD=0\n@CONTINUE'+str(CODEFLAG2)+'\n0;JMP\n(RET_TRUE'+str(CODEFLAG1)+')\nD=-1\
			\n(CONTINUE'+str(CODEFLAG2)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		CODEFLAG1+=1
		CODEFLAG2+=1
	elif command == 'lt':
		wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@RET_TRUE'+str(CODEFLAG1)+'\
			\nD;JLT\nD=0\n@CONTINUE'+str(CODEFLAG2)+'\n0;JMP\n(RET_TRUE'+str(CODEFLAG1)+')\nD=-1\
			\n(CONTINUE'+str(CODEFLAG2)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		CODEFLAG1+=1
		CODEFLAG2+=1


def writePushPop(wfile,command,segment,index,filename):
	if command == 'C_PUSH':
		if segment == 'constant':
			wfile.write('@'+index+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		elif segment == 'local':
			wfile.write('@LCL\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		elif segment == 'argument':
			wfile.write('@ARG\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		elif segment == 'this':
			wfile.write('@THIS\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		elif segment == 'that':
			wfile.write('@THAT\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		elif segment == 'pointer':
			if index == '0':
				wfile.write('@3\n')
			elif index == '1':
				wfile.write('@4\n')
			wfile.write('D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
		elif segment == 'static':
			staticname=filename.strip('.vm')+'.'+index
			wfile.write('@'+staticname+'\nD=A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
	elif command =='C_POP': 
		if segment == 'local':
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n@LCL\nA=M\n')
			for i in range (0,int(index)):
				wfile.write('A=A+1\n')
			wfile.write('M=D\n')
		if segment =='argument':
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\n')
			for i in range (0,int(index)):
				wfile.write('A=A+1\n')
			wfile.write('M=D\n')
		if segment == 'this':
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THIS\nA=M\n')
			for i in range (0,int(index)):
				wfile.write('A=A+1\n')
			wfile.write('M=D\n')
		if segment == 'that':
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THAT\nA=M\n')
			for i in range (0,int(index)):
				wfile.write('A=A+1\n')
			wfile.write('M=D\n')
		if segment == 'pointer':
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n')
			if index == '0':
				wfile.write('@3\n')
			else:
				wfile.write('@4\n')
			wfile.write('M=D\n')
		if segment == 'static':
			staticname=filename.strip('.vm')+'.'+index
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n@'+staticname+'\nM=D\n')
		if segment == 'temp':
			wfile.write('@SP\nM=M-1\nA=M\nD=M\n@R5\n')
			for i in range (0,int(index)):
				wfile.write('A=A+1\n')
			wfile.write('M=D\n')

def writeLabel(wfile,labelstring):
	wfile.write('('+labelstring+')\n')

def writeGoto(wfile,labelstring):
	wfile.write('@'+labelstring+'\n0;JMP\n')

def writeIf(wfile,labelstring):
	wfile.write('@SP\nM=M-1\nA=M\nD=M\n@'+labelstring+'\nD;JNE\n')

def writeFunction(wfile,functionName,numlocals):
	wfile.write('('+functionName+')\n@LCL\nD=M\n@SP\nM=D\n')
	for i in range(0,int(numlocals)):
		wfile.write('@SP\nA=M\nM=0\nD=A+1\n@SP\nM=D\n')

def writeCall(wfile,functionName,numArgs):
	global RETURNFLAG
	wfile.write('@return_address'+str(RETURNFLAG)+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@'+numArgs+'\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\
		\n@'+functionName+'\n0;JMP\n(return_address'+str(RETURNFLAG)+')\n')
	RETURNFLAG+=1

def writeReturn(wfile):
	wfile.write('@LCL\nD=M\n@R13\nM=D\n@5\nD=D-A\nA=D\nD=M\
		\n@R14\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\
		\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n@R13\nD=M\nD=D-1\
		\nA=D\nD=M\n@THAT\nM=D\n@R13\nD=M\nD=D-1\nD=D-1\
		\nA=D\nD=M\n@THIS\nM=D\n@R13\nD=M\nD=D-1\nD=D-1\
		\nD=D-1\nA=D\nD=M\n@ARG\nM=D\n@R13\nD=M\nD=D-1\
		\nD=D-1\nD=D-1\nD=D-1\nA=D\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP\n')


def Close(wfile):
	wfile.close()
