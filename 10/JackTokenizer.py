#!/usr/bin/python
STable=('{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~')
KWtable=('class','constructor','function','method','field','static','var','int','char','boolean',\
	'void','true','false','null','this','let','do','if','else','while','return')


def hasMoreTokens(token):
	if not token:
		return 0
	else:
		return 1

def advance(rfile):
	token=''
	temp=rfile.read(1)
	while temp==' ' or temp =='\n' or temp =='\t':
		temp = rfile.read(1)
	if not temp:
		return ''
	elif temp.isalpha() or temp.isdigit() or temp == '_':
		while temp.isalpha() or temp.isdigit() or temp == '_':
			token+=temp
			temp=rfile.read(1)
		if temp in STable or temp =='"':
			rfile.seek(-1,1)
			return token
		elif temp == ' ' or temp == '\n':
			rfile.seek(-1,1)
			return token
	elif temp in STable:
		return temp
	elif temp =='"':
		token += '"'
		temp=rfile.read(1)
		while temp != '"':
			token+=temp
			temp=rfile.read(1)
		token+='"'
		return token

def tokenType(token):
	if token in KWtable:
		return 'KEYWORD'
	elif token in STable:
		return 'SYMBOL'
	elif token.isdigit():
		return 'INT_CONSTANT'
	elif token.startswith('"'):
		return 'STRING_CONSTANT'
	else:
		return 'IDENTIFIER'


def writeToken(wfile,token):
	tType=tokenType(token)
	if tType == 'KEYWORD':
		wfile.write('<keyword> '+token+' </keyword>\n')
	elif tType == 'SYMBOL':
		if token=='>':
			wfile.write('<symbol> &gt; </symbol>\n')
		elif token=='<':
			wfile.write('<symbol> &lt; </symbol>\n')
		elif token=='&':
			wfile.write('<symbol> &amp; </symbol>\n')
		else:
			wfile.write('<symbol> '+token+' </symbol>\n')
	elif tType == 'IDENTIFIER':
		wfile.write('<identifier> '+token+' </identifier>\n')
	elif tType == 'INT_CONSTANT':
		wfile.write('<integerConstant> '+token+' </integerConstant>\n')
	elif tType == 'STRING_CONSTANT':
		wfile.write('<stringConstant> '+token.strip('"')+' </stringConstant>\n')