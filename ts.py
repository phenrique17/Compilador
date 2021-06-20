from tag import Tag
from token import Token

class TS:
    # dicionario: {"chave" : "valor"}
    def __init__(self):
        self.ts = {}

        # Palavras-chave
        self.ts['if'] = Token(Tag.KW_IF, 'if')
        self.ts['else'] = Token(Tag.KW_ELSE, 'else')
        self.ts['print'] = Token(Tag.KW_PRINT, 'print')
        self.ts['while'] = Token(Tag.KW_WHILE, 'while')
        self.ts['write'] = Token(Tag.KW_WRITE, 'write')
        self.ts['read'] = Token(Tag.KW_READ, 'read')
        self.ts['num'] = Token(Tag.KW_NUM, 'num')
        self.ts['char'] = Token(Tag.KW_CHAR, 'char')
        self.ts['not'] = Token(Tag.KW_NOT, 'not')
        self.ts['or'] = Token(Tag.KW_OR, 'or')
        self.ts['and'] = Token(Tag.KW_AND, 'and')
        self.ts['program'] = Token(Tag.KW_PROGRAM, 'program')

        # Operadores
        self.ts['=='] = Token(Tag.OP_EQ, '==')
        self.ts['!='] = Token(Tag.OP_NE, '!=')
        self.ts['>'] = Token(Tag.OP_GT, '>')
        self.ts['<'] = Token(Tag.OP_LT, '<')
        self.ts['>='] = Token(Tag.OP_GE, '>=')
        self.ts['<='] = Token(Tag.OP_LE, '<=')
        self.ts['+'] = Token(Tag.OP_AD, '+')
        self.ts['-'] = Token(Tag.OP_MIN, '-')
        self.ts['*'] = Token(Tag.OP_MUL, '*')
        self.ts['/'] = Token(Tag.OP_DIV, '/')
        self.ts['='] = Token(Tag.OP_ATRIB, '=')

        # Operadores
        self.ts['{'] = Token(Tag.SMB_OBC, '{')
        self.ts['}'] = Token(Tag.SMB_CBC, '}')
        self.ts['('] = Token(Tag.SMB_OPA, '(')
        self.ts[')'] = Token(Tag.SMB_CPA, ')')
        self.ts[','] = Token(Tag.SMB_COM, ',')
        self.ts[';'] = Token(Tag.SMB_SEM, ';')

        # Identificador
        self.ts['id'] = Token(Tag.ID, 'id')
        self.ts['lit'] = Token(Tag.LIT, 'lit')

        # Numeros
        self.ts['num'] = Token(Tag.NUM, 'num')
        self.ts['num_const'] = Token(Tag.NUM_CONST, 'num_const')
        self.ts['char_const'] = Token(Tag.CHAR_CONST, 'char_const')

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
