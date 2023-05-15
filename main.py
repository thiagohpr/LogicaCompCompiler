import sys

class AssemblyHandler():
    def write(lines):
        with open ('assembly.txt', 'r') as file:
            last_lines = file.read()
        with open ('assembly.txt', 'w') as file:
            file.write(last_lines)
            file.write(lines)
    

class symbolTable():
    table = {}
    def getter(name):
        if name not in symbolTable.table.keys():
            raise ValueError(f'Variável {name} não declarada!')
        return symbolTable.table[name]

    # def setter(name, valueTuple):
    #     this_type, this_value = symbolTable.table[name]
    #     new_type, new_value, shift = valueTuple

    #     if new_type == 'str':
    #         new_type = 'string'

    #     if name not in symbolTable.table.keys():
    #         raise ValueError('Variável não declarada!')
        
    #     if new_type != this_type:
    #         raise ValueError('Variável recebeu tipo errado!')

    #     symbolTable.table[name] = (this_type, new_value, shift)

    def create(name, type):
        if name in symbolTable.table.keys():
            raise ValueError('Variável já declarada!')
        symbolTable.table[name] = (type, None, -4*(len(symbolTable.table)+1))
            

class Node():
    i=0

    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self):
        pass

    def new_id(self):
        Node.i += 1
        return Node.i

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        # print(f'UnOp {self.value}')
        if self.value=='-':
            return ('int',-self.children[0].evaluate())
        if self.value=='+':
            return ('int',self.children[0].evaluate())
        if self.value=='!':
            return ('int',not self.children[0].evaluate())

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        # print(f'Int Valor {self.value}')
        # return ('int',self.value)
        AssemblyHandler.write(f'MOV EBX,{self.value}')
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        # print(f'Str Valor {self.value}')
        return ('str', self.value)

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
        # if self.value=='.':
        #     return ('str', str(self.children[0].evaluate()[1]) + str(self.children[1].evaluate()[1]))
        # else:
        #     if self.children[0].evaluate()[0]=='int' and self.children[1].evaluate()[0]=='int':
        #         if self.value=='+':
        #             return ('int',self.children[0].evaluate()[1] + self.children[1].evaluate()[1])

        #         if self.value=='-':
        #             return ('int',self.children[0].evaluate()[1] - self.children[1].evaluate()[1])

        #         if self.value=='*':
        #             return ('int',self.children[0].evaluate()[1] * self.children[1].evaluate()[1])

        #         if self.value=='/':
        #             return ('int',int(self.children[0].evaluate()[1] // self.children[1].evaluate()[1]))
                
        #         if self.value=='||':
        #             return ('int',int(self.children[0].evaluate()[1] or self.children[1].evaluate()[1]))
                
        #         if self.value=='&&':
        #             return ('int',int(self.children[0].evaluate()[1] and self.children[1].evaluate()[1]))
                
        #         if self.value=='==':
        #             return ('int',int(self.children[0].evaluate()[1] == self.children[1].evaluate()[1]))
                
        #         if self.value=='>':
        #             return ('int',int(self.children[0].evaluate()[1] > self.children[1].evaluate()[1]))
                
        #         if self.value=='<':
        #             return ('int',int(self.children[0].evaluate()[1] < self.children[1].evaluate()[1]))
        #     else:
        #         if self.value == '==':
        #             return ("int", int(self.children[0].evaluate()[1] == self.children[1].evaluate()[1]))
        #         elif self.value == '>':
        #             return ("int", int(self.children[0].evaluate()[1] > self.children[1].evaluate()[1]))
        #         elif self.value == '<':
        #             return ("int", int(self.children[0].evaluate()[1] < self.children[1].evaluate()[1]))
        #         else:
        #             raise ValueError('Erro de operação binária')
        self.children[0].evaluate()
        AssemblyHandler('PUSH EBX')
        self.children[1].evaluate()
        AssemblyHandler('POP EAX')
        operator = ''
        lines = ''

        if self.value in ['>','<','==']:
            if self.value=='==':
                operator = 'binop_je'
            if self.value=='>':
                operator = 'binop_jg'
            if self.value=='<':
                operator = 'binop_jl'

            lines = f'''
CMP EAX, EBX
CALL {operator}'''

        else:
            if self.value=='+':
                operator = 'ADD'
            if self.value=='-':
                operator = 'SUB'
            if self.value=='*':
                operator = 'IMUL'
            if self.value=='/':
                operator = 'IDIV'
            if self.value=='||':
                operator = 'OR'
            if self.value=='&&':
                operator = 'AND'
            lines = f'''
{operator} EAX, EBX
MOV EBX, EAX'''

        AssemblyHandler.write(lines)



class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])
    def evaluate(self):
        # print(f'Variavel {self.value}')
        # return symbolTable.getter(self.value)
        AssemblyHandler(f'MOV EBX, [EBP{symbolTable.getter(self.value)[2]}]')
    
class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self):
        # print('Print')
        #print(self.children[0].evaluate()[1])
        self.children[0].evaluate()
        lines = '''PUSH EBX
CALL print
POP EBX
'''
        AssemblyHandler.write(lines)


class Read(Node):
    def __init__(self):
        super().__init__(None, [])
    def evaluate(self):
        # print('Read')
        return ('int', int(input()))

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def evaluate(self):
        # print(f'Create {self.value} {self.children[0].value} = {self.children[-1].evaluate()}')
        symbolTable.create(self.children[0].value, self.value)
        AssemblyHandler.write('PUSH DWORD 0')
        #symbolTable.setter(self.children[0].value, self.children[-1].evaluate())
        self.children[-1].evaluate()
        this_shift = symbolTable.getter(self.children[0].value)[2]
        AssemblyHandler.write(f'MOV [EBP{this_shift}], EBX')
        # else:
        #     if self.value == 'String':
        #         symbolTable.create(self.children[0].value, self.value, "")
        #     elif self.value == 'Int':
        #         symbolTable.create(self.children[0].value, self.value, 0)

class While(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        # print('While')
        AssemblyHandler.write(f"LOOP_{self.id}:")
        self.children[0].evaluate()
        AssemblyHandler.write(f"CMP EBX, 0")
        AssemblyHandler.write(f"JE EXIT_{self.id}")
        self.children[1].evaluate()
        AssemblyHandler.write(f"JMP LOOP_{self.id}")
        AssemblyHandler.write(f"EXIT_{self.id}:")

        #while self.children[0].evaluate()[1]:
        #    self.children[1].evaluate()

class If(Node):
    def __init__(self, children):
        super().__init__(None, children)
        self.id = self.new_id()

    def evaluate(self):
        # print('If')

        if len(self.children) == 2: #if without else
            self.children[0].evaluate()
            AssemblyHandler.write(f"CMP EBX, 0")
            AssemblyHandler.write(f"JE EXIT_{self.id}")
            self.children[1].evaluate()
            AssemblyHandler.write(f"EXIT_{self.id}:")
            
            
            #if self.children[0].evaluate()[1]:
            #    self.children[1].evaluate()
        else: #if with else
            self.children[0].evaluate()
            AssemblyHandler.write(f"CMP EBX, 0")
            AssemblyHandler.write(f"JE ELSE_{self.id}")
            self.children[1].evaluate()
            AssemblyHandler.write(f"JMP EXIT_{self.id}")
            AssemblyHandler.write(f"ELSE_{self.id}:")
            self.children[2].evaluate()
            AssemblyHandler.write(f"EXIT_{self.id}:")

        # if self.children[0].evaluate():
        #     self.children[1].evaluate()
        # else:
        #     if len(self.children)==3:
        #        self.children[2].evaluate() 


class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self):
        # print('Assignment')
        # symbolTable.setter(self.children[0].value, self.children[1].evaluate())
        self.children[1].evaluate()
        this_shift = symbolTable.getter(self.children[0].value)[2]
        AssemblyHandler.write(f'MOV [EBP{this_shift}], EBX')

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
        operationsTokens = ['+', '-', '/', '*', '(', ')','=','>','<','|','&','!',':','.']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        reservedWords = ['println','if','else','while','readline','end','Int','String']

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
            elif c == '>':
                self.next = Token('>', 'GREATER')
            elif c == '<':
                self.next = Token('<', 'LESSER')
            elif c == '!':
                self.next = Token('!', 'NOT')
            elif c == '.':
                self.next = Token('.', 'CONCAT')
            elif c == '=':
                next_c = self.source[self.position+1]
                if next_c =='=':
                    self.next = Token('==', 'EQUAL')
                    self.position+=1
                else:
                    self.next = Token('=', 'ASSIGN')
            elif c == '|':
                next_c = self.source[self.position+1]
                if next_c =='|':
                    self.next = Token('||', 'OR')
                    self.position+=1
                else:
                    raise ValueError('Erro Léxico')
            elif c == '&':
                next_c = self.source[self.position+1]
                if next_c =='&':
                    self.next = Token('&&', 'AND')
                    self.position+=1
                else:
                    raise ValueError('Erro Léxico')
            elif c == ':':
                next_c = self.source[self.position+1]
                if next_c ==':':
                    self.next = Token('::', 'DEC')
                    self.position+=1
                else:
                    raise ValueError('Erro Léxico')
            
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
        
        elif c=='"':
            tokenIncomplete = True
            word = ''
            while tokenIncomplete:
                self.position+=1
                try:
                    c = self.source[self.position]
                    if c == '"':
                        tokenIncomplete = False
                        
                    else:
                        word += c
                except:
                    raise ValueError('Erro Léxico')
            self.position+=1
            self.next = Token(word,'STRING')

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
                if word == 'Int' or word == 'String':
                    self.next = Token(word, 'TYPE')
                else:
                    self.next = Token(word,word.upper())
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
        # print(f'Entrada statement: {token_atual.type}')
        if token_atual.type == 'LINE':
            Parser.tokenizer.selectNext()
            return NoOp()
        
        else:
            if token_atual.type == 'IDEN':
                # print('Variável')
                iden_name = token_atual.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'ASSIGN':
                    # print('Igual')
                    Parser.tokenizer.selectNext()
                    this_node = Assignment([Identifier(iden_name),Parser.parseRelExpression()])

                elif Parser.tokenizer.next.type == 'DEC':
                    # print('Dec')
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'TYPE':
                        varType = Parser.tokenizer.next.value.lower()
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == 'ASSIGN':
                            Parser.tokenizer.selectNext()
                            this_node = VarDec(varType,[Identifier(iden_name),Parser.parseRelExpression()])
                        else:
                            default = ''
                            if varType == 'int':
                                default = IntVal(0)
                            elif varType=='string':
                                default = StrVal('')
                            this_node = VarDec(varType,[Identifier(iden_name),default])

                    else:
                        raise ValueError('Tipo errado.')

                else:
                    raise ValueError('Erro ao declarar variável.')
            
            elif token_atual.type == 'PRINTLN':
                # print('Print')
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next
                if token_atual.value == '(':
                    # print('(')
                    Parser.tokenizer.selectNext()
                    token_atual = Parser.tokenizer.next
                    this_node = Print([Parser.parseRelExpression()])
                    token_atual = Parser.tokenizer.next
                    if token_atual.value != ')':
                        raise ValueError('Não fechou parênteses!')
                    # print(')')
                    Parser.tokenizer.selectNext()

            elif token_atual.type == 'WHILE':
                # print('While')
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next
                condition_node = Parser.parseRelExpression()
                token_atual = Parser.tokenizer.next
                if token_atual.type == 'LINE':
                    # print('Pulou linha while')
                    Parser.tokenizer.selectNext()
                    while_statement_list = []
                    token_atual = Parser.tokenizer.next
                    while token_atual.type!='END':
                        while_statement_list.append(Parser.parseStatement())
                        # Parser.tokenizer.selectNext()
                        token_atual = Parser.tokenizer.next
                    this_node = While([condition_node, Block(while_statement_list)])

                    Parser.tokenizer.selectNext()
                else:
                    raise ValueError('Não pulou linha')
                    
            elif token_atual.type == 'IF':
                # print('If')
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next
                condition_node = Parser.parseRelExpression()
                token_atual = Parser.tokenizer.next
                if token_atual.type == 'LINE':
                    # print('Pulou linha if')
                    Parser.tokenizer.selectNext()
                    if_statement_list = []
                    token_atual = Parser.tokenizer.next
                    while token_atual.type!='END' and token_atual.type!='ELSE':
                        if_statement_list.append(Parser.parseStatement())
                        # Parser.tokenizer.selectNext()
                        token_atual = Parser.tokenizer.next
                        # print(f'Bloco if: {token_atual.type}')
                    if token_atual.type=='ELSE':
                        # print('Else')
                        Parser.tokenizer.selectNext()
                        token_atual = Parser.tokenizer.next
                        if token_atual.type == 'LINE':
                            # print('Pulou linha else')
                            #if com 3 filhos
                            Parser.tokenizer.selectNext()
                            else_statement_list = []
                            token_atual = Parser.tokenizer.next
                            while token_atual.type!='END':
                                else_statement_list.append(Parser.parseStatement())
                                token_atual = Parser.tokenizer.next
                                # Parser.tokenizer.selectNext()
                            this_node = If([condition_node, Block(if_statement_list), Block(else_statement_list)])
                        else:
                            raise ValueError('Não pulou linha')
                    else:
                        #if com 2 filhos
                        this_node = If([condition_node, Block(if_statement_list)])

                    Parser.tokenizer.selectNext()
                else:
                    raise ValueError('Não pulou linha')

            token_atual = Parser.tokenizer.next
            # print(f'Saída statement: {token_atual.type}')
            if token_atual.type == 'LINE' or token_atual.type == 'EOF':
                Parser.tokenizer.selectNext()
                return this_node
            else:
                raise ValueError(r'A linha não acabou com um \n')
    
    @staticmethod
    def parseRelExpression():
        this_node = Parser.parseExpression()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'EQUAL' or token_atual.type == 'GREATER' or token_atual.type == 'LESSER':
            # print('Binop')
            Parser.tokenizer.selectNext()
            this_node = BinOp(token_atual.value,[this_node,Parser.parseExpression()])
            token_atual = Parser.tokenizer.next  

        return this_node
    
    @staticmethod
    def parseExpression():
        this_node = Parser.parseTerm()
        token_atual = Parser.tokenizer.next
        while token_atual.type == 'PLUS' or token_atual.type == 'MINUS' or token_atual.type == 'OR' or token_atual.type == 'CONCAT':
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
        while token_atual.type == 'MULT' or token_atual.type == 'DIV' or token_atual.type == 'AND':
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
        elif token_atual.type == 'STRING':
            # print('Inteiro')
            # resultado = token_atual.value
            Parser.tokenizer.selectNext()
            this_node = StrVal(token_atual.value)

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

        elif token_atual.type == 'NOT':
            # print('Menos')
            Parser.tokenizer.selectNext()
            this_node = UnOp('!', [Parser.parseFactor()])

        elif token_atual.value == '(':
            # print('(')
            Parser.tokenizer.selectNext()
            this_node = Parser.parseRelExpression()
            token_atual = Parser.tokenizer.next
            if token_atual.value != ')':
                raise ValueError('Não fechou parênteses!')
            # print(')')
            Parser.tokenizer.selectNext()

        elif token_atual.value == 'readline':
            Parser.tokenizer.selectNext()
            token_atual = Parser.tokenizer.next
            if token_atual.value != '(':
                raise ValueError('Não abriu parênteses!')
            Parser.tokenizer.selectNext()
            token_atual = Parser.tokenizer.next
            if token_atual.value != ')':
                raise ValueError('Não fechou parêntêses!')
            # print(')')
            this_node = Read()
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
with open(archive, "r") as f:
    codigo = f.read()
    # create new file args[1].split(".")[0] + ".asm" file
    with open(archive.split(".")[0] + ".asm", "w") as f:
        lines = '''
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer
'''
        f.write(lines)

    parser.run(codigo)
    
    with open(archive.split(".")[0] + ".asm", "a") as f:
        lines = '''
; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
        '''
        f.write(lines)

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
#parser = Parser()
#print(parser.run('2+5*4'))

# with open('teste.jl', 'r') as file:
#     archive_content = file.read()
# words = [archive_content]
# for word in words:
#     print(word)

    # prepro = PrePro()
    # code_filtered = prepro.filter(word)

    # tokenizer = Tokenizer(code_filtered)
    # tokenizer.selectNext()
    # print(f'{tokenizer.next.type}: {tokenizer.next.value}')
    # while (tokenizer.next.type!='EOF'):
    #     tokenizer.selectNext()
    #     print(f'{tokenizer.next.type}: {tokenizer.next.value}')

    #parser.run(word)

#     lines = '''
# MOV EBX, 3
# POP EAX
# ADD EAX, EBX'''
#     AssemblyHandler.write(lines)

    #print('-------------------------')