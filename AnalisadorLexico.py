from Csmall import tokens
from colorama import Fore
from colorama import Style
import re

def analisador_lexico(f_in):

  buffer = [] #forma cada lexema 
  token_lista = [] #tokens reconhecidos 
  estado = 0 #estado inicial do automato
  cont_linha = 1 #salva o numero atual da linha 

  for linha in f_in: #percorre as linhas do arquivo de entrada
    linha = linha.rstrip('\n')
    cont_char = 0

    while (cont_char < len(linha)): #percorre todos os caracteres da linha

      char = linha[cont_char] #le o proximo caractere do buffer

      if estado == 0:
        if char.isalpha():
          estado = 1
          buffer.append(char)
        elif char.isnumeric():
          estado = 2
          buffer.append(char)
        elif char == '<':
          estado = 5
          buffer.append(char)
        elif char == '>':
          estado = 6
          buffer.append(char)
        elif char == '=':
          estado = 7
          buffer.append(char)
        elif char == '!':
          estado = 8
          buffer.append(char)
        elif char == '|':
          estado = 9
          buffer.append(char)
        elif char == '&':
          estado = 10
          buffer.append(char)
        elif char == ' ':
          pass
        else:
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema,cont_linha,cont_char+1]) #armazenado na lista de tokens reconhecido 
          buffer = [] #limpa o buffer

      elif estado == 1:
        if re.match('^[a-zA-Z0-9_]*$', char):
          buffer.append(char)
        else:
          col=(cont_char - len(buffer))+1
          cont_char -= 1
          estado = 0
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema] if lexema in tokens else "ID", lexema, cont_linha,col]) #armazenado como palavra reservada ou ID
          buffer = [] #limpa o buffer

      elif estado == 2:
        if char.isnumeric():
          buffer.append(char)
        elif char == '.': #ponto decimal, vai para o estado 3
          estado = 3
          buffer.append(char)
        else:
          col=(cont_char - len(buffer))+1
          cont_char -= 1
          estado = 0
          lexema = ''.join(buffer)
          token_lista.append(['INTEGER_CONST', lexema, cont_linha,col]) #token armazenado como constante inteira
          buffer = [] # Limpa o buffer
          
      elif estado == 3:
        if char.isnumeric(): #numero após o ponto decimal, vai para o estado 4
          estado = 4
          buffer.append(char)
        else:
          print(Fore.RED,'Erro',f'[Linha {cont_linha}, Coluna {cont_char}]: Produção não aceita no estado {estado}.',Fore.RESET)
          print('Foi recebido',Fore.YELLOW,*buffer,char,Fore.RESET)

      elif estado == 4:
        if char.isnumeric():
          buffer.append(char)
        else:
          col=(cont_char - len(buffer))+1
          cont_char -= 1
          estado = 0
          lexema = ''.join(buffer)
          token_lista.append(['FLOAT_CONST', lexema, cont_linha,col]) #token armazenado como float 
          buffer = [] # Limpa o buffer

      elif estado == 5:
        if (char == '='):
          estado = 0
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha]) #token armazenado como <=
          buffer = [] #limpa o buffer
        else:
          col=(cont_char - len(buffer))+1        
          cont_char -= 1
          estado = 0
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, col]) #token armazenado como <
          buffer = [] #limpa o buffer

      elif estado == 6:
        if (char == '='):
          estado = 0
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha]) #token armazenado como >=
          buffer = [] #limpa o buffer
        else:
          col=(cont_char - len(buffer))+1          
          cont_char -= 1
          estado = 0
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha,col]) #token armazenado como >
          buffer = [] #limpa o buffer

      elif estado == 7:
        if (char == '='):
          estado = 0
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha,cont_char]) #token armazenado como ==
          buffer = [] # Limpa o buffer
        else:
          col=(cont_char - len(buffer))+1
          cont_char -= 1
          estado = 0
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha,col]) #token armazenado como =
          buffer = [] # Limpa o buffer

      elif estado == 8:
        if (char == '='):
          estado = 0
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha, cont_char]) #token armazenado como !=
          buffer = [] # Limpa o buffer
        else:
          print(Fore.RED,'Erro',f'[Linha {cont_linha}, Coluna {cont_char}]: Produção não aceita no estado {estado}.',Fore.RESET)
          print('Era esperado',Fore.YELLOW,'!=',Fore.RESET,'\nFoi recebido',Fore.YELLOW,'!'+char,Fore.RESET)
          estado = 0
          buffer=[]

      elif estado == 9:
        if (char == '|'):
          estado = 0
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha,cont_char]) #token armazenado como ||
          buffer = [] # Limpa o buffer
        else:
          print(Fore.RED,'Erro',f'[Linha {cont_linha}, Coluna {cont_char}]: Produção não aceita no estado {estado}.',Fore.RESET)
          print('Era esperado',Fore.YELLOW,'||',Fore.RESET,'\nFoi recebido',Fore.YELLOW,'|'+char,Fore.RESET)
          buffer = [] #limpa o buffer
          estado = 0

      elif estado == 10:
        if (char == '&'):
          estado = 0
          buffer.append(char)
          lexema = ''.join(buffer)
          token_lista.append([tokens[lexema], lexema, cont_linha,cont_char]) #token armazenado como &&
          buffer = [] # Limpa o buffer
        else:
          print(Fore.RED,'Erro',f'[Linha {cont_linha}, Coluna {cont_char}]: Produção não aceita no estado {estado}.',Fore.RESET)
          print('Era esperado',Fore.YELLOW,'&&',Fore.RESET,'\nFoi recebido',Fore.YELLOW,'&'+char,Fore.RESET)
          buffer = []
          estado = 0 
      cont_char += 1

    cont_linha += 1
  token_lista.append(['EOF', '', cont_linha,'1']) #token referente ao fim do arquivo

  return token_lista, cont_linha  

