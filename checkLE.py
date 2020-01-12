'''
该程序用于检查逻辑表达式是否存在语法错误
'''

exp = '(A&(~B|C))&B|(C&D)'
import re

bra = re.compile(r'[(][^()]*[)]')
dot = re.compile(r'[&|]')
item = re.compile(r'~*[a-zA-Z_]\w*')

def check_one(exp):  #没有括号的情况
	ite = re.compile(r'^~*[a-zA-Z_]\w*$') #匹配单个元素变元的情况
	dot = re.compile(r'[&|]')  #逻辑符号
	val = re.compile(r'~*[01]') #匹配单个元素01的情况
	for item in re.split(dot,exp):
		if not ite.match(item) and not val.match(item):
			return False
	return True



def check(exp):
	bra = re.compile(r'[(][^()]*[)]')  #最里面的括号
	brackets = bra.findall(exp)
	if brackets:  
		for bracket in brackets:
			if not check_one(bracket[1:-1]):
				return False
		exp = bra.sub('R',exp)
		return check(exp)
	else:
		return check_one(exp)


if __name__ == "__main__":
	print(check("(V&I)|~~F"))
