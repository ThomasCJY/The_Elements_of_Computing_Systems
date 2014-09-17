#!/usr/bin/python
import JackTokenizer
import SymbolTable
import VMWriter

class Compile():
	def __init__(self,rfile,wfile,wVmFile):
		self.rfile=rfile
		self.wfile=wfile #Write XML file
		self.vmWriter=VMWriter.VMwriter(wVmFile) #Write VM file
		self.tokenizer=JackTokenizer.Tokenizer(self.rfile)
		self.class_symbol=SymbolTable.SymbolTable()
		self.sub_symbol=SymbolTable.SymbolTable()
		self.Stype=''  #Stype records the type of the identifier.
		self.Skind=''
		#ClassName records the name of the class, used to make the sub_functionName
		self.ClassName=''
		self.expressionListNum=0	#Record the number of expression in ExpressionList.
		self.WHILEFLAG=0	#the index of while_loop in case of tautonomy
		self.IFFLAG=0
		

	def writeXmlTag(self,token):
		self.wfile.write(token)

	def writeXml(self,tType,token):
		if tType == 'symbol':
			if self.tokenizer.token=='>':
				self.writeXmlTag('<'+tType+'> '+'&gt'+' </'+tType+'>\n')
			elif self.tokenizer.token=='<':
				self.writeXmlTag('<'+tType+'> '+'&lt'+' </'+tType+'>\n')
			elif self.tokenizer.token=='&':
				self.writeXmlTag('<'+tType+'> '+'&amp'+' </'+tType+'>\n')
			else:
				self.writeXmlTag('<'+tType+'> '+token+' </'+tType+'>\n')
		else:
			self.writeXmlTag('<'+tType+'> '+token+' </'+tType+'>\n')

	def NextToken(self):
		if self.tokenizer.hasMoreTokens():
			self.tokenizer.advance()

	def moveBack(self):
		#Move back to the last token.
		lennum=-len(self.tokenizer.token)
		self.rfile.seek(lennum,1)

	def writeArrayPush(self,symbolName):
		#This function is used in 'Push' Array Terms.
		SubTag=self.sub_symbol.FoundName(symbolName)
		if SubTag==-1:
			ClassTag=self.class_symbol.FoundName(symbolName)
			if ClassTag==-1:
				print 'Error Term!'
				exit()
			else:
				self.vmWriter.writePush('this',self.class_symbol.Scope[ClassTag][3])
		else:
			KINDFLAG=self.sub_symbol.Scope[SubTag][2]
			self.vmWriter.writePush(KINDFLAG,self.sub_symbol.Scope[SubTag][3])

	def defineSymbol(self,symbolName,_symbol):
		#This function adds symbolName into SymbolTable.
		_symbol.Define(symbolName,self.Stype,self.Skind)

	def checkSymbol(self,symbolName):
		#Check the index of the Identifier
		SubTag=self.sub_symbol.FoundName(symbolName)
		if SubTag==-1:
			ClassTag=self.class_symbol.FoundName(symbolName)
			if ClassTag==-1:
				return -1
			else:
				return self.class_symbol.Scope[ClassTag]
		else:
			return self.sub_symbol.Scope[SubTag]

	def compileType(self):
		tType=self.tokenizer.tokenType()
		if tType == 'KEYWORD':
			self.Stype=self.tokenizer.token
			self.writeXml('keyword',self.tokenizer.token)
		elif tType == 'IDENTIFIER':
			self.Stype=self.tokenizer.token
			self.writeXml('identifier',self.tokenizer.token)

	def compileTermType(self):
		tType=self.tokenizer.tokenType()
		if tType == 'KEYWORD':
			kWord=self.tokenizer.token
			if kWord=='true':
				self.vmWriter.writePush('constant',1)
				self.vmWriter.writeArithmetic('neg')
			elif kWord=='false' or kWord=='null':
				self.vmWriter.writePush('constant',0)
			elif kWord=='this':
				self.vmWriter.writePush('pointer',0)
			self.writeXml('keyword',self.tokenizer.token)
		elif tType == 'INT_CONSTANT':
			self.writeXml('integerConstant',self.tokenizer.token)
			self.vmWriter.writePush('constant',int(self.tokenizer.token))
		elif tType == 'STRING_CONSTANT':	
			string_copy=self.tokenizer.token.strip('"')
			self.writeXml('stringConstant',string_copy)
			string_length=len(string_copy)
			self.vmWriter.writePush('constant',string_length)
			self.vmWriter.writeCall('String.new',1)
			for i in range(0,string_length):
				self.vmWriter.writePush('constant',ord(string_copy[i]))
				self.vmWriter.writeCall('String.appendChar',2)

	def compileVarDec(self):
		'''
		var type varName(,'varName')*;
		'''
		self.writeXmlTag('<varDec>\n')
		self.writeXml('keyword','var')
		self.Skind='var'
		#type
		self.NextToken()
		self.compileType()
		#varName
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		self.defineSymbol(self.tokenizer.token,self.sub_symbol)
		#(,varName)*
		self.NextToken()
		while self.tokenizer.token != ';':
			self.writeXml('symbol',self.tokenizer.token)
			self.NextToken()
			self.writeXml('identifier',self.tokenizer.token)
			self.defineSymbol(self.tokenizer.token,self.sub_symbol)
			self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</varDec>\n')
		
	def compileParameterList(self):
		'''
		((type varName)(, type varName)*)?
		'''
		self.writeXmlTag('<parameterList>\n')
		self.NextToken()
		while self.tokenizer.token != ')':
			self.Skind='argument'
			if self.tokenizer.token != ',':
				self.compileType()
				self.NextToken()
				self.writeXml('identifier',self.tokenizer.token)
				self.defineSymbol(self.tokenizer.token,self.sub_symbol)
				self.NextToken()
			else:
				self.writeXml('symbol',self.tokenizer.token)
				self.NextToken()
				self.compileType()
				self.NextToken()
				self.writeXml('identifier',self.tokenizer.token)
				self.defineSymbol(self.tokenizer.token,self.sub_symbol)
				self.NextToken()				
		self.writeXmlTag('</parameterList>\n')

	def compileClassVarDec(self):
		'''
		('static'|'field') type varName(, varName)*;
		'''
		self.writeXmlTag('<classVarDec>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.Skind=self.tokenizer.token

		self.NextToken()
		self.compileType()
		#varName
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		self.defineSymbol(self.tokenizer.token,self.class_symbol)
		#(,varName)*
		self.NextToken()
		while self.tokenizer.token != ';':
			self.writeXml('symbol',self.tokenizer.token)
			self.NextToken()
			self.writeXml('identifier',self.tokenizer.token)
			self.defineSymbol(self.tokenizer.token,self.class_symbol)
			self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</classVarDec>\n')

	def compileTerm(self):
		self.writeXmlTag('<term>\n')
		self.NextToken()
		tType=self.tokenizer.tokenType()
		if tType == 'IDENTIFIER':
			temp=self.rfile.read(1)
			if temp=='.':
				lennum=-len(self.tokenizer.token)-1
				self.rfile.seek(lennum,1)
				self.subroutineCall()
			elif temp=='[':
				self.writeXml('identifier',self.tokenizer.token)
				self.writeArrayPush(self.tokenizer.token)
				self.writeXml('symbol','[')
				self.compileExpression()
				self.vmWriter.writeArithmetic('add')
				self.vmWriter.writePop('pointer',1)
				self.vmWriter.writePush('that',0)
				self.writeXml('symbol',']')
			else:
				self.rfile.seek(-1,1)
				self.writeXml('identifier',self.tokenizer.token)
				ListSeg=self.checkSymbol(self.tokenizer.token)
				self.vmWriter.writePush(ListSeg[2],ListSeg[3])
		elif self.tokenizer.token in ('-','~'):
			UnaryOp=self.tokenizer.token
			self.writeXml('symbol',self.tokenizer.token)
			self.compileTerm()
			if UnaryOp == '-':
				self.vmWriter.writeArithmetic('neg')
			else:
				self.vmWriter.writeArithmetic('not')
		elif self.tokenizer.token == '(':
			self.writeXml('symbol',self.tokenizer.token)
			self.compileExpression()
			self.writeXml('symbol',')')
		else:
			self.compileTermType()
		self.writeXmlTag('</term>\n')

	def compileExpression(self):
		'''
		term (op term)*
		'''
		self.writeXmlTag('<expression>\n')
		self.compileTerm()
		self.NextToken()
		while (self.tokenizer.tokenType() == 'SYMBOL' and \
			self.tokenizer.Symbol() in '+-*/&|<>='):
			operator = self.tokenizer.Symbol()
			self.writeXml('symbol', self.tokenizer.token)
			self.compileTerm()
			if operator == '+':
				self.vmWriter.writeArithmetic('add')
			elif operator == '-':
				self.vmWriter.writeArithmetic('sub')
			elif operator == '*':
				self.vmWriter.writeCall('Math.multiply', 2)
			elif operator == '/':
				self.vmWriter.writeCall('Math.divide', 2)
			elif operator == '&':
				self.vmWriter.writeArithmetic('and')
			elif operator == '|':
				self.vmWriter.writeArithmetic('or')
			elif operator == '<':
				self.vmWriter.writeArithmetic('lt')
			elif operator == '>':
				self.vmWriter.writeArithmetic('gt')
			elif operator == '=':
				self.vmWriter.writeArithmetic('eq')
			self.NextToken()

		self.writeXmlTag('</expression>\n')	

	def compileExpressionList(self):
		self.writeXmlTag('<expressionList>\n')
		self.expressionListNum=0
		self.NextToken()
		while self.tokenizer.token != ')':
			if self.tokenizer.token != ',':
				self.moveBack()
				self.compileExpression()
				self.expressionListNum+=1
			else:
				self.writeXml('symbol',self.tokenizer.token)
				self.compileExpression()
				self.expressionListNum+=1
		self.writeXmlTag('</expressionList>\n')

	def subroutineCall(self):
		sub_MethodFlag=False 
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		sub_className=self.tokenizer.token
		self.NextToken()
		if self.tokenizer.token=='.':
			self.writeXml('symbol',self.tokenizer.token)
			self.NextToken()
			self.writeXml('identifier',self.tokenizer.token)
			sub_funcName=self.tokenizer.token
			#To check if sub_className is a ClassName or an instance
			SubCallTag=self.sub_symbol.FoundName(sub_className)
			if SubCallTag==-1:
				ClassCallTag=self.class_symbol.FoundName(sub_className)
				if ClassCallTag==-1:
					sub_Name=sub_className+'.'+sub_funcName
				else:
					sub_MethodFlag=True
					sub_className=self.class_symbol.Scope[ClassCallTag][1]
					sub_index=self.class_symbol.Scope[ClassCallTag][3]
					self.vmWriter.writePush('this',sub_index)
					sub_Name=sub_className+'.'+sub_funcName
			else:
				sub_MethodFlag=True
				sub_className=self.sub_symbol.Scope[SubCallTag][1]
				sub_index=self.sub_symbol.Scope[SubCallTag][3]
				self.vmWriter.writePush('local',sub_index)
				sub_Name=sub_className+'.'+sub_funcName
			self.rfile.read(1)
			self.writeXml('symbol','(')
			self.compileExpressionList()
			self.writeXml('symbol',')')
			if sub_MethodFlag:
				self.vmWriter.writeCall(sub_Name,self.expressionListNum+1)
			else:
				self.vmWriter.writeCall(sub_Name,self.expressionListNum)
		elif self.tokenizer.token=='(':
			sub_Name=self.ClassName+'.'+sub_className
			self.writeXml('symbol','(')
			self.vmWriter.writePush('pointer',0)
			self.compileExpressionList()
			self.vmWriter.writeCall(sub_Name,self.expressionListNum+1)
			self.writeXml('symbol',')')

	def compileDo(self):
		self.writeXmlTag('<doStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.subroutineCall()
		self.vmWriter.writePop('temp',0)
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</doStatement>\n')	

	def compileLet(self):
		'''
		If the term on the left of '=' is Array, the order of the VM code is 
		totally different from other conditions. 
		'''
		self.writeXmlTag('<letStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		LetVarName=self.tokenizer.token
		ListSeg=self.checkSymbol(LetVarName)
		self.NextToken()
		temp=self.tokenizer.token
		if temp=='[':
			self.writeArrayPush(LetVarName)
			self.writeXml('symbol',self.tokenizer.token)
			self.compileExpression()
			self.writeXml('symbol',']')
			self.vmWriter.writeArithmetic('add')
			self.NextToken()
			self.writeXml('symbol',self.tokenizer.token)
			self.compileExpression()
			self.vmWriter.writePop('temp',0)
			self.vmWriter.writePop('pointer',1)
			self.vmWriter.writePush('temp',0)
			self.vmWriter.writePop('that',0)
			self.writeXml('symbol',';')
			self.writeXmlTag('</letStatement>\n')	
		elif temp == '=':
			self.writeXml('symbol',self.tokenizer.token)
			self.compileExpression()
			self.vmWriter.writePop(ListSeg[2],ListSeg[3])
			self.writeXml('symbol',';')
			self.writeXmlTag('</letStatement>\n')

	def compileWhile(self):
		self.writeXmlTag('<whileStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		sub_WHILEFLAG=self.WHILEFLAG
		self.WHILEFLAG+=1
		self.vmWriter.writeLabel('WHILE_START'+str(sub_WHILEFLAG))
		#(expression)
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileExpression()
		self.writeXml('symbol',')')
		self.vmWriter.writeArithmetic('not')
		self.vmWriter.writeIf('WHILE_OVER'+str(sub_WHILEFLAG))
		#{statements}
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileStatements()
		self.vmWriter.writeGoto('WHILE_START'+str(sub_WHILEFLAG))
		self.vmWriter.writeLabel('WHILE_OVER'+str(sub_WHILEFLAG))
		self.writeXml('symbol',self.tokenizer.token)	
		self.writeXmlTag('</whileStatement>\n')

	def compileReturn(self):
		self.writeXmlTag('<returnStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		#expression?
		self.NextToken()
		if self.tokenizer.token == ';':
			self.writeXml('symbol',self.tokenizer.token)
			self.vmWriter.writePush('constant',0)
			self.vmWriter.writeReturn()
		else:
			self.moveBack()
			self.compileExpression()
			self.vmWriter.writeReturn()
			self.writeXml('symbol',';')
		self.writeXmlTag('</returnStatement>\n')

	def compileStatements(self):
		self.writeXmlTag('<statements>\n')
		self.NextToken()
		while self.tokenizer.token != '}':
			if self.tokenizer.token =='let':
				self.compileLet()
			elif self.tokenizer.token == 'if':
				self.compileIf()
			elif self.tokenizer.token == 'while':
				self.compileWhile()
			elif self.tokenizer.token == 'do':
				self.compileDo()
			elif self.tokenizer.token == 'return':
				self.compileReturn()
			else:
				print 'Error!'+self.tokenizer.token
				exit()
			self.NextToken()
		self.writeXmlTag('</statements>\n')

	def compileIf(self):
		self.writeXmlTag('<ifStatement>\n')
		sub_IFFLAG=self.IFFLAG
		self.IFFLAG+=1
		self.writeXml('keyword',self.tokenizer.token)
		#(expression)
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileExpression()
		self.writeXml('symbol',')')
		self.vmWriter.writeArithmetic('not')
		self.vmWriter.writeIf('IF_RIGHT'+str(sub_IFFLAG))	
		#{statements}
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileStatements()
		self.writeXml('symbol',self.tokenizer.token)
		#(else {statements})?	
		self.NextToken()
		if self.tokenizer.token=='else':
			self.vmWriter.writeGoto('IF_WRONG'+str(sub_IFFLAG))
			self.vmWriter.writeLabel('IF_RIGHT'+str(sub_IFFLAG))
			self.writeXml('keyword',self.tokenizer.token)
			self.NextToken()
			self.writeXml('symbol',self.tokenizer.token)
			self.compileStatements()
			self.vmWriter.writeLabel('IF_WRONG'+str(sub_IFFLAG))
			self.writeXml('symbol',self.tokenizer.token)
		else:
			self.vmWriter.writeLabel('IF_RIGHT'+str(sub_IFFLAG))
			self.moveBack()
		self.writeXmlTag('</ifStatement>\n')	

	def compileClass(self):
		self.writeXmlTag('<class>\n')
		self.NextToken()
		self.writeXml('keyword',self.tokenizer.token)
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		self.ClassName=self.tokenizer.token
		self.NextToken()
		self.writeXml('keyword',self.tokenizer.token)
		#classVarDec*
		self.NextToken()
		while self.tokenizer.token in ('static','field'):		
			self.compileClassVarDec()
			self.NextToken()
		#subroutineDec*
		while self.tokenizer.token in ('constructor','function','method'):
			self.compileSubroutine()
			self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</class>\n')

	def compileSubroutine(self):
		Subroutine_Flag=''
		self.WHILEFLAG=0
		self.IFFLAG=0
		self.writeXmlTag('<subroutineDec>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.sub_symbol.startSubroutine()
		if self.tokenizer.token =='method':
			self.sub_symbol.Define('this',self.ClassName,'argument')
			Subroutine_Flag='METHOD'
		elif self.tokenizer.token == 'constructor':
			Subroutine_Flag='CONSTRUCTOR'
		else:
			Subroutine_Flag='FUNCTION'
		#(void|type) subroutineName (parameterList)
		self.NextToken()
		self.compileType()
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		#special, to be xxx.yyy
		FunctionName=self.ClassName+'.'+self.tokenizer.token
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileParameterList()
		self.writeXml('symbol',self.tokenizer.token)
		#subroutinBody
		self.writeXmlTag('<subroutineBody>\n')
		#{varDec* statements}
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.NextToken()
		while self.tokenizer.token == 'var':
			self.compileVarDec()
			self.NextToken()
		self.moveBack()
		LclNum=self.sub_symbol.VarCount('var')
		self.vmWriter.writeFunction(FunctionName,LclNum)
		if Subroutine_Flag == 'METHOD':
			self.vmWriter.writePush('argument',0)
			self.vmWriter.writePop('pointer',0)
		elif Subroutine_Flag=='CONSTRUCTOR':
			FieldNum=self.class_symbol.VarCount('field')
			self.vmWriter.writePush('constant',FieldNum)
			self.vmWriter.writeCall('Memory.alloc',1)
			self.vmWriter.writePop('pointer',0)
		self.compileStatements()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</subroutineBody>\n')
		self.writeXmlTag('</subroutineDec>\n')
