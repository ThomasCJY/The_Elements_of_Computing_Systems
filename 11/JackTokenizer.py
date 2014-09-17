#!/usr/bin/python
STable=('{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~')
KWtable=('class','constructor','function','method','field','static','var','int','char','boolean',\
	'void','true','false','null','this','let','do','if','else','while','return')

class Tokenizer():
	def __init__(self,rfile):
		self.rfile=rfile
		self.token=''

	def hasMoreTokens(self):
		temp=self.rfile.read(1)
		while temp in ' \n\t' and temp != '':
			temp=self.rfile.read(1)
		if not temp:
			return 0
		else:
			self.rfile.seek(-1,1)
			return 1

	def advance(self):
		self.token=''
		temp=self.rfile.read(1)

		if temp.isalpha() or temp.isdigit() or temp == '_':
			while temp.isalpha() or temp.isdigit() or temp == '_':
				self.token+=temp
				temp=self.rfile.read(1)
			if temp in STable or temp =='"':
				self.rfile.seek(-1,1)
			elif temp == ' ' or temp == '\n':
				self.rfile.seek(-1,1)
		elif temp in STable:
			self.token=temp
		elif temp =='"':
			self.token += '"'
			temp=self.rfile.read(1)
			while temp != '"':
				self.token+=temp
				temp=self.rfile.read(1)
			self.token+='"'

	def tokenType(self):
		if self.token in KWtable:
			return 'KEYWORD'
		elif self.token in STable:
			return 'SYMBOL'
		elif self.token.isdigit():
			return 'INT_CONSTANT'
		elif self.token.startswith('"'):
			return 'STRING_CONSTANT'
		else:
			return 'IDENTIFIER'

	def Keyword(self):
		return self.token

	def Symbol(self):
		return self.token

	def Identifier(self):
		return self.token

	def intVal(self):
		return int(self.token)

	def stringVal(self):
		return self.token