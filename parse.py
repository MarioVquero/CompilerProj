import sys
from lex import *

# Parser object keeps track of current token and checks if the code matches the grammar
class Parser:
    def __init__ (self, lexer):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() # called twice to initialize current and peek

    # return true if the current token matches:
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # return true if the next token matches:
    def checkPeek(self,kind):
        return kind == self.peekToken.kind

    # Try to match current token. if not, error Advances the current token
    def match(self,kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + " , got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # no need to worry about passing the EOF, lexer handles that.

    def abort(self,message):
        sys.exit("Error" + message)

    # Production rules

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):
        # Check the first token to see what kind of statement this is.
        # "PRINT" (expressions | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # Simple string.
                self.nextToken()

            else:
                # expect an expression.
                self.expression()

        # NEWLINE.
        self.nl()
    

    # nl ::= '\n' +
    def nl(self):
        print("NEWLINE")

        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        # NOTE: We will allow extra newlines too, of course
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken
    
    
