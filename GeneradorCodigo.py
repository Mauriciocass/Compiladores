import pandas as pd
import numpy as np
from binarytree import Node

variables = pd.read_csv('referencias.csv').to_numpy()

variables = np.delete(variables, 0, 1)

contEti = 0
etiquetas = 0

# Imprime todas las variables que se tienen en la tabla de referencias
def assemblyVariables():
    for variable in variables:
            temp1 = variable[1].replace("[","").replace("]","")
            temp2 = variable[0]
            print(f'    {temp1} {temp2}')

# Imprime la condicion del si
def assemblySi(code):
    global contEti
    global etiquetas
    print(f'    mov ax, {code[2]}')
    print(f'    mov bx, {code[4]}')
    print(f'    cmp ax, bx')

    # ==
    if(code[3] == '[07]'):
        print(f'    je ETI{contEti}')
    # <>
    elif(code[3] == '[08]'):
        print(f'    jne ETI{contEti}')
    # >
    elif(code[3] == '[09]'):
        print(f'    jg ETI{contEti}')
    # >=
    elif(code[3] == '[10]'):
        print(f'    jge ETI{contEti}')
    # <
    elif(code[3] == '[11]'):
        print(f'    jl ETI{contEti}')
    # <=
    elif(code[3] == '[12]'):
        print(f'    jle ETI{contEti}')

'''
    contEti += 1
    print(f'    jmp ETI{contEti}')
    contEti += 1

    for x in list(range(0, 7)):
        code.pop(0)

    ifContent(code)

def ifContent(code):
    global contEti
    global etiquetas

    print(f'\nETI{etiquetas}')
    etiquetas += 1
    print(f'    jmp ETI{etiquetas}')
'''
# Asignacion
def asignacion(code):
    destiny = code.pop(0)
    tempCode = []

    code.pop(0)

    while code[0] != '[15]':
        tempCode.append(code.pop(0))
    code.pop(0)

    tempCode = posfija(tempCode)
    print(f'    mov {destiny}, ax')

# Convirte una expresion infija a una posfija
def posfija(expresion):
    operator = ['[01]', '[02]', '[03]', '[04]']
    prec = {'[01]':1, '[02]':1, '[03]':2, '[04]':2, '[05]':0, '[06]':0}

    postfix = []
    stack = []

    for x in expresion:
        if x not in operator and x != '[05]' and x != '[06]':
            print(f'    move ax, {x}')
            print(f'    push ax')
            postfix.append(x)
        elif x == '[05]':
            stack.append(x)
        elif x == '[06]':
            while stack[-1]!= '[05]':
                print(f'    pop bx')
                print(f'    pop ax')
                if(stack[-1] == '[01]'):
                    print('    add ax, bx')
                elif(stack[-1] == '[02]'):
                    print('    sub ax, bx')
                elif(stack[-1] == '[03]'):
                    print('    mul ax, bx')
                elif(stack[-1] == '[04]'):
                    print('    div ax, bx')
                postfix.append(stack.pop())
                if len(stack) != 0:
                    print('    push ax')
            stack.pop()
        else:
            while len(stack) != 0 and prec[x] <= prec[stack[-1]]:
                print(f'    pop bx')
                print(f'    pop ax')
                if(stack[-1] == '[01]'):
                    print('    add ax, bx')
                elif(stack[-1] == '[02]'):
                    print('    sub ax, bx')
                elif(stack[-1] == '[03]'):
                    print('    mul ax, bx')
                elif(stack[-1] == '[04]'):
                    print('    div ax, bx')
                postfix.append(stack.pop())
                if len(stack) != 0:
                    print('    push ax')
            stack.append(x)

    while len(stack) != 0:
        print(f'    pop bx')
        print(f'    pop ax')
        if(stack[-1] == '[01]'):
            print('    add ax, bx')
        elif(stack[-1] == '[02]'):
            print('    sub ax, bx')
        elif(stack[-1] == '[03]'):
            print('    mul ax, bx')
        elif(stack[-1] == '[04]'):
            print('    div ax, bx')
        postfix.append(stack.pop())
        if len(stack) != 0:
            print('    push ax')

    return postfix

def main():
    print('\njmp inicio')
    assemblyVariables()
    print('\ninicio')

    code = open('codigo.xxz', 'r').read().replace('][', ']\n[').split('\n')
    code.pop()
    code.pop()
    code.pop()
    code.pop(0)
    code.pop(0)

    if(code[0] == '[20]'):
        assemblySi(code)
    elif code[0] in variables:
        asignacion(code)

    print('    int 20H')

    # print(code)

if __name__=="__main__":
    main()
