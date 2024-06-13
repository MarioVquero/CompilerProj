# Emitter object keeps track of the generated code and outputs it
class Emitter:
    def __init__(self, fullPath):
        self.fullpath = fullPath
        self.header = ""
        self.code = ""

    def emit(self,code):
        self.code += code

    def emitline(self, code):
        self.code += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'

    def writeFile(self):
        with open(self.fullpath, 'w') as outputFile:
            outputFile.write(self.header + self.code)
