#!/usr/bin/python
class SymbolTable:
	'''
	SymbolTable is a two-dimensional list.
	The first list contains all the names of the symbols. And Each name 
	is also a single list, containing the [name,type,kind,index] of the 
	symbol.
	'''
	def __init__(self):
		self.Scope=[]

	def Constructor(self):
		self.Scope=[]

	def startSubroutine(self):
		self.Scope=[]

	def FoundName(self,name):
		#Search the funcName in SymbolTable
		for i in range(0,len(self.Scope)):
			if name == self.Scope[i][0]:
				return i
		return -1

	def Define(self,name,segType,kind):
		#Add new elements into the List.
		index=self.VarCount(kind)
		if kind == 'field':
			kind='this'		
		elif kind == 'var':
			kind='local'
		name=[name,segType,kind,index]
		self.Scope.append(name)

	def VarCount(self,kind):
		#count the number of existed elements with 'kind'.
		#It is used to count the index of the elements.
		if kind == 'field':
			kind='this'		
		elif kind == 'var':
			kind='local'
		lengthKind=0
		for i in range(0,len(self.Scope)):
			if self.Scope[i][2]==kind:
				lengthKind+=1
		return lengthKind

	def KindOf(self,name):
		for i in range(0,len(self.Scope)):
			if name == self.Scope[i][0]:
				return self.Scope[i][2]
		return 'NONE'

	def TypeOf(self,name):
		for i in range(0,len(self.Scope)):
			if name == self.Scope[i][0]:
				return self.Scope[i][1]
		return 'NONE'

	def IndexOf(self,name):
		for i in range(0,len(self.Scope)):
			if name == self.Scope[i][0]:
				return self.Scope[i][3]
		return 'NONE'


