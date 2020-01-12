from flask import Flask,render_template,request
import json
from logic_expression import *
from checkLE import check

def withAddition(expression,addition):
	for add in addition.split(';'):
		key,value = add.split('=')
		expression = expression.replace(key,value)
	return expression

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
	if request.method == 'POST':
		expression = request.form.get('expression')
		if not check(expression):
			return render_template("index.html",form=request.form,aaa=False)
		addition = request.form.get('addition')
		if addition:
			expression = withAddition(expression,addition)
		le = LogicExpression(expression)
		varss,results,conclusion = le.vars,le.results,le.conclusion
		logic_table = tuple(product(*[[0,1]]*len(varss)))
		return render_template("index.html",form=request.form,logic_table=logic_table,varss=varss,results=results,conclusion=conclusion,aaa=True)
	else:
		return render_template("index.html",form={},aaa=True)

if __name__ == "__main__":
	app.run(debug=True)