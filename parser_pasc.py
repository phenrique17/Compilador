import sys
import copy

from tag import Tag
from token import Token
from lexer import Lexer
from nao_terminal import NaoTerminal

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken()
        self.erros = 0

        if self.token is None:
            sys.exit(0)

    def sinalizaErroSemantico(self, message):
        print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
        print(message, "\n")

    def sinalizaErroSintatico(self, message):
        print("\n")
        print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
        print(message, "\n")

    def advance(self):
        print("[DEBUG] token: ", self.token.toString())
        self.token = self.lexer.proxToken()
        if self.token is None:
            sys.exit(0)

    def eat(self, t):
        if (self.token.getNome() == t):
            self.advance()
            return True
        else:
            return False

    def skip(self, message):
        self.sinalizaErroSintatico(message)
        self.erros += 1
        if self.erros == 5:
            print("[LIMITE DE ERROS ALCANÇADO]")
            sys.exit(0)

    #======================================================================================

    def prog(self):
        if (not self.eat(Tag.KW_PROGRAM)):
            self.skip("Esperado 'program'")
        if (not self.eat(Tag.ID)):
            self.skip("Esperado 'id'")
        self.body()

    def body(self):
        self.declList()

        if(not self.eat(Tag.SMB_OBC)):
            self.skip("Esperado '{'")

        self.stmtList()

        if (not self.eat(Tag.SMB_CBC)):
            self.skip("Esperado '}'")

    def declList(self):
        # Duvida!!! no 'KW_NUM'
        if(self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR):
            self.decl()

            if (not self.eat(Tag.SMB_SEM)):
                self.skip("Esperado ';'")

            self.declList()
        elif(self.token.getNome() == Tag.SMB_OBC):
            return
        else:
            self.skip("Esperado 'palavra-chave' ou '{'")

    def decl(self):
        self.type()
        self.idList()

    def type(self):
        if(self.token.getNome() == Tag.KW_NUM):
            self.advance()
        elif(self.token.getNome() == Tag.KW_CHAR):
            self.advance()
        else:
            self.skip("Esperado uma palavra-chave 'num' ou 'char'")

    def idList(self):
        if (not self.eat(Tag.ID)):
            self.skip("Esperado 'id'")

        self.idListLinha()

    def idListLinha(self):
        if(self.token.getNome() == Tag.SMB_COM):
            self.advance()
            self.idList()
        elif(self.token.getNome() == Tag.SMB_SEM):
            return
        else:
            self.skip("Esperado ',' ou ';'")

    def stmtList(self):
        if(self.token.getNome() in [Tag.ID, Tag.KW_IF, Tag.KW_READ, Tag.KW_WRITE, Tag.KW_WHILE]):
            self.stmt()

            if (not self.eat(Tag.SMB_SEM)):
                self.skip("Esperado ';'")

            self.stmtList()
        elif(self.token.getNome() == Tag.SMB_CBC):
            return
        else:
            self.skip("Esperado 'id' ou '}'")

    def stmt(self):
        if(self.token.getNome() == Tag.ID):
            self.assignStmt()
        elif(self.token.getNome() == Tag.KW_IF):
            self.ifStmt()
        elif(self.token.getNome() == Tag.KW_WHILE):
            self.whileStmt()
        elif(self.token.getNome() == Tag.KW_READ):
            self.readStmt()
        elif(self.token.getNome() == Tag.KW_WRITE):
            self.writeStmt()
        else:
            self.skip("Esperado uma 'palavra-chave'")

    def assignStmt(self):
        if (not self.eat(Tag.ID)):
            self.skip("Esperado 'id'")

        if (not self.eat(Tag.OP_ATRIB)):
            self.skip("Esperado '='")

        self.simpleExpr()

    def ifStmt(self):
        if(not self.eat(Tag.KW_IF)):
            self.skip("Esperado 'if'")

        if(not self.eat(Tag.SMB_OPA)):
            self.skip("Esperado '('")

        self.expression()

        if(not self.eat(Tag.SMB_CPA)):
            self.skip("Esperado ')'")

        if(not self.eat(Tag.SMB_OBC)):
            self.skip("Esperado '{'")

        self.stmtList()

        if(not self.eat(Tag.SMB_CBC)):
            self.skip("Esperado '}'")

        self.ifStmtLinha()

    def ifStmtLinha(self):
        if(self.token.getNome() == Tag.KW_ELSE):
            self.advance()

            if(not self.eat(Tag.SMB_OBC)):
                self.skip("Esperado '{'")

            self.stmtList()

            if(not self.eat(Tag.SMB_CBC)):
                self.skip("Esperado '}'")
        elif(self.token.getNome() == Tag.SMB_SEM):
            return
        else:
            self.skip("Esperado 'palavra-chave' ou ';'")

    def whileStmt(self):
        self.stmtPrefix()

        if (not self.eat(Tag.SMB_OBC)):
            self.skip("Esperado '{'")

        self.stmtList()

        if (not self.eat(Tag.SMB_CBC)):
            self.skip("Esperado '}'")

    def stmtPrefix(self):
        if (not self.eat(Tag.KW_WHILE)):
            self.skip("Esperado 'while'")

        if (not self.eat(Tag.SMB_OPA)):
            self.skip("Esperado '('")

        self.expression()

        if (not self.eat(Tag.SMB_CPA)):
            self.skip("Esperado ')'")

    def readStmt(self):
        if (not self.eat(Tag.KW_READ)):
            self.skip("Esperado 'read'")

        if (not self.eat(Tag.ID)):
            self.skip("Esperado 'id'")

    def writeStmt(self):
        if (not self.eat(Tag.KW_WRITE)):
            self.skip("Esperado 'write'")

        self.simpleExpr()

    def expression(self):
        self.simpleExpr()
        self.expressionLinha()

    def expressionLinha(self):
        if(self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND):
            self.logop()
            self.simpleExpr()
            self.expressionLinha()
        elif(self.token.getNome() == Tag.SMB_CPA):
            return
        else:
            self.skip("Esperado 'palavra-chave' ou ')'")

    def simpleExpr(self):
        self.term()
        self.simpleExprLinha()

    def simpleExprLinha(self):
        lis_token_1 = [Tag.OP_EQ, Tag.OP_GT, Tag.OP_GE, Tag.OP_LT, Tag.OP_LE, Tag.OP_NE]
        lis_token_2 = [Tag.SMB_SEM, Tag.SMB_CPA, Tag.KW_AND, Tag.KW_OR]

        if(self.token.getNome() in lis_token_1):
            self.relop()
            self.term()
            self.simpleExprLinha()
        elif(self.token.getNome() in lis_token_2):
            return
        else:
            self.skip("Esperado 'operador', 'simbolo' ou 'palavra-chave'")

    def term(self):
        self.factorB()
        self.termLinha()

    def termLinha(self):
        lista = [Tag.OP_EQ,Tag.OP_GT,Tag.OP_GE,Tag.OP_LT,Tag.OP_LE,Tag.OP_NE,Tag.KW_AND,Tag.KW_OR,Tag.SMB_SEM,Tag.SMB_CPA]

        if(self.token.getNome() == Tag.OP_MIN or self.token.getNome() == Tag.OP_AD):
            self.addop()
            self.factorB()
            self.termLinha()
        elif(self.token.getNome() in lista):
            return
        else:
            self.skip("Esperado 'operador', 'simbolo' ou 'palavra-chave'")

    def factorB(self):
        self.factorA()
        self.factorBLinha()

    def factorBLinha(self):
        lista = [Tag.SMB_SEM, Tag.SMB_CPA, Tag.KW_OR, Tag.KW_AND, Tag.OP_EQ, Tag.OP_GT, Tag.OP_GE, Tag.OP_LT, Tag.OP_LE, Tag.OP_NE, Tag.OP_AD, Tag.OP_MIN]

        if(self.token.getNome() == Tag.OP_MUL or self.token.getNome() == Tag.OP_DIV):
            self.mulop()
            self.factorA()
            self.factorBLinha()
        elif(self.token.getNome() in lista):
            return
        else:
            self.skip("Esperado 'operador'")

    def factorA(self):
        lista = [Tag.ID, Tag.SMB_OPA, Tag.NUM, Tag.NUM_CONST, Tag.CHAR_CONST]

        if(self.token.getNome() == Tag.KW_NOT):
            self.advance()
            self.factor()
        else:
            self.factor()
        '''
        if(self.token.getNome() in lista):
            self.factor()
        elif(self.token.getNome() == Tag.KW_NOT):
            self.factor()
        else:
            self.skip("Esperado 'id', '(', 'numérico' ou 'not'")
        '''

    def factor(self):
        if(self.token.getNome() == Tag.ID):
            self.advance()
        elif(self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.CHAR_CONST):
            self.constant()
        elif(self.token.getNome() == Tag.SMB_OPA):
            self.advance()
            self.expression()

            if (not self.eat(Tag.SMB_CPA)):
                self.skip("Esperado ')'")
        else:
            self.skip("Esperado 'id', 'numérico' ou '('")

    def logop(self):
        if(self.token.getNome() == Tag.KW_OR):
            self.advance()
        elif(self.token.getNome() == Tag.KW_AND):
            self.advance()
        else:
            self.skip("Esperado 'or' ou 'and'")

    def relop(self):
        lista = [Tag.OP_EQ,Tag.OP_GT,Tag.OP_GE,Tag.OP_LT,Tag.OP_LE,Tag.OP_NE]

        if(self.token.getNome() in lista):
            self.advance()
        else:
            self.skip("Esperado 'operador'")

    def addop(self):
        if(self.token.getNome() == Tag.OP_AD):
            self.advance()
        elif(self.token.getNome() == Tag.OP_MIN):
            self.advance()
        else:
            self.skip("Esperado '+' ou '-'")

    def mulop(self):
        if(self.token.getNome() == Tag.OP_MUL):
            self.advance()
        elif(self.token.getNome() == Tag.OP_DIV):
            self.advance()
        else:
            self.skip("Esperado '*' ou '/'")

    def constant(self):
        if(self.token.getNome() == Tag.NUM_CONST):
            self.advance()
        elif(self.token.getNome() == Tag.CHAR_CONST):
            self.advance()
        else:
            self.skip("Esperado 'numérico'")
