import sys

class Token():
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Tokenizer():
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        tokenIncomplete = True
        operationsTokens = ['+', '-', '/', '*']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        try:
            c = self.source[self.position]
        except:
            self.next = Token('','EOF')
            return

        if c in operationsTokens:
            if c == '+':
                self.next = Token('+', 'PLUS')
            elif c == '-':
                self.next = Token('-', 'MINUS')
            elif c == '/':
                self.next = Token('/', 'DIV')
            elif c == '*':
                self.next = Token('*', 'MULT')
            self.position+=1
 
        elif c in numbers:
            tokenIncomplete = True
            number = ''
            number += c
            while tokenIncomplete:
                self.position+=1
                try:
                    c = self.source[self.position]
                except:
                    self.next = Token(int(number),'INT')
                    return
                
                if c == ' ' or c in operationsTokens:
                    tokenIncomplete = False
                    self.next = Token(int(number),'INT')
                else:
                    number += c
        elif c == ' ':
            self.position += 1
            self.selectNext()

class PrePro():
    @staticmethod
    def filter(code):
        index_first_comment = code.find('#')
        if index_first_comment==-1:
            return code
        elif index_first_comment==0:
            return ''
        return code[:index_first_comment]
    

class Parser():
    tokenizer = None

    @staticmethod
    def parseExpression():
        resultado = Parser.parseTerm()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'PLUS' or token_atual.type == 'MINUS':
            if token_atual.type == 'PLUS':
                Parser.tokenizer.selectNext()
                resultado += Parser.parseTerm()

            elif token_atual.type == 'MINUS':
                Parser.tokenizer.selectNext()
                resultado -= Parser.parseTerm()

            token_atual = Parser.tokenizer.next  
        
        return resultado

    @staticmethod
    def parseTerm():
        token_atual = Parser.tokenizer.next
        if token_atual.type == 'INT':
            resultado = token_atual.value
            Parser.tokenizer.selectNext()
            token_atual = Parser.tokenizer.next

            while token_atual.type == 'MULT' or token_atual.type == 'DIV':
                if token_atual.type == 'MULT':
                    Parser.tokenizer.selectNext()
                    token_atual = Parser.tokenizer.next
                    if token_atual.type == 'INT':
                        resultado *= token_atual.value
                    else:
                        raise ValueError('Operações seguidas!')

                elif token_atual.type == 'DIV':
                    Parser.tokenizer.selectNext()
                    token_atual = Parser.tokenizer.next
                    if token_atual.type == 'INT':
                        resultado //= token_atual.value
                    else:
                        raise ValueError('Operações seguidas!')
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next  
            
            return resultado

        else:
            raise ValueError('Começou com operação!')
    @staticmethod
    def run(code):
        prepro = PrePro()
        code_filtered = prepro.filter(code)

        Parser.tokenizer = Tokenizer(code_filtered)
        Parser.tokenizer.selectNext()

        result = Parser.parseExpression()

        if Parser.tokenizer.next.type == 'EOF':
            return result
        else:
            raise ValueError('Não chegou no final do código!')

parser = Parser()
print(parser.run(sys.argv[1]))

# words = [
#     '3-2',
#     '1 # b',
#     '11+22-33 # # a',
#     '4/2+3',
#     '3+4/2',
#     '+3',
#     '3+ # a',
#     '# a',
#     '3* 3 + # a 5'
# ]
# parser = Parser()
# for word in words:
#     print(word)
#     print(parser.run(word))
# #     prepro = PrePro()
# #     code_filtered = prepro.filter(word)
# #     tokenizer = Tokenizer(code_filtered)
# #     tokenizer.selectNext()
# #     print(f'{tokenizer.next.type}: {tokenizer.next.value}')
# #     while (tokenizer.next.type!='EOF'):
# #         tokenizer.selectNext()
# #         print(f'{tokenizer.next.type}: {tokenizer.next.value}')
#     print('-------------------------')