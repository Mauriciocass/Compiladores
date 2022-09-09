def main():
    # Abre el archivo de nombre 'codigo.xxy'.
    f = open('codigo.xxy', 'r')
    code = f.read()
    print(code)

    # Divide el codigo en lineas, para tokenizar linea por linea.
    code = code.split('\n')

    #
    for line in code:
        pass

    # Crea un nuevo archivo de nombre 'codigo.xxz' y escribe lo mismo estaba en el
    # archivo 'codigo.xxy'.
    g = open('codigo.xxz', 'w')

    for l in code:
        g.write(l + '\n')

if __name__=="__main__":
    main()