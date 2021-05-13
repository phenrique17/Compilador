from enum import Enum

class Tag(Enum):
    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_IF = 1
    KW_ELSE = 2
    KW_PRINT = 4
    KW_WHILE = 5
    KW_WRITE = 6
    KW_READ = 7
    KW_NUM = 8
    KW_CHAR = 9
    KW_NOT = 10
    KW_OR = 11
    KW_AND = 12
    KW_PROGRAM = 13

    # Operadores
    # ==
    OP_EQ = 14

    # !=
    OP_NE = 15

    # >
    OP_GT = 16

    # <
    OP_LT = 17

    # >=
    OP_GE = 18

    # <=
    OP_LE = 19

    # +
    OP_AD = 20

    # -
    OP_MIN = 21

    # *
    OP_MUL = 22

    # /
    OP_DIV = 23

    # =
    OP_ATRIB = 24

    # Simbolos
    # {
    SMB_OBC = 25

    # }
    SMB_CBC = 26

    # (
    SMB_OPA = 27

    # )
    SMB_CPA = 28

    # ,
    SMB_COM = 29

    # ;
    SMB_SEM = 30

    # Identificador
    ID = 31
    LIT = 32

    # Numeros
    NUM = 33
    NUM_CONST = 34
    CHAR_CONST = 35
