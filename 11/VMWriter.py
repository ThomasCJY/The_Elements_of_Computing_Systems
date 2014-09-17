#!/usr/bin/python

class VMwriter:
	def __init__(self,wfile):
		self.wfile=wfile

	def writePush(self,segment,index):
		self.wfile.write('push '+segment+' '+str(index)+'\n')

	def writePop(self,segment,index):
		self.wfile.write('pop '+segment+' '+str(index)+'\n')

	def writeArithmetic(self,command):
		self.wfile.write(command+'\n')

	def writeFunction(self,functionName,LclNum):
		self.wfile.write('function '+functionName+' '+str(LclNum)+'\n')

	def writeReturn(self):
		self.wfile.write('return\n')

	def writeCall(self,functionName,ELNum):
		self.wfile.write('call '+functionName+' '+str(ELNum)+'\n')

	def writeLabel(self,label):
		self.wfile.write('label '+label+'\n')

	def writeGoto(self,label):
		self.wfile.write('goto '+label+'\n')

	def writeIf(self,label):
		self.wfile.write('if-goto '+label+'\n')

