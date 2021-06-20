import sys
import copy

from tag import Tag
from token import Token
from lexer import Lexer
from no import No

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
      if self.token is None: # erro no Lexer
        sys.exit(0)

   def sinalizaErroSemantico(self, message):
      print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
      if self.token is None: # erro no Lexer
        sys.exit(0)
   
   def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

   # verifica token esperado t 
   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False

   """
   LEMBRETE:
   Todas as decisoes do Parser, sao guiadas pela Tabela Preditiva (TP)
   """

   # Programa -> CMD EOF
   def Programa(self):
      self.Cmd()
      if(self.token.getNome() != Tag.EOF):
         self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   def Cmd(self):

      # armazena token corrente, uma vez que o ID pode ser consumido
      tempToken = copy.copy(self.token)

      # Cmd -> if E then { CMD } CMD'
      if(self.eat(Tag.KW_IF)): 
         noE = self.E()
         if noE.tipo != Tag.TIPO_LOGICO:
            self.sinalizaErroSemantico("Expressao mal formada.")

         if(not self.eat(Tag.KW_THEN)):
            self.sinalizaErroSintatico("Esperado \"then\", encontrado " + "\"" + self.token.getLexema() + "\"")

         if(not self.eat(Tag.SMB_AB_CHA)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")

         self.Cmd()

         if(not self.eat(Tag.SMB_FE_CHA)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")

         self.CmdLinha()
      # Cmd -> id = T
      elif(self.eat(Tag.ID)):
        if(not self.eat(Tag.OP_ATRIB)):
            self.sinalizaErroSintatico("Esperado \"=\", encontrado " + "\"" + self.token.getLexema() + "\"")
       
        noT = self.T()

        if noT.tipo == Tag.TIPO_NUMERO:
          self.lexer.ts.removeToken(tempToken.getLexema())
          tempToken.setTipo(noT.tipo)
          self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
        else:
          self.sinalizaErroSemantico("Variável não declarada antes de atribuição")
      # Cmd -> print T
      elif(self.eat(Tag.KW_PRINT)):
        noT = self.T()
        if(noT.tipo == Tag.TIPO_VAZIO):
          self.sinalizaErroSemantico("Variavel não declarada.")
      else:
         self.skip("Esperado \"if, print, id\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   def CmdLinha(self):
      # CmdLinha -> else { CMD }
      if(self.eat(Tag.KW_ELSE)):
         if(not self.eat(Tag.SMB_AB_CHA)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FE_CHA)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
      # CmdLinha -> epsilon
      elif(self.token.getNome() == Tag.SMB_FE_CHA or self.token.getNome() == Tag.EOF):
         return
      else:
         self.skip("Esperado \"else, }\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   # E -> T T'
   def E(self):
      noE = No()
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM):
        noT = self.T()
        noTLinha = self.TLinha()

        if noTLinha.tipo == Tag.TIPO_VAZIO:
          noE.tipo = noT.tipo
        elif noTLinha.tipo == noT.tipo and noT.tipo == Tag.TIPO_NUMERO:
          noE.tipo = Tag.TIPO_LOGICO
        else:
          noE.tipo = Tag.TIPO_ERRO
        return noE
      else:
         self.sinalizaErroSintatico("Esperado \"id, numero\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   '''
   Mudei um pouco essa implementacao para ficar mais simples.
   T' --> ">" T  | "<" T | ">=" T | 
          "<=" T | "==" T | "!=" T| epsilon
   '''
   def TLinha(self):
      noTLinha = No()
      if(self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or 
         self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE)):
        noT = self.T()
        noTLinha.tipo = noT.tipo
        return noTLinha
      elif(self.token.getNome() == Tag.KW_THEN):
         return noTLinha
      else:
         self.skip("Esperado \">, <, >=, <=, ==, !=, then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   # T -> id | num
   def T(self):
      noT = No()

      # armazena token corrente, uma vez que o ID pode ser consumido
      tempToken = copy.copy(self.token) 

      if(self.eat(Tag.ID)):
          noT.tipo = tempToken.getTipo()
      elif(self.eat(Tag.NUM)):
        noT.tipo = Tag.TIPO_NUMERO
      else:
        self.skip("Esperado \"numero, id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        sys.exit(0)

      return noT
