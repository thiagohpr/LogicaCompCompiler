import sys

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self):
        pass 

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value=='-':
            return -self.children[0].evaluate()
        return self.children[0].evaluate()

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        return self.value
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self):
        return super().evaluate()

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self):
        if self.value=='+':
            return self.children[0].evaluate() + self.children[1].evaluate()

        if self.value=='-':
            return self.children[0].evaluate() - self.children[1].evaluate()

        if self.value=='*':
            return self.children[0].evaluate() * self.children[1].evaluate()

        if self.value=='/':
            return self.children[0].evaluate() // self.children[1].evaluate()
        

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
        operationsTokens = ['+', '-', '/', '*', '(', ')']
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
            elif c == '(':
                self.next = Token('(', 'PAREN')
            elif c == ')':
                self.next = Token(')', 'PAREN')
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
        this_node = Parser.parseTerm()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'PLUS' or token_atual.type == 'MINUS':
            Parser.tokenizer.selectNext()
            this_node = BinOp(token_atual.value,[this_node,Parser.parseFactor()])
            
            token_atual = Parser.tokenizer.next  

        
        return this_node
    
    @staticmethod
    def parseTerm():
        # resultado = Parser.parseFactor()
        this_node = Parser.parseFactor()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'MULT' or token_atual.type == 'DIV':
            Parser.tokenizer.selectNext()
            this_node = BinOp(token_atual.value,[this_node,Parser.parseFactor()])

            token_atual = Parser.tokenizer.next  
        
        return this_node
        
    @staticmethod
    def parseFactor():
        token_atual = Parser.tokenizer.next
        if token_atual.type == 'INT':
            # resultado = token_atual.value
            Parser.tokenizer.selectNext()
            this_node = IntVal(token_atual.value)
            

        elif token_atual.type == 'MINUS':
            Parser.tokenizer.selectNext()
            this_node = UnOp('-', [Parser.parseFactor()])
            # resultado = Parser.parseFactor() * (-1)

        elif token_atual.type == 'PLUS':
            Parser.tokenizer.selectNext()
            this_node = UnOp('+', [Parser.parseFactor()])
            # resultado = Parser.parseFactor()

        elif token_atual.value == '(':
            Parser.tokenizer.selectNext()
            this_node = Parser.parseExpression()
            token_atual = Parser.tokenizer.next
            if token_atual.value != ')':
                raise ValueError('Não fechou parênteses!')
            Parser.tokenizer.selectNext()
        else:
            raise ValueError('Erro de continuidade!')
        return this_node
            
    @staticmethod
    def run(code):
        prepro = PrePro()
        code_filtered = prepro.filter(code)

        Parser.tokenizer = Tokenizer(code_filtered)
        Parser.tokenizer.selectNext()

        parent_node = Parser.parseExpression()
        result = parent_node.evaluate()

        if Parser.tokenizer.next.type == 'EOF':
            return result
        else:
            raise ValueError('Não chegou no final do código!')

parser = Parser()
archive = sys.argv[1]
with open(archive, 'r') as file:
    archive_content = file.read()
print(parser.run(archive_content))

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
# words2 = [
#     '(3 + 2) /5',
#     '+--++3',
#     '3 - -2/4',
#     '4/(1+1)*2',
#     '(2*2'
# ]
# parser = Parser()
# print(parser.run('3* 3 + # a 5'))
# for word in words2:
#     print(word)
#     parser.run(word)
#     # prepro = PrePro()
#     # code_filtered = prepro.filter(word)
#     # tokenizer = Tokenizer(code_filtered)
#     # tokenizer.selectNext()
#     # print(f'{tokenizer.next.type}: {tokenizer.next.value}')
#     # while (tokenizer.next.type!='EOF'):
#     #     tokenizer.selectNext()
#     #     print(f'{tokenizer.next.type}: {tokenizer.next.value}')
#     print('-------------------------')