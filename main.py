from tag import Tag
from token import Token
from lexer import Lexer
from parser import Parser

# PAULO HENRIQUE DOS SANTOS - 11722528
# RAFAEL MOREIRA ALMEIDA - 11722680

if __name__ == "__main__":
    lexer = Lexer('prog1.txt')
    parser = Parser(lexer)
    parser.Programa()
    parser.lexer.closeFile()

    print("\nLista de tokens:")
    token = lexer.proxToken()

    while token is not None:
        print(token.toString(), "Linha: " + str(token.getLinha()) + " Coluna: " + str(token.getColuna()))

        if token.getNome() == Tag.EOF:
            break

        token = lexer.proxToken()

    print("\n")
    

    print("Tabela de simbolos:\n")
    
    lexer.printTS()
    lexer.closeFile()
    
    print('\nFim da compilacao\n')
