import pandas as pd

global error
error = False

instrucciones = [
    "[00]", "[01]", "[02]", "[03]", "[04]", "[05]",
    "[06]", "[07]", "[08]", "[09]", "[10]", "[11]",
    "[12]", "[13]", "[14]", "[15]", "[16]", "[20]",
    "[21]", "[22]", "[23]", "[24]", "[25]", "[26]",
    "[27]", "[28]", "[30]", "[31]"
]

operadores = [
    "[07]", "[08]", "[09]", "[10]", "[11]", "[12]"
]

aritmeticos1 = {
    "[03]", "[04]"
}

aritmeticos2 = {
    "[01]", "[02]"
}

aritmeticos = aritmeticos1.union(aritmeticos2)

brackets = {
    "[05]", "[06]"
}

variables = pd.read_csv('referencias.csv')['Value'].to_list()

# Revisa los SI y SINO
def check_20(code):
    global error
    # Revisa que el SI este correctamente estructurado.
    if f'{code[0]}{code[1]}{code[5]}{code[6]}{code[7]}' == '[20][05][06][16][13]' and code[2] in variables and code[4] in variables and code[3] in operadores:
        for x in list(range(0,8)):
            code.pop(0)
        check_code(code)
    else:
        print(f'ERROR: condicion si incorrecta')
        error = True
        # Vaciar pila si hay error.

    if f'{code[0]}' == '[14]':
        code.pop(0)
    else:
        print(f'ERROR: condicion no cerrada')
        error = True

    if f'{code[0]}' == '[21]':
        if f'{code[0]}{code[1]}{code[2]}' == '[21][16][13]':
            for x in list(range(0,3)):
                code.pop(0)
            check_code(code)
        else:
            print(f'ERROR: condicion sino incorrecta')
            error = True

        if f'{code[0]}' == '[14]':
            code.pop(0)
            check_code(code)
        else:
            print(f'ERROR: condicion no cerrada')
            error = True

# Revisa los DESDE y REALIZA
def check_22(code):
    global error

    if f'{code[0]}{code[2]}{code[4]}{code[6]}{code[8]}{code[9]}' == '[22][00][27][00][23][13]' and code[1] in variables:
        for x in list(range(0,10)):
            code.pop(0)
        check_code(code)
    else:
        print(f'ERROR: desde mal creado')
        error = True
        # Vaciar pila si hay error.

    if f'{code[0]}' == '[14]':
        code.pop(0)
    else:
        print(f'ERROR: realiza correspondiente a desde')
        error = True

# Revisa los MIENTRAS y REALIZA
def check_24(code):
    global error
    if f'{code[0]}{code[4]}{code[5]}' == '[24][23][13]' and code[1] in variables and code[2] in operadores and code[3] in variables:
        for x in list(range(0,6)):
            code.pop(0)
        check_code(code)
    else:
        print(f'ERROR: mientras')
        error = True
        # Vaciar pila si hay error.

    if f'{code[0]}' == '[14]':
        code.pop(0)
    else:
        print(f'ERROR: parentesis final de mientras')
        error = True

# Revisa los LEE
def check_25(code):
    if f'{code[0]}{code[2]}' == '[25][15]' and code[1] in variables:
        code.pop(0)
        code.pop(0)
        code.pop(0)
    else:
        print('ERROR: lee mal creado')
        error = True

# Revisa los ESCRIBE
def check_26(code):
    global error
    if f'{code[0]}{code[2]}' == '[26][15]' and code[1] in variables:
        code.pop(0)
        code.pop(0)
        code.pop(0)
    else:
        print('ERROR: escribe mal creado\n' +
        f'{code[0]}{code[1]}{code[2]}')
        error = True
        # Vaciar pila si hay error.

# Revisa el INICIO y FIN
def check_30(code):
    global error
    if f'{code[0]}{code[1]}' == '[30][13]':
        code.pop(0)
        code.pop(0)
        check_code(code)
    else:
        print(f'ERROR: falta inicio')
        error = True

    if len(code) < 2:
        print(f'ERROR: falta fin o parentesis de fin')
        error = True
    elif f'{code[0]}{code[1]}' == '[14][31]':
        code.pop(0)
        code.pop(0)

#Revisa la asignacion de variables
def check_asignacion(code):
    global error
    espera_var = True
    c = 0
    brackets = 0
    code.pop(0)

    if f'{code[0]}' == '[00]':
        code.pop(0)
        while f'{code[0]}' != '[15]':
            c += 1
            if espera_var and f'{code[0]}' in variables:
                code.pop(0)
                espera_var = False
            elif espera_var and f'{code[0]}' in aritmeticos2:
                code.pop(0)
                espera_var = True
            elif not espera_var and f'{code[0]}' in aritmeticos:
                code.pop(0)
                espera_var = True
            elif code[0] == '[05]':
                brackets += 1
                code.pop(0)
            elif code[0] == '[06]':
                brackets -= 1
                code.pop(0)
            else:
                break
    else:
        print('ERROR: Mala asignacion, falta =')

    if espera_var:
        print('ERROR: Asignacion incorrecta')
        error = True

    if f'{code[0]}' == '[15]':
        code.pop(0)
    else:
        print('ERROR: Falta #')
        error = True

def check_code(code):
    global error
    while not error:
        if code is None:
            break
        else:
            try:
                if code[0] == '[20]':
                    check_20(code)
                elif code[0] == '[22]':
                    check_22(code)
                elif code[0] == '[24]':
                    check_24(code)
                elif code[0] == '[25]':
                    check_25(code)
                elif code[0] == '[26]':
                    check_26(code)
                elif code[0] == '[30]':
                    check_30(code)
                elif code[1] == '[31]':
                    break
                elif code[0] in variables:
                    check_asignacion(code)
                elif code[0] == '[14]':
                    break
            except:
                break

    return code

def main():
    global error
    code = open('codigo.xxz', 'r').read().replace('][', ']\n[').split('\n')
    code.pop()

    code = check_code(code)

    if not error:
        print('Felicidades! El codigo no cuenta con errores.')

if __name__=="__main__":
    main()
