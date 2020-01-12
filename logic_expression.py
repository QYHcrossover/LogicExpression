import re
from itertools import *
class LogicExpression:
	priority = {'(':4,'~':3,'&':2,'|':1}  #定义符号的优先级
	def __init__(self,expression):
		self.expression = expression.replace(' ','') #初始表达式、并删掉多余空格
		self.vars = self.parse()     #解析后的变量列表
		self.results = self.main()   #最终结果变量

	def parse(self):
		pattern =  re.compile(r'[a-zA-Z_]\w*') #变量规则与代码中变量定义规则相同 字母、数字、下划线组合,数字不能开头
		vars1 = pattern.findall(self.expression)  #解析成变量列表(待去重)
		vars2 = list(set(vars1))  #去重
		vars2.sort(key=vars1.index) #保持原来顺序不变
		return vars2

	def generate(self):
		l = [0,1]
		for case in product(*[l]*len(self.vars)): #case为生成的组合元祖：两个变量的情况下为(0,0) (0,1) (1,0) (1,1)
			exp = self.expression
			for i in range(len(self.vars)):
				exp = exp.replace(self.vars[i],str(case[i]))
			yield exp  #使用python的迭代器依次返回代入值后的表达式

	def operate(self,symbol,*arg):    #不定长参数
		'''
			symbol:逻辑符号 !&|
			arg:逻辑值(不定长)
		'''
		if symbol=='~' and len(arg)==1: # ~的情况
			return not arg[0]
		elif symbol=='&' and len(arg)==2: # &的情况
			return arg[0] and arg[1]
		elif symbol=='|' and len(arg)==2: # |的情况
			return arg[0] or arg[1]
		else:
			raise "operate error"

	def process(self,data,opt):
		'''
			data:逻辑值栈 存放true和false
			opt:符号栈 存放~ & |
		'''
		symbol = opt.pop()
		if symbol == '~':
			logic1 = data.pop()
			data.append(self.operate(symbol,logic1))
			return
		elif symbol in ('&','|'):
			logic1 = data.pop()
			logic2 = data.pop()
			data.append(self.operate(symbol,logic1,logic2))
			return

	def solve(self,exp):
		data = [] #逻辑栈
		opt = [] #操作符号栈
		for i in exp:
			if i.isdigit():           #如果是数字则直接进逻辑栈
				data.append(int(i)==1)
			elif i==')':              #如果是)则依次则开始从data栈和opt计算直到遇到(为止
				while opt[-1]!='(':
					self.process(data,opt)
				opt.pop() #出栈(
			elif not opt or opt[-1] == '(' or self.priority[i]>self.priority[opt[-1]]: #符号进栈的三种情况:符号栈为空、符号栈头为(,ps:(进栈后优先值降为最低、拿到的比栈中的优先级大
				opt.append(i)
			else:                     #优先级低需要先计算达到进栈条件后方能进栈  
				while opt and opt[-1] != '(' and self.priority[i]<self.priority[opt[-1]]: 
					self.process(data,opt)
				opt.append(i)
		while opt:
			self.process(data,opt)
		return data.pop()

	def main(self):
		results = []
		for exp in self.generate():
			results.append(self.solve(exp))
		return results

	@property
	def conclusion(self):
		if False not in self.results:
			return 'True forever'
		elif True not in self.results:
			return 'False forever'
		else:
			return 'Satisfactible'


if __name__ == "__main__":
	le = LogicExpression("p|p&q")
	print(le.vars)
	print(le.results)
	print(le.conclusion)
