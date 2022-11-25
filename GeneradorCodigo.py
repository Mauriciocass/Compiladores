import pandas as pd
import numpy as np

variables = pd.read_csv('referencias.csv').to_numpy()
variables = np.delete(variables, 0, 1)

contEti = 0
printETI = 0
etiquetas = []
result = ""

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
    global result
    result += '\njmp inicio:\n'
    print('\njmp inicio:')
    for variable in variables:
            temp1 = variable[1].replace("[","").replace("]","")
            temp2 = variable[0]
            result += f'    {temp1} {temp2}\n'
            print(f'    {temp1} {temp2}')

    result += '\ninicio:\n'
    print('\ninicio:')

# Asignacion
def asignacion(code):
    global result
    destiny = code.pop(0)
    tempCode = []

    code.pop(0)

    while code[0] != '[15]':
        tempCode.append(code.pop(0))
    code.pop(0)

    tempCode = posfija(tempCode)
    result += f'    mov {destiny}, ax\n'
    print(f'    mov {destiny}, ax')

    switch(code)

# Convierte una linea de codigo lee a codigo ensamblador
def lee(code):
    global result
    code.pop(0)

    result += '    mov ax, 01\n'
    print('    mov ax, 01')

    result += f'    mov dx, {code[0]}\n'
    print(f'    mov dx, {code.pop(0)}')

    result += f'    mov cx, 2\n'
    print(f'    mov cx, 2')

    result += f'    int 21H\n'
    print(f'    int 21H')
    code.pop(0)

# Convierte una linea de codigo escribe a codigo ensamblador
def escribe(code):
    global result
    code.pop(0)

    result += '    mov ax, 02\n'
    print('    mov ax, 02')

    result += f'    mov dx, {code[0]}\n'
    print(f'    mov dx, {code.pop(0)}')
    code.pop(0)

    result += f'    mov cx, 2'
    print(f'    mov cx, 2')

    result += f'    int 21H\n'
    print(f'    int 21H')

# Convierte una expresion infija a una posfija e imprime las instrucciones en ensamblador
def posfija(expresion):
    global result
    operator = ['[01]', '[02]', '[03]', '[04]']
    prec = {'[01]':1, '[02]':1, '[03]':2, '[04]':2, '[05]':0, '[06]':0}

    postfix = []
    stack = []

    if len(expresion) == 1:
        result += f'    mov ax, {expresion[-1]}\n'
        print(f'    mov ax, {expresion.pop()}')
    else:
        for x in expresion:
            if x not in operator and x != '[05]' and x != '[06]':
                result += f'    mov ax, {x}\n'
                print(f'    mov ax, {x}')

                result += f'    push ax\n'
                print(f'    push ax')
                postfix.append(x)

            elif x == '[05]':
                stack.append(x)
            elif x == '[06]':
                while stack[-1]!= '[05]':
                    result += f'    pop bx\n'
                    print(f'    pop bx')

                    result += f'    pop ax\n'
                    print(f'    pop ax')

                    if(stack[-1] == '[01]'):
                        result += '    add ax, bx\n'
                        print('    add ax, bx')

                    elif(stack[-1] == '[02]'):
                        result += '    sub ax, bx\n'
                        print('    sub ax, bx')

                    elif(stack[-1] == '[03]'):
                        result += '    mul ax, bx\n'
                        print('    mul ax, bx')

                    elif(stack[-1] == '[04]'):
                        result += '    div ax, bx\n'
                        print('    div ax, bx')

                    print('    push ax')

                    postfix.append(stack.pop())
                    if len(stack) != 0:
                        result += '    push ax\n'
                        print('    push ax')
                stack.pop()

            else:
                while len(stack) != 0 and prec[x] <= prec[stack[-1]]:
                    result += f'    pop bx\n'
                    print(f'    pop bx')

                    result += f'    pop ax\n'
                    print(f'    pop ax')

                    if(stack[-1] == '[01]'):
                        result += '    add ax, bx\n'
                        print('    add ax, bx')

                    elif(stack[-1] == '[02]'):
                        result += '    sub ax, bx\n'
                        print('    sub ax, bx')

                    elif(stack[-1] == '[03]'):
                        result += '    mul ax, bx\n'
                        print('    mul ax, bx')

                    elif(stack[-1] == '[04]'):
                        result += '    div ax, bx\n'
                        print('    div ax, bx')

                    postfix.append(stack.pop())

                    if len(stack) != 0:
                        result += '    push ax\n'
                        print('    push ax')

                    print('    push ax')

                stack.append(x)

        while len(stack) != 0:
            result += f'    pop bx\n'
            print(f'    pop bx')

            result += f'    pop ax\n'
            print(f'    pop ax')

            if(stack[-1] == '[01]'):
                result += '    add ax, bx\n'
                print('    add ax, bx')

            elif(stack[-1] == '[02]'):
                result += '    sub ax, bx\n'
                print('    sub ax, bx')

            elif(stack[-1] == '[03]'):
                result += '    mul ax, bx\n'
                print('    mul ax, bx')

            elif(stack[-1] == '[04]'):
                result += '    div ax, bx\n'
                print('    div ax, bx')

            postfix.append(stack.pop())
            if len(stack) != 0:
                result += '    push ax\n'
                print('    push ax')

    return postfix

# Convierte la expresion del si a codigo ensamblador
def assemblySi(code):
    global contEti
    global printETI
    global result
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

    result += f'    mov ax, {tempCode[2]}\n'
    print(f'    mov ax, {tempCode[2]}')

    result += f'    mov ax, {tempCode[4]}\n'
    print(f'    mov bx, {tempCode[4]}')

    result += f'    cmp ax, bx\n'
    print(f'    cmp ax, bx')

    result += f'    {jumps[tempCode[3]]} ETI{contEti}\n'
    print(f'    {jumps[tempCode[3]]} ETI{contEti}')
    contEti += 1

    result += f'    jmp ETI{contEti}\n'
    print(f'    jmp ETI{contEti}')
    contEti += 1

    result += f'\nETI{printETI}:\n'
    print(f'\nETI{printETI}:')
    printETI += 1
    switch(tempCode[8:-1])

    if code[0] == '[21]':
        result += f'    jmp ETI{contEti}:\n'
        print(f'    jmp ETI{contEti}:')
        contEti += 1
        assemblySino(code)

        result += f'\nETI{printETI}:\n'
        print(f'\nETI{printETI}:')
        printETI += 1
    else:
        result += f'\nETI{printETI}:\n'
        print(f'\nETI{printETI}:')
        printETI += 1

# Convierte la expresion del sino a codigo ensamblador
def assemblySino(code):
    global printETI
    global result
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

    result += f'\nETI{printETI}:\n'
    print(f'\nETI{printETI}:')
    printETI += 1
    switch(tempCode[3:-1])

# Convierte la expresion del mientras a codigo ensamblador
# Corregir
def assemblyMientras(code):
    global contEti
    global printETI
    global result
    jumps = {'[07]':'je', '[08]':'jne', '[09]':'jg', '[10]':'jge', '[11]':'jl', '[12]':'jle',}

    tempCode = []
    brackets = 0
    # Este codigo revisa el inicio y fin del desde, para mandar solo eso a la funcion que crea el codigo de si.
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

    result += f'    mov ax, {tempCode[1]}\n'
    print(f'    mov ax, {tempCode[1]}')

    result += f'    mov ax, {tempCode[3]}\n'
    print(f'    mov bx, {tempCode[3]}')

    result += f'    cmp ax, bx\n'
    print(f'    cmp ax, bx')

    result += f'    {jumps[tempCode[2]]} ETI{contEti}\n'
    print(f'    {jumps[tempCode[2]]} ETI{contEti}')
    contEti += 1

    result += f'    jmp ETI{contEti}\n'
    print(f'    jmp ETI{contEti}')
    contEti += 1

    result += f'\nETI{printETI}:\n'
    print(f'\nETI{printETI}:')
    printETI += 1
    switch(tempCode[6:-1])

    result += f'    mov ax, {tempCode[1]}\n'
    print(f'    mov ax, {tempCode[1]}')

    result += f'    mov ax, {tempCode[3]}\n'
    print(f'    mov bx, {tempCode[3]}')

    result += f'    cmp ax, bx\n'
    print(f'    cmp ax, bx')

    result += f'    {jumps[tempCode[2]]} ETI{contEti-2}\n'
    print(f'    {jumps[tempCode[2]]} ETI{contEti-2}')
    contEti += 1

    result += f'    jmp ETI{contEti-2}\n'
    print(f'    jmp ETI{contEti-2}')
    contEti += 1

    result += f'\nETI{printETI}:\n'
    print(f'\nETI{printETI}:')
    printETI += 1

# Convierte la expresion de desde a codigo ensamblador
def assemblyDesde(code):
    global contEti
    global printETI
    global result

    tempCode = []
    brackets = 0
    # Este codigo revisa el inicio y fin del desde, para mandar solo eso a la funcion que crea el codigo de si.
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

    result += f'\nETI{printETI}:\n'
    print(f'\nETI{printETI}:')
    printETI += 1
    switch(tempCode[10:-1])

    result += f'    mov ax, {tempCode[1]}\n'
    print(f'    mov ax, {tempCode[1]}')

    result += '    add ax, 1\n'
    print('    add ax, 1')

    result += f'    mov {tempCode[1]}, ax\n'
    print(f'    mov {tempCode[1]}, ax')

    result += f'    mov bx, {tempCode[7]}\n'
    print(f'    mov bx, {tempCode[7]}')

    result += f'    cmp ax, bx\n'
    print(f'    cmp ax, bx')

    result += f'    jle ETI{contEti}\n'
    print(f'    jle ETI{contEti}')
    contEti += 1
    contEti += 1

    result += f'\nETI{printETI}:\n'
    print(f'\nETI{printETI}:')
    printETI += 1

# Decide que otra funcion debe usarse dependiendo de la funcion que se vaya a convertir a ensamblador
def switch(code):
    try:
        # Si hay un si se va a la funcion para imprimir el si
        if code[0] == '[20]':
            assemblySi(code)
        # Hace el codigo para las asignaciones
        elif code[0] in variables:
            asignacion(code)
        # Hace el codigo para lee
        elif code[0] == '[25]':
            lee(code)
        # Hace el codigo para escribe
        elif code[0] == '[26]':
            escribe(code)
        # Hace el codigo para desde
        elif code[0] == '[22]':
            assemblyDesde(code)
        # Hace el codigo para mientra
        elif code[0] == '[24]':
            assemblyMientras(code)
    except:
        pass

def main():
    global contEti
    global result
    assemblyVariables()
    code = cargarCodigo()
    while len(code) > 0:
        switch(code)

    result += '\n    int 20H'
    print('\n    int 20H')

    #print(result)

if __name__=="__main__":
    main()