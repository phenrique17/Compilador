import sys

from ts import TS
from tag import Tag
from token import Token

class Lexer:
    def __init__(self, input_file):
        try:
            self.input_file = open(input_file, 'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 0
            self.ts = TS()
            self.totalErros = 0
        except IOError:
            print('Erro de abertura do arquivo. Encerrando.')
            sys.exit(0)

    def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro ao fechar arquivo. Encerrando.')
            sys.exit(0)

    def sinalizaErroLexico(self, message):
        self.totalErros = self.totalErros + 1
        print("[Erro Lexico]: ", message, "\n")

    def retornaPonteiro(self):
        if self.lookahead.decode('ascii') != '':
            self.input_file.seek(self.input_file.tell() - 1)
        self.n_column = self.n_column - 1

    def printTS(self):
        self.ts.printTS()

    def proxToken(self):
        estado = 1
        lexema = ""
        c = '\u0000'

        while True:
            self.lookahead = self.input_file.read(1)
            c = self.lookahead.decode('ascii') # caractere lido
            self.n_column = self.n_column + 1

            if estado == 1:
                if c == '':
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
                elif c == ' ' or c == '\t' or c == '\n' or c == '\r':
                    estado = 1
                    if c == '\n':
                        self.n_line = self.n_line + 1
                        self.n_column = 0
                    if c == '\t':
                        self.n_column = self.n_column + 3
                elif c == '=':
                    estado = 2
                elif c == '!':
                    estado = 4
                elif c == '<':
                    estado = 6
                elif c == '>':
                    estado = 9
                elif c.isdigit(): # Verificando se é um número
                    lexema += c
                    estado = 12
                elif c.isalpha(): # Verificando se é uma letra
                    lexema += c
                    estado = 14
                elif c == '/':
                    estado = 16
                elif c == '+':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.OP_AD, "+", self.n_line, self.n_column)
                elif c == '*':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.OP_MUL, "*", self.n_line, self.n_column)
                elif c == '-':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)
                elif c == '{':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)
                elif c == '}':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)
                elif c == ';':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)
                elif c == ',':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)
                elif c == '(':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)
                elif c == ')':
                    self.ts.updateLineColumn(c, self.n_line, self.n_column)
                    return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)
                elif c == '"':
                    estado = 21
                else:
                    lexema += c
                    self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " + str(self.n_line) + " e coluna " + str(self.n_column))
                    if self.totalErros == 3:
                        return None
                    else:
                        estado = 1
                        lexema = ""
                        c = '\u0000'
                        continue
            elif estado == 2:
                if c == '=':
                    self.ts.updateLineColumn("==", self.n_line, self.n_column)
                    return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)
                else:
                    self.retornaPonteiro()
                    self.ts.updateLineColumn("=", self.n_line, self.n_column)
                    return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
            elif estado == 4:
                if c == '=':
                    self.ts.updateLineColumn("!=", self.n_line, self.n_column)
                    return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)

                self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " + str(self.n_line) + " e coluna " + str(self.n_column))
                self.retornaPonteiro()

                if self.totalErros == 3:
                    return None
                else:
                    estado = 1
                    lexema = ""
                    c = '\u0000'
                    continue
            elif estado == 6:
                if c == '=':
                    self.ts.updateLineColumn("<=", self.n_line, self.n_column)
                    return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)

                self.retornaPonteiro()
                self.ts.updateLineColumn("<", self.n_line, self.n_column)
                return Token(Tag.OP_LT, "<", self.n_line, self.n_column)
            elif estado == 9:
                if c == '=':
                    self.ts.updateLineColumn(">=", self.n_line, self.n_column)
                    return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)

                self.retornaPonteiro()
                self.ts.updateLineColumn(">", self.n_line, self.n_column)
                return Token(Tag.OP_GT, ">", self.n_line, self.n_column)
            elif estado == 12:
                if c.isdigit():
                    lexema += c
                elif c == '.':
                    lexema += c
                    estado = 20
                else:
                    self.retornaPonteiro()
                    return Token(Tag.NUM, lexema, self.n_line, self.n_column)
            elif estado == 14:
                if c.isalnum(): # Verificando se é um número ou uma letra
                    lexema += c
                else:
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema)

                    if token is None:
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    else:
                        token.setColuna(self.n_column)
                        token.setLinha(self.n_line)
                        self.ts.updateLineColumn(lexema, self.n_line, self.n_column)

                    return token
            elif estado == 16:
                if c == '/':
                    estado = 17
                elif c == '*':
                    estado = 18
                else:
                    self.retornaPonteiro()
                    self.ts.updateLineColumn("/", self.n_line, self.n_column)
                    return Token(Tag.OP_DIV, '/', self.n_line, self.n_column)
            elif estado == 17:
                if c == '\n':
                    self.n_line = self.n_line + 1
                    self.n_column = 0
                    estado = 1
                elif c == '\t':
                    self.n_column = self.n_column + 3
                elif c == '':
                    self.ts.updateLineColumn("EOF", self.n_line, self.n_column)
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif estado == 18:
                if c == '*':
                    estado = 19
                elif c == '\n':
                    self.n_line = self.n_line + 1
                    self.n_column = 1
                elif c == '':
                    self.ts.updateLineColumn("EOF", self.n_line, self.n_column)
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column - 1)
            elif estado == 19:
                if c == '/':
                    estado = 1
                elif c == '\t':
                    self.n_column = self.n_column + 3
                else:
                    estado = 18
            elif estado == 20:
                if c.isdigit():
                    lexema += c
                else:
                    self.retornaPonteiro()
                    return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)
            elif estado == 21:
                if c == '"':
                    return Token(Tag.CHAR_CONST, lexema, self.n_line, self.n_column)
                elif c == '\n':
                    self.sinalizaErroLexico("Caractere invalido [quebra de linha] na linha " + str(self.n_line) + " e coluna " + str(self.n_column))

                    if self.totalErros == 3:
                        return None
                    else:
                        self.n_line = self.n_line + 1
                        estado = 1
                        lexema = ""
                        c = '\u0000'
                        continue
                elif c == '':
                    coluna = self.n_column
                    self.n_column = 0
                    return Token(Tag.CHAR_CONST, lexema, self.n_line, coluna)
                elif c == '\t':
                    self.n_column = self.n_column + 3
                lexema += c
            # fim if's de estados
        # fim while
