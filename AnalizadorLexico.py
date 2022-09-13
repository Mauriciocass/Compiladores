from curses.ascii import isupper
from dataclasses import replace
from distutils.log import error
import re
import pandas as pd

reservadas = {"=": "[00]", "+": "[01]", "-": "[02]", "*": "[03]", "/": "[04]",
    "(": "[05]", ")": "[06]", "==": "[07]", "<>": "[08]", ">": "[09]",
    ">=": "[10]", "<": "[11]", "<=": "[12]", "[": "[13]", "]": "[14]",
    "#": "[15]", ":": "[16]", "si": "[20]", "sino": "[21]", "desde": "[22]",
    "realiza": "[23]", "mientras": "[24]", "lee": "[25]", "escribe": "[26]",
    "hasta": "[27]", "//": "[28]", "inicio": "[30]", "fin": "[31]"
}

tokens = {}

def main():
    # Crea un nuevo archivo de nombre 'codigo.xxz' y escribe lo mismo estaba en
    # el archivo 'codigo.xxy'.
    f = open('codigo.xxy', 'r').read()

    # Numero en el que empiezan las referencias de la tabla de referencias.
    x = 100
    # Bandera que nos sirve para saber si existe algun error, por default es
    # false.
    error = False
    # Contador de la linea en la que el analizador esta en el momento.
    linea = 0

    # Variable de codigo temporal, si el proceso es exitoso se guardara en el
    # archivo con extension ".xxz".
    temp_code = ""

    # Busca los strings constantes en el codigo y los tokeniza individualmente.
    while re.search('"(.*)"', f) is not None:
            temp = re.search('"(.*)"', f).group(0)
            f = f.replace(temp, f'[{x}]')
            tokens[temp] = f'{[x]}'
            x += 1

    f = f.replace('#', ' #')
    f = f.replace(':', ' :')
    f = f.replace('(', ' (')
    f = f.replace(')', ' )')
    f = f.replace('+', ' + ')
    f = f.replace('-', ' - ')
    f = f.replace('*', ' * ')

    # Pasa por el codigo linea por linea y tokeniza.
    for l in f.split('\n'):
        linea += 1
        if '//' not in l:
            for s in l.split():
                if s in reservadas.keys():
                    s = reservadas.get(s)
                else:
                    if s in tokens:
                        s = tokens.get(s)
                    elif s in tokens.values():
                        pass
                    else:
                        # Checa cada letra de los tokens que todavia no se han
                        # tokenizado, si alguno tiene mayuscula, marca error.
                        for n in s:
                            if n.isupper():
                                error = True
                                print(f'Error en linea {linea}')
                                break
                        tokens[s] = f'{[x]}'
                        s = tokens.get(s)
                    x += 1
                temp_code += s
            temp_code += '\n'

    # Hace un DataFrame de los tokens de variables y constantes, con sus
    # valores.
    df = pd.DataFrame(
        {
            "Token": tokens.keys(),
            "Value": tokens.values()
        }
    )

    df.to_csv('referencias.csv')

    # Si no hubo error, se crea un archivo con extension ".xxz".
    if not error:
        g = open('codigo.xxz', 'w')
        g.write(temp_code)

if __name__=="__main__":
    main()
