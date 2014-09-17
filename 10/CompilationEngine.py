#!/usr/bin/python
import JackTokenizer

class Compile():
	def __init__(self,rfile,wfile):
		self.rfile=rfile
		self.wfile=wfile
		self.tokenizer=JackTokenizer.Tokenizer(self.rfile)

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
		else:
			pass

	def moveBack(self):
		lennum=-len(self.tokenizer.token)
		self.rfile.seek(lennum,1)

	def compileType(self):
		tType=self.tokenizer.tokenType()
		if tType == 'KEYWORD':
			self.writeXml('keyword',self.tokenizer.token)
		elif tType == 'SYMBOL':
			if self.tokenizer.token=='>':
				self.writeXml('symbol','&gt')
			elif self.tokenizer.token=='<':
				self.writeXml('symbol','&lt')
			elif self.tokenizer.token=='&':
				self.writeXml('symbol','&amp')
			else:
				self.writeXml('symbol',self.tokenizer.token)
		elif tType == 'IDENTIFIER':
			self.writeXml('identifier',self.tokenizer.token)
		elif tType == 'INT_CONSTANT':
			self.writeXml('integerConstant',self.tokenizer.token)
		elif tType == 'STRING_CONSTANT':
			self.writeXml('stringConstant',self.tokenizer.token.strip('"'))

	def compileVarDec(self):
		'''
		var type varName(,'varName')*;
		'''
		self.writeXmlTag('<varDec>\n')
		self.writeXml('keyword','var')
		#type
		self.NextToken()
		self.compileType()
		#varName
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		#(,varName)*
		self.NextToken()
		while self.tokenizer.token != ';':
			self.writeXml('symbol',self.tokenizer.token)
			self.NextToken()
			self.writeXml('identifier',self.tokenizer.token)
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
			if self.tokenizer.token != ',':
				self.compileType()
				self.NextToken()
				self.writeXml('identifier',self.tokenizer.token)
				self.NextToken()
			else:
				self.writeXml('symbol',self.tokenizer.token)
				self.NextToken()
				self.compileType()
				self.NextToken()
				self.writeXml('identifier',self.tokenizer.token)
				self.NextToken()				
		self.writeXmlTag('/<parameterList>\n')

	def compileClassVarDec(self):
		'''
		('static'|'field') type varName(, varName)*;
		'''
		self.writeXmlTag('<classVarDec>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.NextToken()
		self.compileType()
		#varName
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		#(,varName)*
		self.NextToken()
		while self.tokenizer.token != ';':
			self.writeXml('symbol',self.tokenizer.token)
			self.NextToken()
			self.writeXml('identifier',self.tokenizer.token)
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
				self.subroutinCall()
			elif temp=='[':
				self.writeXml('identifier',self.tokenizer.token)
				self.writeXml('symbol','[')
				self.compileExpression()
				self.writeXml('symbol',']')
			else:
				self.rfile.seek(-1,1)
				self.writeXml('identifier',self.tokenizer.token)
		elif self.tokenizer.token in ('-','~'):
			self.writeXml('symbol',self.tokenizer.token)
			self.compileTerm()
		elif self.tokenizer.token == '(':
			self.writeXml('symbol',self.tokenizer.token)
			self.compileExpression()
			self.writeXml('symbol',')')
		else:
			self.compileType()
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

			self.writeXml('symbol', self.tokenizer.token)
			self.compileTerm()
			self.NextToken()

		self.writeXmlTag('</expression>\n')	

	def compileExpressionList(self):
		self.writeXmlTag('<expressionList>\n')
		self.NextToken()
		while self.tokenizer.token != ')':
			if self.tokenizer.token != ',':
				self.moveBack()
				self.compileExpression()
			else:
				self.writeXml('symbol',self.tokenizer.token)
				self.compileExpression()	
		self.writeXmlTag('</expressionList>\n')

	def subroutinCall(self):
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		self.NextToken()
		if self.tokenizer.token=='.':
			self.writeXml('symbol',self.tokenizer.token)
			self.NextToken()
			self.writeXml('identifier',self.tokenizer.token)
			self.rfile.read(1)
			self.writeXml('symbol','(')
			self.compileExpressionList()
			self.writeXml('symbol',')')
		elif self.tokenizer.token=='(':
			self.writeXml('symbol','(')
			self.compileExpressionList()
			self.writeXml('symbol',')')

	def compileDo(self):
		self.writeXmlTag('<doStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.subroutinCall()
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</doStatement>\n')	

	def compileLet(self):
		self.writeXmlTag('<letStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		self.NextToken()
		temp=self.tokenizer.token
		if temp=='[':
			self.writeXml('symbol',self.tokenizer.token)
			self.compileExpression()
			self.writeXml('symbol',']')
			self.NextToken()
			self.writeXml('symbol',self.tokenizer.token)
		elif temp == '=':
			self.writeXml('symbol',self.tokenizer.token)
		self.compileExpression()
		self.writeXml('symbol',';')
		self.writeXmlTag('</letStatement>\n')

	def compileWhile(self):
		self.writeXmlTag('<whileStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		#(expression)
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileExpression()
		self.writeXml('symbol',')')
		#{statements}
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileStatements()
		self.writeXml('symbol',self.tokenizer.token)	
		self.writeXmlTag('</whileStatement>\n')

	def compileReturn(self):
		self.writeXmlTag('<returnStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		#expression?
		self.NextToken()
		if self.tokenizer.token == ';':
			self.writeXml('symbol',self.tokenizer.token)
		else:
			self.moveBack()
			self.compileExpression()
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
				print 'Error!'+token
				exit()
			self.NextToken()
		self.writeXmlTag('</statements>\n')

	def compileIf(self):
		self.writeXmlTag('<ifStatement>\n')
		self.writeXml('keyword',self.tokenizer.token)
		#(expression)
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileExpression()
		self.writeXml('symbol',')')
		#{statements}
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileStatements()
		self.writeXml('symbol',self.tokenizer.token)
		#(else {statements})?	
		self.NextToken()
		if self.tokenizer.token=='else':
			self.writeXml('keyword',self.tokenizer.token)
			self.NextToken()
			self.writeXml('symbol',self.tokenizer.token)
			self.compileStatements()
			self.writeXml('symbol',self.tokenizer.token)
		else:
			self.moveBack()
		self.writeXmlTag('</ifStatement>\n')	

	def compileClass(self):
		self.writeXmlTag('<class>\n')
		self.NextToken()
		self.writeXml('keyword',self.tokenizer.token)
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
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
		self.writeXmlTag('<subroutineDec>\n')
		self.writeXml('keyword',self.tokenizer.token)
		#(void|type) subroutineName (parameterList)
		self.NextToken()
		self.compileType()
		self.NextToken()
		self.writeXml('identifier',self.tokenizer.token)
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.compileParameterList()
		self.writeXml('symbol',self.tokenizer.token)
		#subroutinBody
		self.compileSubroutineBody()
		self.writeXmlTag('</subroutineDec>\n')

	def compileSubroutineBody(self):
		self.writeXmlTag('<subroutineBody>\n')
		#{varDec* statements}
		self.NextToken()
		self.writeXml('symbol',self.tokenizer.token)
		self.NextToken()
		while self.tokenizer.token == 'var':
			self.compileVarDec()
			self.NextToken()
		self.moveBack()
		self.compileStatements()
		self.writeXml('symbol',self.tokenizer.token)
		self.writeXmlTag('</subroutineBody>\n')