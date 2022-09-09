# Abre el archivo de nombre 'codigo.xxy', lo lee y lo imprime.
f = open('codigo.xxy', 'r')
code = f.read()
print(code)

# Crea un nuevo archivo de nombre 'codigo.xxz' y escribe lo mismo estaba en el
# archivo 'codigo.xxy'.
g = open('codigo.xxz', 'w')
g.write(code)