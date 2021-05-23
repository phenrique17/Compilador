from tag import Tag
from token import Token

class TS:
    # dicionario: {"chave" : "valor"}
    def __init__(self):
        self.ts = {}

        # Palavras-chave
        self.ts['if'] = Token(Tag.KW_IF, 'if', 0, 0)
        self.ts['else'] = Token(Tag.KW_ELSE, 'else', 0, 0)
        self.ts['print'] = Token(Tag.KW_PRINT, 'print', 0, 0)
        self.ts['while'] = Token(Tag.KW_WHILE, 'while', 0, 0)
        self.ts['write'] = Token(Tag.KW_WRITE, 'write', 0, 0)
        self.ts['read'] = Token(Tag.KW_READ, 'read', 0, 0)
        self.ts['num'] = Token(Tag.KW_NUM, 'num', 0, 0)
        self.ts['char'] = Token(Tag.KW_CHAR, 'char', 0, 0)
        self.ts['not'] = Token(Tag.KW_NOT, 'not', 0, 0)
        self.ts['or'] = Token(Tag.KW_OR, 'or', 0, 0)
        self.ts['and'] = Token(Tag.KW_AND, 'and', 0, 0)
        self.ts['program'] = Token(Tag.KW_PROGRAM, 'program', 0, 0)

        # Operadores
        self.ts['=='] = Token(Tag.OP_EQ, '==', 0, 0)
        self.ts['!='] = Token(Tag.OP_NE, '!=', 0, 0)
        self.ts['>'] = Token(Tag.OP_GT, '>', 0, 0)
        self.ts['<'] = Token(Tag.OP_LT, '<', 0, 0)
        self.ts['>='] = Token(Tag.OP_GE, '>=', 0, 0)
        self.ts['<='] = Token(Tag.OP_LE, '<=', 0, 0)
        self.ts['+'] = Token(Tag.OP_AD, '+', 0, 0)
        self.ts['-'] = Token(Tag.OP_MIN, '-', 0, 0)
        self.ts['*'] = Token(Tag.OP_MUL, '*', 0, 0)
        self.ts['/'] = Token(Tag.OP_DIV, '/', 0, 0)
        self.ts['='] = Token(Tag.OP_ATRIB, '=', 0, 0)

        # Operadores
        self.ts['{'] = Token(Tag.SMB_OBC, '{', 0, 0)
        self.ts['}'] = Token(Tag.SMB_CBC, '}', 0, 0)
        self.ts['('] = Token(Tag.SMB_OPA, '(', 0, 0)
        self.ts[')'] = Token(Tag.SMB_CPA, ')', 0, 0)
        self.ts[','] = Token(Tag.SMB_COM, ',', 0, 0)
        self.ts[';'] = Token(Tag.SMB_SEM, ';', 0, 0)

        # Identificador
        self.ts['id'] = Token(Tag.ID, 'id', 0, 0)
        self.ts['lit'] = Token(Tag.LIT, 'lit', 0, 0)

        # Numeros
        self.ts['num'] = Token(Tag.NUM, 'num', 0, 0)
        self.ts['num_const'] = Token(Tag.NUM_CONST, 'num_const', 0, 0)
        self.ts['char_const'] = Token(Tag.CHAR_CONST, 'char_const', 0, 0)

    def getToken(self, lexema):
        token = self.ts.get(lexema.lower())
        return token

    def updateLineColumn(self, lexema, n_line, n_column):
        token = self.ts.get(lexema.lower())
        token.setColuna(n_column)
        token.setLinha(n_line)

    def addToken(self, lexema, token):
        self.ts[lexema] = token

    def printTS(self):
        for k, t in (self.ts.items()):
            print(k, ":", t.toString(True))
