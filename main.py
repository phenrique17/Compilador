from tag import Tag
from token import Token
from lexer import Lexer

if __name__ == "__main__":
    lexer = Lexer('prog1.txt')

    print("\nLista de tokens:\n")

    token = lexer.proxToken()

    while token is not None:
        if token == '':
            token = lexer.proxToken()
            continue
        print(token.toString(), "Linha: " + str(token.getLinha()) + " Coluna: " + str(token.getColuna()))
        # Imprimindo reconhecimento do fim do arquivo
        if token.getNome() == Tag.EOF:
            break
        token = lexer.proxToken()

    # print("\nTabela de simbolos:\n")
    # lexer.printTS()
    # lexer.closeFile()
    # print('\nFim da compilacao\n')
