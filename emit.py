# Emitter object keeps track of the generated code and outputs it
class Emitter:
    def __init__(self, fullPath):
        self.fullpath = fullPath
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emitLine(self, code):
        self.code += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'

    def writeFile(self):
        with open(self.fullpath, 'w') as outputFile:
            outputFile.write(self.header + self.code)

# this is the entirety of the emitters coded. it is simply a helper class for appending strings together