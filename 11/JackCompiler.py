#!/usr/bin/python
import CompilationEngine
import SymbolTable
import sys,os

'''
The command line of this module is : JackCompiler.py (-x) sourcename
The first option is -x, which decides whether to run xmlWriter() and to output the constructive xml file\
putting forward by CompilationEngine.
'''

option=sys.argv[1]
if option == '-x':
	filename=sys.argv[2]
else:
	filename=sys.argv[1]

#clear all the // /* ... notes, create a new file to save the result
readfile = open(filename,'r')
copyfile = open('copyfile','w')
line=readfile.readline()
while line:
	while line == '\n' or line.startswith('//'):
		line=readfile.readline()
	if '//' in line:
		line=line[:line.find('//')]
	if '/*' in line:
		aline=line[:line.find('/*')]
		while line.find('*/')<0:
			line=readfile.readline()
		bline=line[line.find('*/')+2:]
		line=aline+bline
	copyfile.write(line)
	line=readfile.readline()
copyfile.close()
readfile.close()

#Main Function
readCopyFile=open('copyfile','r')
writeXmlFile=open(filename.strip('.jack')+'.xml','w')
writeVmFile=open(filename.strip('.jack')+'.vm','w')

outputCompile=CompilationEngine.Compile(readCopyFile,writeXmlFile,writeVmFile)
outputCompile.compileClass()

readCopyFile.close()
writeXmlFile.close()
writeVmFile.close()
os.remove('copyfile')

if option != '-x':
	os.remove(filename.strip('.jack')+'.xml')




