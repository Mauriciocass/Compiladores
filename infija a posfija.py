# Expression 1
# infija: 5 + 3 * 8
# posfija: 5 3 8 * +

# Expresion 2
# infija: 7 * 2 - 4
# posfija: 7 2 * 4 -

# Expresion 3
# infija: 7 * ( ( 2 - 4 ) + 8 * 10 )
# posfija: 7 2 4 - 8 10 * + *

# Expresion 4
# infija: 7 * ( 2 - 4 )
# posfija: 7 2 4 - *

operator = ['+', '-', '*', '/']
prec = {'+':1, '-':1, '*':2, '/':2, '(':0, ')':0}

expression = '7 * ( ( 2 - 4 ) + 8 * 10 )'

postfix = []
stack = []

for x in expression.split():
    if x not in operator and x != '(' and x != ')':
        postfix += x
    elif x == '(':
        stack.append(x)
    elif x == ')':
        while stack[-1]!= '(':
            postfix += stack.pop()
        stack.pop()
    else:
        while len(stack) != 0 and prec[x] <= prec[stack[-1]]:
            postfix += stack.pop()
        stack.append(x)

while len(stack) != 0:
    postfix += stack.pop()

#print(expression.split())
print(postfix)
