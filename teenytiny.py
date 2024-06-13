from lex import *
from emit import *
from parse import *
import sys

def main():
    print("Teeny Tiny Compiler")
    
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()
    
    # Initialize the lexer and parser.
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program() #start the parser.
    Emitter.writefile() #write the output to file
    print("compiling complete")

main()