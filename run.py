from AnalizadorLexico import main as lex
from AnalizadorSemantico import main as sem
from GeneradorCodigo import main as cod

def main():
    lex()
    sem()
    cod()

if __name__=="__main__":
    main()