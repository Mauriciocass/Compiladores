# Trabajo de compiladores
Fecha de Creacion: 09/07/2022 <br>
Fecha de Ultima Modificacion: 11/03/2022 <br>

Autores:
- Roberto Gonzalez
- Mauricio Nuñez
- Ilian Chavez
- German Morales
- Armando Perez 

Contenido:
- <b>AnalizadorLexico.py</b> :<br>
    Es el analizador lexico del compilador, se encarga de tokenizar el codigo que se encuentre escrito en el archivo 'codigo.xxy' si este no tiene ningun error. Si no encuentra ningun error, entonces los tokens se escriben en el archivo 'codigo.xxz' y los valores de los tokens de las variables y constantes se guardan en el archivo 'referencias.csv'.
- <b>AnalizadorSemantico.py</b> :<br>
    Es el analizador semantico del compilador, se encarga de revisar que la gramatica del codigo sea correcta. Revisa el codigo que esta en el archivo 'codigo.xxz' e indica si ha habido un error. Cabe mencionar que solo correra hasta que encuentre un error y en ese error dejara de analizar el resto del archivo, porque solo puede detectar entre uno o dos errores cada vez que se corre.
- <b>codigo.xxy</b> :<br>
    Es el archivo de codigo escrito por el usuario y que despues se tokenizara.
- <b>codigo.xxz</b> :<br>
    Es el archivo de codigo ya tokenizado que se usara por el analizador semantico.
- <b>GeneradorCodigo.py</b> :<br>
    Este archivo genera el codigo, de nuestro lenguaje personalizado a assembly.
- <b>referencias.csv</b> :<br>
    Es el archivo con las variables y constantes que fueron referenciadas en el codigo del archivo 'codigo.xxy'.
- <b>run.py</b> :<br>
    Para facilitar correr los dos analizadores se creo 'run.py', que corre los archivos 'AnalizadorLexico.py' y 'AnalizadorSemantico.py' en secuencia, pues es necesarios que se corra el analizador lexico si se le hizo un cambio al archivo 'codigo.xxy'.
