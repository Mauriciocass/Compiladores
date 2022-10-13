import pandas as pd

instrucciones = [
    "[00]", "[01]", "[02]", "[03]", "[04]", "[05]",
    "[06]", "[07]", "[08]", "[09]", "[10]", "[11]",
    "[12]", "[13]", "[14]", "[15]", "[16]", "[20]",
    "[21]", "[22]", "[23]", "[24]", "[25]", "[26]",
    "[27]", "[28]", "[30]", "[31]"
]

operadores = [
    "[06]", "[07]", "[08]", "[09]", "[10]", "[11]", "[12]"
]

variables = pd.read_csv('referencias.csv')['Value'].to_list()

# Revisa los SI y SINO
def check_20(code):
    print('revisa SI')

    # Revisa que el SI este correctamente estructurado.
    if f'{code[0]}{code[1]}{code[5]}{code[6]}{code[7]}' == '[20][05][06][16][13]' and code[2] in variables and code[4] in variables and code[3] in operadores:
        for x in list(range(0,8)):
            code.pop(0)
        check_code(code)
    else:
        print(f'ERROR en {code[0]}{code[1]}')
        code = []
        # Vaciar pila si hay error.

    if f'{code[0]}' == '[14]':
        code.pop(0)
    else:
        print(f'ERROR en {code[0]}')
        code = []

    print('revisa SINO')
    if f'{code[0]}' == '[21]':
        if f'{code[0]}{code[1]}{code[2]}' == '[21][16][13]':
            for x in list(range(0,3)):
                code.pop(0)
            check_code(code)
        else:
            print(f'ERROR en {code[0]}')
            code = []

        if f'{code[0]}' == '[14]':
            code.pop(0)
            check_code(code)
        else:
            print(f'ERROR en {code[0]}')
            code = []

# Revisa los DESDE y REALIZA
def check_22(code):
    print('revisa DESDE y REALIZA')

    if f'{code[0]}{code[2]}{code[4]}{code[6]}{code[8]}{code[9]}' == '[22][00][27][00][23][13]' and code[1] in variables:
        for x in list(range(0,10)):
            code.pop(0)
        check_code(code)
    else:
        print(f'DESDE y REALIZA')
        print(f'ERROR en {code[0]}{code[1]}')
        code = []
        # Vaciar pila si hay error.

    if f'{code[0]}' == '[14]':
        code.pop(0)
    else:
        print(f'DESDE y REALIZA 2')
        print(f'ERROR en {code[0]}')
        code = []

# Revisa los MIENTRAS y REALIZA
def check_24(code):
    pass

# Revisa los LEE
def check_25(code):
    print('revisa LEE')
    if f'{code[0]}{code[2]}' == '[25][15]' and code[1] in variables:
        code.pop(0)
        code.pop(0)
        code.pop(0)
    else:
        print(f'LEE')
        print('ERROR! in line:\n' +
        f'{code[0]}{code[1]}{code[2]}')
        code = []

# Revisa los ESCRIBE
def check_26(code):
    print('revisa ESCRIBE')
    if f'{code[0]}{code[2]}' == '[26][15]' and code[1] in variables:
        code.pop(0)
        code.pop(0)
        code.pop(0)
    else:
        print(f'ESCRIBE')
        print('ERROR! in line:\n' +
        f'{code[0]}{code[1]}{code[2]}')
        code = []
        # Vaciar pila si hay error.

# Revisa el INICIO y FIN
def check_30(code):
    print('revisa INICIO y FIN')
    if f'{code[0]}{code[1]}' == '[30][13]':
        code.pop(0)
        code.pop(0)
        check_code(code)
    elif f'{code[0]}{code[1]}' == '[14][31]':
        code.pop(0)
        code.pop(0)
    else:
        print(f'INICIO y FIN')
        print(f'ERROR en {code[0]}{code[1]}')
        code = []

def check_code(code):
    print(code)
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
    elif len(code) == 1 or code[0] == '':
        print('El codigo se termino de analizar')
    elif code[0] == '[30]' or code[1] == '[31]':
        check_30(code)
    else:
        print(f'CHECK CODE')
        print(f'ERROR en {code[0]}')
        code = []
    return code

def main():
    code = open('codigo.xxz', 'r').read().replace('][', ']\n[').split('\n')

    while len(code) > 1:
        code = check_code(code)

    print(code)
    print('ANALIZADO')

if __name__=="__main__":
    main()
