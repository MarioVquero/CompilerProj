import sys
from lex import *

# Parser object keeps track of current token and checks if the code matches the grammar
class Parser:
    def __init__ (self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.labelsDeclared = set() # variables declared so far
        self.labeslGotoed = set() # labels declared so far
        

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
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        # Since some newlines are required in our grammar, need to skip the excess
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # wrap everything up
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        # check that each label referenced in GOTO is delcared
        for label in self.labeslGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

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
        
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            print("STATEMENT_IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # Zero or more statements in the body
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # Zero or more statements in the loop body
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT_LABEL")
            self.nextToken()

            # make sure this lavel doesnt already exist
            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists" + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)
            
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT_GOTO")
            self.nextToken()
            self.labeslGotoed.add(self.curToken.text)
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STATEMENT_LEFT")
            self.nextToken()

            # check if ident exists in symbol table if not declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT_INPUT")
            self.nextToken()

            # If variable doesnt already exit declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)

        # NOTE: ERROR CATCHER/ INPUT IS NOT A VALID STATEMENT
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # NEWLINE.
        self.nl()
    

    # nl ::= '\n' +
    def nl(self):
        print("NEWLINE")

        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        # NOTE: We will allow extra newlines too, of course
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text )

        # can have 0 or more comparison operator and expressions
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    # Return true if the current token is a comparison operator
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

        
    # Expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")
        
        self.unary()
        # Can have 0 or more *// and expressions
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()
    
    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # Ensure the variable already exists
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment " + self.curToken.text)
            self.nextToken()
        else:
            # ERROR
            self.abort("Unexpected token at " + self.curToken.text)