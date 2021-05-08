from enum import Enum


class Tag(Enum):
    '''
   Uma representacao em constante de todos os nomes
   de tokens para a linguagem.
   '''

    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_IF = 1
    KW_ELSE = 2
    # then print e outros n tem no arquivo do professor
    KW_PRINT = 3
    KW_WHILE = 4
    KW_WRITE = 5
    KW_READ = 6
    KW_NUM = 7
    KW_CHAR = 8
    KW_NOT = 9
    KW_OR = 10
    KW_AND = 11
    KW_PROGRAM = 12

    # Operadores
    # ==
    OP_EQ = 13
    # !=
    OP_NE = 14
    # >
    OP_GT = 15
    # <
    OP_LT = 16
    # >=
    OP_GE = 17
    # <=
    OP_LE = 18
    # +
    OP_AD = 19
    # -
    OP_MIN = 20
    # *
    OP_MUL = 21
    # /
    OP_DIV = 22
    # =
    OP_ATRIB = 23

    # Simbolos
    # {
    SMB_OBC = 24
    # }
    SMB_CBC = 25
    # (
    SMB_OPA = 26
    # )
    SMB_CPA = 27
    # ,
    SMB_COM = 28
    # ;
    SMB_SEM = 29

    # Identificador
    ID = 30
    LIT = 31

    # Numeros
    NUM = 32
    NUM_CONST = 33
    CHAR_CONST = 34
