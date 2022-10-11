from os import popen
from numpy import var
import pandas as pd

instrucciones = [
    "[00]", "[01]", "[02]", "[03]", "[04]", "[05]",
    "[06]", "[07]", "[08]", "[09]", "[10]", "[11]",
    "[12]", "[13]", "[14]", "[15]", "[16]", "[20]",
    "[21]", "[22]", "[23]", "[24]", "[25]", "[26]",
    "[27]", "[28]", "[30]", "[31]"
]

variables = pd.read_csv('referencias.csv')['Value'].to_list()

# Revisa los SI y SINO
def check_20(code):
    print('20')
    pass

# Revisa los DESDE y REALIZA
def check_22(code):
    print('22')
    if f'{code[0]}' == '[14]':
        code.pop(0)
    elif f'{code[0]}{code[2]}{code[4]}{code[6]}{code[8]}{code[9]}' == '[22][00][27][00][23][13]' and code[1] in variables:
        for x in list(range(0,10)):
            code.pop(0)
        check_code(code)
    else:
        print(f'ERROR en {code[0]}{code[1]}')
        code.pop(0)
        code.pop(0)

# Revisa los MIENTRAS y REALIZA
def check_24(code):
    pass

# Revisa los LEE
def check_25(code):
    print('25')
    if f'{code[0]}{code[2]}' == '[25][15]' and code[1] in variables:
        code.pop(0)
        code.pop(0)
        code.pop(0)
    else:
        print('ERROR! in line:\n' +
        f'{code[0]}{code[1]}{code[2]}')

# Revisa los ESCRIBE
def check_26(code):
    print('26')
    if f'{code[0]}{code[2]}' == '[26][15]' and code[1] in variables:
        code.pop(0)
        code.pop(0)
        code.pop(0)
    else:
        print('ERROR! in line:\n' +
        f'{code[0]}{code[1]}{code[2]}')

# Revisa el INICIO y FIN
def check_30(code):
    print('30')
    if f'{code[0]}{code[1]}' == '[30][13]':
        code.pop(0)
        code.pop(0)
        check_code(code)
    elif f'{code[0]}{code[1]}' == '[14][31]':
        code.pop(0)
        code.pop(0)
    else:
        print(f'ERROR en {code[0]}{code[1]}')
        code.pop(0)
        code.pop(0)


def check_code(code):
    while len(code) > 0:
        print(code)
        if code[0] == '[20]':
            check_20(code)
        elif code[0] == '[22]' or (code[0] == '[14]' and len(code) > 2):
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
            print(f'ERROR en {code[0]}')

def main():
    code = open('codigo.xxz', 'r').read().replace('][', ']\n[').split('\n')

    check_code(code)
    print(code)
    print('ANALIZADO')

if __name__=="__main__":
    main()