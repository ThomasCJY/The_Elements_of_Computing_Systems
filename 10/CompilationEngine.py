#!/usr/bin/python
import JackTokenizer

def compileClass(rfile,wfile):
	wfile.write('<class>\n')
	token=JackTokenizer.advance(rfile)
	while token != '{':
		JackTokenizer.writeToken(wfile,token)
		token=JackTokenizer.advance(rfile)
	wfile.write('<symbol> { </symbol>\n')
	#classVarDec*
	token=JackTokenizer.advance(rfile)
	while token in ('static','field'):
		compileClassVarDec(rfile,wfile,token)
		token=JackTokenizer.advance(rfile)
	#subroutineDec*
	while token in ('constructor','function','method'):
		compileSubroutine(rfile,wfile,token)
		token=JackTokenizer.advance(rfile)
	wfile.write('<symbol> } </symbol>\n')
	wfile.write('</class>\n')

def compileSubroutine(rfile,wfile,tokenAtt):
	wfile.write('<subroutineDec>\n<keyword> '+tokenAtt+' </keyword>\n')
	#(void|type) subroutineName (parameterList)
	token=JackTokenizer.advance(rfile)
	while token != '(':
		JackTokenizer.writeToken(wfile,token)
		token=JackTokenizer.advance(rfile)
	wfile.write('<symbol> ( </symbol>\n')
	compileParameterList(rfile,wfile)
	wfile.write('<symbol> ) </symbol>\n')
	#subroutinBody
	compileSubroutineBody(rfile,wfile)
	wfile.write('</subroutineDec>\n')

def compileSubroutineBody(rfile,wfile):
	wfile.write('<subroutineBody>\n')
	#{varDec* statements}
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	token=JackTokenizer.advance(rfile)
	while token == 'var':
		compileVarDec(rfile,wfile)
		token=JackTokenizer.advance(rfile)
	lennum=-len(token)
	rfile.seek(lennum,1)
	compileStatements(rfile,wfile)
	wfile.write('<symbol> } </symbol>\n')
	wfile.write('</subroutineBody>\n')

def compileClassVarDec(rfile,wfile,tokenAtt):
	wfile.write('<classVarDec>\n<keyword> '+tokenAtt+' </keyword>\n')
	token=JackTokenizer.advance(rfile)
	while token != ';':
		JackTokenizer.writeToken(wfile,token)
		token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	wfile.write('</classVarDec>\n')

def compileParameterList(rfile,wfile):
	wfile.write('<parameterList>\n')
	token=JackTokenizer.advance(rfile)
	while token != ')':
		JackTokenizer.writeToken(wfile,token)
		token=JackTokenizer.advance(rfile)
	wfile.write('</parameterList>\n')

def compileVarDec(rfile,wfile):
	wfile.write('<varDec>\n<keyword> var </keyword>\n')
	token=JackTokenizer.advance(rfile)
	while token != ';':
		JackTokenizer.writeToken(wfile,token)
		token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	wfile.write('</varDec>\n')

def compileExpression(rfile,wfile):
	wfile.write('<expression>\n')
	compileTerm(rfile,wfile)
	token=JackTokenizer.advance(rfile)
	while not (token in (')',']',';',',')):
		JackTokenizer.writeToken(wfile,token)
		compileTerm(rfile,wfile)
		token=JackTokenizer.advance(rfile)
	wfile.write('</expression>\n')	

def compileExpressionList(rfile,wfile):
	wfile.write('<expressionList>\n')
	token=JackTokenizer.advance(rfile)
	if token != ')':
		lennum=-len(token)
		rfile.seek(lennum,1)
	while token != ')':
		compileExpression(rfile,wfile)
		rfile.seek(-1,1)
		token=JackTokenizer.advance(rfile)
		if token == ',':
			wfile.write('<symbol> , </symbol>\n')
	wfile.write('</expressionList>\n')		

def compileTerm(rfile,wfile):
	wfile.write('<term>\n')
	token=JackTokenizer.advance(rfile)
	tType=JackTokenizer.tokenType(token)
	if tType == 'IDENTIFIER':
		temp=rfile.read(1)
		if temp=='.':
			lennum=-len(token)-1
			rfile.seek(lennum,1)
			subroutinCall(rfile,wfile)
		elif temp=='[':
			JackTokenizer.writeToken(wfile,token)
			wfile.write('<symbol> [ </symbol>\n')
			compileExpression(rfile,wfile)
			wfile.write('<symbol> ] </symbol>\n')
		elif temp=='(':
			JackTokenizer.writeToken(wfile,token)
			wfile.write('<symbol> ( </symbol>\n')
			compileExpression(rfile,wfile)
			wfile.write('<symbol> ) </symbol>\n')
		else:
			rfile.seek(-1,1)
			JackTokenizer.writeToken(wfile,token)
	elif token in ('-','~'):
		JackTokenizer.writeToken(wfile,token)
		compileTerm(rfile,wfile)
	elif token == '(':
		wfile.write('<symbol> ( </symbol>\n')
		compileExpression(rfile,wfile)
		wfile.write('<symbol> ) </symbol>\n')
	else:
		JackTokenizer.writeToken(wfile,token)
	wfile.write('</term>\n')

def subroutinCall(rfile,wfile):
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	temp = rfile.read(1)
	if temp=='.':
		wfile.write('<symbol> . </symbol>\n')
		token=JackTokenizer.advance(rfile)
		JackTokenizer.writeToken(wfile,token)
		rfile.read(1)
		wfile.write('<symbol> ( </symbol>\n')
		compileExpressionList(rfile,wfile)
		wfile.write('<symbol> ) </symbol>\n')
	elif temp=='(':
		wfile.write('<symbol> ( </symbol>\n')
		compileExpressionList(rfile,wfile)
		wfile.write('<symbol> ) </symbol>\n')

def compileStatements(rfile,wfile):
	wfile.write('<statements>\n')
	token=JackTokenizer.advance(rfile)
	while token != '}':
		if token=='let':
			compileLet(rfile,wfile)
		elif token == 'if':
			compileIf(rfile,wfile)
		elif token == 'while':
			compileWhile(rfile,wfile)
		elif token == 'do':
			compileDo(rfile,wfile)
		elif token == 'return':
			compileReturn(rfile,wfile)
		else:
			print 'Error!'+token
			exit()
		token=JackTokenizer.advance(rfile)
	wfile.write('</statements>\n')

def compileDo(rfile,wfile):
	wfile.write('<doStatement>\n')
	wfile.write('<keyword> do </keyword>\n')
	subroutinCall(rfile,wfile)
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)	
	wfile.write('</doStatement>\n')	

def compileLet(rfile,wfile):
	wfile.write('<letStatement>\n')
	wfile.write('<keyword> let </keyword>\n')
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	temp=JackTokenizer.advance(rfile)
	if temp=='[':
		wfile.write('<symbol> [ </symbol>\n')
		compileExpression(rfile,wfile)
		wfile.write('<symbol> ] </symbol>\n')
		token=JackTokenizer.advance(rfile)
		JackTokenizer.writeToken(wfile,token)
	elif temp == '=':
		wfile.write('<symbol> = </symbol>\n')
	compileExpression(rfile,wfile)
	wfile.write('<symbol> ; </symbol>\n')
	wfile.write('</letStatement>\n')

def compileIf(rfile,wfile):
	wfile.write('<ifStatement>\n')
	wfile.write('<keyword> if </keyword>\n')
	#(expression)
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	compileExpression(rfile,wfile)
	wfile.write('<symbol> ) </symbol>\n')
	#{statements}
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	compileStatements(rfile,wfile)
	wfile.write('<symbol> } </symbol>\n')
	#(else {statements})?	
	token=JackTokenizer.advance(rfile)
	if token=='else':
		JackTokenizer.writeToken(wfile,token)
		token=JackTokenizer.advance(rfile)
		JackTokenizer.writeToken(wfile,token)
		compileStatements(rfile,wfile)
		wfile.write('<symbol> } </symbol>\n')	
	else:
		lennum=-len(token)
		rfile.seek(lennum,1)
	wfile.write('</ifStatement>\n')	

def compileWhile(rfile,wfile):
	wfile.write('<whileStatement>\n')
	wfile.write('<keyword> while </keyword>\n')
	#(expression)
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	compileExpression(rfile,wfile)
	wfile.write('<symbol> ) </symbol>\n')
	#{statements}
	token=JackTokenizer.advance(rfile)
	JackTokenizer.writeToken(wfile,token)
	compileStatements(rfile,wfile)
	wfile.write('<symbol> } </symbol>\n')		
	wfile.write('</whileStatement>\n')

def compileReturn(rfile,wfile):
	wfile.write('<returnStatement>\n')
	wfile.write('<keyword> return </keyword>\n')
	#expression?
	token=JackTokenizer.advance(rfile)
	if token == ';':
		JackTokenizer.writeToken(wfile,token)
	else:
		lennum= -len(token)
		rfile.seek(lennum,1)
		compileExpression(rfile,wfile)
		wfile.write('<symbol> ; </symbol>\n')
	wfile.write('</returnStatement>\n')	