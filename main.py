#Franciele de Paula

from tabulate import tabulate
import argparse
from AnalisadorLexico import *

#argumentos da linha de comandos: -i [arquivo de entrada .c] -o [arquivo de saida contendo os tokens]
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="insert the path and name of a .c file (DEFAULT: 'input/teste1.c')", default="input/teste1.c")
parser.add_argument("-o", "--output", help="insert the path and name of output file (DEFAULT: 'output/output.txt')", default="output/output.txt")
args = parser.parse_args()
f_in = open(args.input, "r") #lê o arquivo de entrada

token_lista, cont_linha = analisador_lexico(f_in)

#grava no arquivo de saida os tokens reconhecidos
f_out = open(args.output, "w")
f_out.write(tabulate(token_lista, headers=['Token', 'Lexema', 'Linha', 'Coluna'],tablefmt="fancy_grid"),)

f_out.close()

f_in.close()

