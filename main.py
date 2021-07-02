from lexer import Lexer
from parser_pasc import Parser

# PAULO HENRIQUE DOS SANTOS - 11722528
# RAFAEL MOREIRA ALMEIDA - 11722680

if __name__ == "__main__":
    lexer = Lexer('prog1.txt')
    parser = Parser(lexer)

    parser.prog()
    parser.lexer.closeFile()

    # token = lexer.proxToken() -> Os tokens estavam sendo chamados daqui

    # print("\n")
    # print("Tabela de simbolos:\n")
    # lexer.printTS()
    # lexer.closeFile()
    # print('\nFim da compilacao\n')
