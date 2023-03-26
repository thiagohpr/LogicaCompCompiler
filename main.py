import sys

class symbolTable():
    table = {}
    def getter(name):
        if name not in symbolTable.table.keys():
            raise ValueError(f'Variável {name} não declarada!')
        return symbolTable.table[name]

    def setter(name, value):
        symbolTable.table[name] = value
            

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
        # print(f'UnOp {self.value}')
        if self.value=='-':
            return -self.children[0].evaluate()
        return self.children[0].evaluate()

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        # print(f'Valor {self.value}')
        return self.value
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self):
        super().evaluate()

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self):
        # print(f'BinOp {self.value}')
        if self.value=='+':
            return self.children[0].evaluate() + self.children[1].evaluate()

        if self.value=='-':
            return self.children[0].evaluate() - self.children[1].evaluate()

        if self.value=='*':
            return self.children[0].evaluate() * self.children[1].evaluate()

        if self.value=='/':
            return self.children[0].evaluate() // self.children[1].evaluate()
        
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])
    def evaluate(self):
        # print(f'Variavel {self.value}')
        return symbolTable.getter(self.value)
    
class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self):
        # print('Print')
        print(self.children[0].evaluate())

class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self):
        # print('Assignment')
        symbolTable.setter(self.children[0].value, self.children[1].evaluate())

class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self):
        # print(f'Block')
        for statement in self.children:
            statement.evaluate()
        

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
        operationsTokens = ['+', '-', '/', '*', '(', ')','=']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        reservedWords = ['println']

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
            elif c == '=':
                self.next = Token('=', 'EQUAL')
            self.position+=1
        elif c =='\n':
            self.next = Token('\n', 'LINE')
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
                
                if c == ' ' or c in operationsTokens or c=='\n':
                    tokenIncomplete = False
                    self.next = Token(int(number),'INT')
                else:
                    number += c
        elif c == ' ':
            self.position += 1
            self.selectNext()
        
        else:
            tokenIncomplete = True
            word = ''
            word += c
            while tokenIncomplete:
                self.position+=1
                try:
                    c = self.source[self.position]
                    if c == ' ' or c in operationsTokens or c=='\n':
                        tokenIncomplete = False
                        
                    else:
                        word += c
                except:
                    
                    tokenIncomplete=False
            if word in reservedWords:
                if word == reservedWords[0]:
                    self.next = Token('println','PRINT')
            else:
                self.next = Token(word,'IDEN')

                
class PrePro():
    @staticmethod
    def filter(code):
        statements=[]
        for statement in code.split('\n'):
            index_first_comment = statement.find('#')
            if index_first_comment==-1:
                statements.append(statement)
            elif index_first_comment==0:
                pass
            else:
                statements.append(statement[:index_first_comment])
        return '\n'.join(statements)
    

class Parser():
    tokenizer = None
    @staticmethod
    def parseBlock():
        statements = []
        token_atual = Parser.tokenizer.next

        while token_atual.type !='EOF':
            statements.append(Parser.parseStatement())
            token_atual = Parser.tokenizer.next
            # print(token_atual.type)
        # print(statements)
        return Block(statements)
    
    @staticmethod
    def parseStatement():
        token_atual = Parser.tokenizer.next
        if token_atual.type == 'LINE':
            Parser.tokenizer.selectNext()
            return NoOp()
        
        else:
            if token_atual.type == 'IDEN':
                # print('Variável')
                iden_name = token_atual.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'EQUAL':
                    # print('Igual')
                    Parser.tokenizer.selectNext()
                    this_node = Assignment([Identifier(iden_name),Parser.parseExpression()])
                else:
                    raise ValueError('Erro ao declarar variável.')
            
            elif token_atual.type == 'PRINT':
                # print('Print')
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next
                if token_atual.value == '(':
                    # print('(')
                    Parser.tokenizer.selectNext()
                    token_atual = Parser.tokenizer.next
                    this_node = Print([Parser.parseExpression()])
                    token_atual = Parser.tokenizer.next
                    if token_atual.value != ')':
                        raise ValueError('Não fechou parênteses!')
                    # print(')')
                    Parser.tokenizer.selectNext()

            token_atual = Parser.tokenizer.next
            # print(token_atual.type)
            if token_atual.type == 'LINE' or token_atual.type == 'EOF':
                Parser.tokenizer.selectNext()
                return this_node
            else:
                raise ValueError(r'A linha não acabou com um \n')
    
    @staticmethod
    def parseExpression():
        this_node = Parser.parseTerm()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'PLUS' or token_atual.type == 'MINUS':
            # print('Binop')
            Parser.tokenizer.selectNext()
            this_node = BinOp(token_atual.value,[this_node,Parser.parseTerm()])
            token_atual = Parser.tokenizer.next  

        return this_node
    
    @staticmethod
    def parseTerm():
        # resultado = Parser.parseFactor()
        this_node = Parser.parseFactor()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'MULT' or token_atual.type == 'DIV':
            # print('Binop')
            Parser.tokenizer.selectNext()
            this_node = BinOp(token_atual.value,[this_node,Parser.parseFactor()])
            token_atual = Parser.tokenizer.next  

        return this_node
        
    @staticmethod
    def parseFactor():
        token_atual = Parser.tokenizer.next
        # print(token_atual.type)
        if token_atual.type == 'INT':
            # print('Inteiro')
            # resultado = token_atual.value
            Parser.tokenizer.selectNext()
            this_node = IntVal(token_atual.value)

        elif token_atual.type == 'IDEN':
            # print('Variável')
            Parser.tokenizer.selectNext()
            this_node = Identifier(token_atual.value)

        elif token_atual.type == 'MINUS':
            # print('Menos')
            Parser.tokenizer.selectNext()
            this_node = UnOp('-', [Parser.parseFactor()])
            # resultado = Parser.parseFactor() * (-1)

        elif token_atual.type == 'PLUS':
            # print('Mais')
            Parser.tokenizer.selectNext()
            this_node = UnOp('+', [Parser.parseFactor()])
            # resultado = Parser.parseFactor()

        elif token_atual.value == '(':
            # print('(')
            Parser.tokenizer.selectNext()
            this_node = Parser.parseExpression()
            token_atual = Parser.tokenizer.next
            if token_atual.value != ')':
                raise ValueError('Não fechou parênteses!')
            # print(')')
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

        parent_node = Parser.parseBlock()
        result = parent_node.evaluate()

        if Parser.tokenizer.next.type == 'EOF':
            return result
        else:
            raise ValueError('Não chegou no final do código!')

parser = Parser()
archive = sys.argv[1]
with open(archive, 'r') as file:
    archive_content = file.read()
parser.run(archive_content)



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
# words3 = [
#     '''a = 1\nb435245= 1 + 2\nc =(3/4)/2*2\nprintln(c)'''
# ]
# parser = Parser()
# # print(parser.run('2+5*4'))

# with open('teste.jl', 'r') as file:
#     archive_content = file.read()
# words = [archive_content]
# for word in words:
#     print(word)

#     prepro = PrePro()
#     code_filtered = prepro.filter(word)

#     tokenizer = Tokenizer(code_filtered)
#     tokenizer.selectNext()
#     print(f'{tokenizer.next.type}: {tokenizer.next.value}')
#     while (tokenizer.next.type!='EOF'):
#         tokenizer.selectNext()
#         print(f'{tokenizer.next.type}: {tokenizer.next.value}')

#     parser.run(word)

#     print('-------------------------')