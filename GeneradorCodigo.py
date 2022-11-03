import pandas as pd
import numpy as np

variables = pd.read_csv('referencias.csv').to_numpy()

variables = np.delete(variables, 0, 1)

contEti = 0
printETI = 0
etiquetas = []

# Carga el codigo del archivo .xxz y lo regresa como lista de tokens
def cargarCodigo():
    code = open('codigo.xxz', 'r').read().replace('][', ']\n[').split('\n')
    code.pop()
    code.pop()
    code.pop()
    code.pop(0)
    code.pop(0)
    return code

# Imprime todas las variables que se tienen en la tabla de referencias
def assemblyVariables():
    print('\njmp inicio:')
    for variable in variables:
            temp1 = variable[1].replace("[","").replace("]","")
            temp2 = variable[0]
            print(f'    {temp1} {temp2}')

    print('\ninicio:')

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

# Convierte una expresion infija a una posfija e imprime las instrucciones en ensamblador
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

def assemblySi(code):
    global contEti
    global printETI
    jumps = {'[07]':'je', '[08]':'jne', '[09]':'jg', '[10]':'jge', '[11]':'jl', '[12]':'jle',}

    tempCode = []
    brackets = 0
    # Este codigo revisa el inicio y fin del si, para mandar solo eso a la funcion que crea el codigo de si.
    for x in code:
        if x == '[13]':
            tempCode.append(x)
            brackets += 1
        elif x == '[14]':
            tempCode.append(x)
            brackets -= 1
            if brackets == 0:
                break
        else:
            tempCode.append(x)
    # Quita todo el codigo que fue impreso en el si anteriormente
    for x in tempCode:
            code.remove(x)

    print(f'    mov ax, {tempCode[2]}')
    print(f'    mov bx, {tempCode[4]}')
    print(f'    cmp ax, bx')

    print(f'    {jumps[tempCode[3]]} ETI{contEti}')
    contEti += 1
    print(f'    jmp ETI{contEti}')
    contEti += 1

    print(f'\nETI{printETI}')
    printETI += 1
    switch(tempCode[8:-1])

    if(code[0] == '[21]'):
        print(f'    jmp ETI{contEti}')
        assemblySino(code)
        print(f'\nETI{contEti}:')
    else:
        print(f'\nETI{printETI}:')
        printETI += 1

def assemblySino(code):
    global printETI
    tempCode = []
    brackets = 0
    # Este codigo revisa el inicio y fin del sino, para mandar solo eso a la funcion que crea el codigo de sino.
    for x in code:
        if x == '[13]':
            tempCode.append(x)
            brackets += 1
        elif x == '[14]':
            tempCode.append(x)
            brackets -= 1
            if brackets == 0:
                break
        else:
            tempCode.append(x)

    # Quita todo el codigo que fue impreso en el sino anteriormente
    for x in tempCode:
            code.remove(x)

    print(f'\nETI{printETI:}')
    printETI += 1
    switch(tempCode[3:-1])

def switch(code):
    try:
        # Si hay un si se va a la funcion para imprimir el si
        if(code[0] == '[20]'):
            assemblySi(code)
        # Hace el codigo para las asignaciones
        elif code[0] in variables:
            asignacion(code)
    except:
        pass

def main():
    global contEti
    assemblyVariables()
    code = cargarCodigo()

    while len(code) > 0:
        switch(code)

    print('\n    int 20H')

if __name__=="__main__":
    main()