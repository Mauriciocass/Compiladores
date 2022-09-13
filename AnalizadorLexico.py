from dataclasses import replace
import re
#Catga el documento
f = open('codigo.xxy', 'r')
code = f.read()
#Se eliminan los comentarios despues de //
def stripComments(code):
    return re.sub(r'(?m)^ *//.*\n?', '', code)

def main():
    # Abre el archivo de nombre 'codigo.xxy'.
    f = open('codigo.xxy', 'r')
    code = f.read()

    # Tokeniza las palabras 'sino' y 'si'. En este orden estrictamente, pues
    # 'sino' contiene 'si'.
    code = code.replace('sino', '{21}')
    code = code.replace('si', '{20}')

    # Tokeniza las palabras 'lee' y 'escribe'.
    code = code.replace('lee', '{25}')
    code = code.replace('escribe', '{26}')

    # Tokeniza las palabras 'desde', 'realiza', 'mientras' y 'hasta'.
    code = code.replace('desde', '{22}')
    code = code.replace('realiza', '{23}')
    code = code.replace('meintras', '{24}')
    code = code.replace('hasta', '{27}')

    # Tokeniza las palabras 'inicio' y 'final'.
    code = code.replace('inicio', '{30}')
    code = code.replace('fin', '{31}')

    # Tokeniza los operandos '==', '<>', '>=', '<=', '>', '<' en ese orden.
    code = code.replace('==', '{07}')
    code = code.replace('<>', '{08}')
    code = code.replace('>=', '{10}')
    code = code.replace('<=', '{12}')
    code = code.replace('>', '{09}')
    code = code.replace('<', '{11}')

    # Tokeniza simbolos '[', ']', '+', '-', '*', '/', '=', '(', ')', ':', '#'.
    code = code.replace('[', '{13}')
    code = code.replace(']', '{14}')
    code = code.replace('+', '{01}')
    code = code.replace('-', '{02}')
    code = code.replace('*', '{03}')
    code = code.replace('/', '{04}')
    code = code.replace('=', '{00}')
    code = code.replace('(', '{05}')
    code = code.replace(')', '{06}')
    code = code.replace(':', '{16}')
    code = code.replace('#', '{15}')

    # Cambia los simbolos de '{' y '}' a '[' y ']' respectivamente.
    code = code.replace('{', '[')
    code = code.replace('}', ']')

    # Divide el codigo en lineas, para tokenizar linea por linea.
    code = code.split('\n')

    # Crea un nuevo archivo de nombre 'codigo.xxz' y escribe lo mismo estaba en
    # el archivo 'codigo.xxy'.
    g = open('codigo.xxz', 'w')

    # Cada linea se agrega al nuevo archivo individualmente.
    for l in code:
        g.write(l + '\n')

if __name__=="__main__":
    main()
print(stripComments(code))
