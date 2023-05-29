import sys

class symbolTable():
    def __init__(self):
        self.table = {}

    def getter(self, name):
        if name not in self.table.keys():
            raise ValueError(f'Variável {name} não declarada!')
        return self.table[name]

    def setter(self, name, valueTuple):
        this_type, this_value = self.table[name]
        new_type, new_value = valueTuple

        if new_type == 'str':
            new_type = 'string'

        if name not in self.table.keys():
            raise ValueError('Variável não declarada!')
        
        if new_type != this_type:
            raise ValueError('Variável recebeu tipo errado!')

        self.table[name] = (this_type, new_value)

    def create(self, name, type):
        if name in self.table.keys():
            raise ValueError('Variável já declarada!')
        self.table[name] = (type, None)


class funcTable():
    table = {}
    def getter(name):
        if name not in funcTable.table.keys():
            raise ValueError(f'Variável {name} não declarada!')
        return funcTable.table[name]

    def setter(name, valueTuple):
        this_type, this_value = funcTable.table[name]
        new_type, new_value = valueTuple

        if new_type == 'str':
            new_type = 'string'

        if name not in funcTable.table.keys():
            raise ValueError('Função não declarada!')
        
        if new_type != this_type:
            raise ValueError('Função recebeu tipo errado!')

        funcTable.table[name] = (this_type, new_value)

    def create(name, type):
        if name in funcTable.table.keys():
            raise ValueError('Função já declarada!')
        funcTable.table[name] = (type, None)
            

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self):
        pass

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, table):
        # print(f'UnOp {self.value}')
        if self.value=='-':
            return ('int',-self.children[0].evaluate(table))
        if self.value=='+':
            return ('int',self.children[0].evaluate(table))
        if self.value=='!':
            return ('int',not self.children[0].evaluate(table))

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, table):
        # print(f'Int Valor {self.value}')
        return ('int',self.value)
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, table):
        # print(f'Str Valor {self.value}')
        return ('str', self.value)

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self, table):
        super().evaluate()

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self, table):
        # print(f'BinOp {self.value}')
        if self.value=='.':
            return ('str', str(self.children[0].evaluate(table)[1]) + str(self.children[1].evaluate(table)[1]))
        else:
            if self.children[0].evaluate(table)[0]=='int' and self.children[1].evaluate(table)[0]=='int':
                if self.value=='+':
                    return ('int',self.children[0].evaluate(table)[1] + self.children[1].evaluate(table)[1])

                if self.value=='-':
                    return ('int',self.children[0].evaluate(table)[1] - self.children[1].evaluate(table)[1])

                if self.value=='*':
                    return ('int',self.children[0].evaluate(table)[1] * self.children[1].evaluate(table)[1])

                if self.value=='/':
                    return ('int',int(self.children[0].evaluate(table)[1] // self.children[1].evaluate(table)[1]))
                
                if self.value=='||':
                    return ('int',int(self.children[0].evaluate(table)[1] or self.children[1].evaluate(table)[1]))
                
                if self.value=='&&':
                    return ('int',int(self.children[0].evaluate(table)[1] and self.children[1].evaluate(table)[1]))
                
                if self.value=='==':
                    return ('int',int(self.children[0].evaluate(table)[1] == self.children[1].evaluate(table)[1]))
                
                if self.value=='>':
                    return ('int',int(self.children[0].evaluate(table)[1] > self.children[1].evaluate(table)[1]))
                
                if self.value=='<':
                    return ('int',int(self.children[0].evaluate(table)[1] < self.children[1].evaluate(table)[1]))
            else:
                if self.value == '==':
                    return ("Int", int(self.children[0].evaluate(table)[1] == self.children[1].evaluate(table)[1]))
                elif self.value == '>':
                    return ("Int", int(self.children[0].evaluate(table)[1] > self.children[1].evaluate(table)[1]))
                elif self.value == '<':
                    return ("Int", int(self.children[0].evaluate(table)[1] < self.children[1].evaluate(table)[1]))
                else:
                    raise ValueError('Erro de operação binária')
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])
    def evaluate(self, table):
        # print(f'Variavel {self.value}')
        return table.getter(self.value)
    
class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self, table):
        # print('Print')
        print(self.children[0].evaluate(table)[1])

class Read(Node):
    def __init__(self):
        super().__init__(None, [])
    def evaluate(self, table):
        # print('Read')
        return ('int', int(input()))

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def evaluate(self, table):
        # print(f'Create {self.value} {self.children[0].value} = {self.children[-1].evaluate()}')
        table.create(self.children[0].value, self.value)
        table.setter(self.children[0].value, self.children[-1].evaluate(table))
        # else:
        #     if self.value == 'String':
        #         symbolTable.create(self.children[0].value, self.value, "")
        #     elif self.value == 'Int':
        #         symbolTable.create(self.children[0].value, self.value, 0)

class While(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self, table):
        # print('While')
        while self.children[0].evaluate(table)[1]:
            self.children[1].evaluate(table)

class If(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self, table):
        # print('If')
        if self.children[0].evaluate(table):
            self.children[1].evaluate(table)
        else:
            if len(self.children)==3:
               self.children[2].evaluate(table) 


class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self, table):
        # print('Assignment')
        table.setter(self.children[0].value, self.children[1].evaluate(table))

class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def evaluate(self, table):
        # print(f'Block')
        for statement in self.children:
            if statement.value == 'return':
                return statement.evaluate(table)
            statement.evaluate(table)
        

class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, table):
        funcTable.create(self.children[0].value, self)

class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, table): 
        funcNode = funcTable.getter(self.value)

        if len(funcNode.children) - 2 != len(self.children):
            raise Exception("Erro de número de argumentos")
        
        SymbolTableFunc = symbolTable()
        if len(funcNode.children) > 2:
            for i in range(1, len(funcNode.children) - 1):
                SymbolTableFunc.create(funcNode.children[i], funcNode.children[i].evaluate(SymbolTableFunc))
                SymbolTableFunc.setter(funcNode.children[i].children[0].value, self.children[i-1].evaluate(table))
            
            return funcNode.children[-1].evaluate(SymbolTableFunc)
        else:
            return funcNode.children[-1].evaluate(SymbolTableFunc)

class Return(Node):
    def __init__(self, children):
        super().__init__("return", children)
        
    def evaluate(self, table):
        return self.children[0].evaluate(table)     



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
        operationsTokens = ['+', '-', '/', '*', '(', ')','=','>','<','|','&','!',':','.',',']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        reservedWords = ['println','if','else','while','readline','end','Int','String','return','function']

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
            elif c == ",":
                self.next = Token(',', 'COMMA')

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

                elif Parser.tokenizer.next.value == '(':
                    Parser.tokenizer.selectNext()
                    token_atual = Parser.tokenizer.next
                    funcArgs = []

                    while token_atual.value != ')':
                        funcArgs.append(Parser.parseRelExpression())
                        token_atual = Parser.tokenizer.next
                    
                        if token_atual.type == 'COMMA':
                            Parser.tokenizer.selectNext()
                            token_atual = Parser.tokenizer.next
                        else:
                            break
                            
                            
                    if token_atual.value != ')':
                        raise ValueError('Erro ao chamar função.')

                    this_node = FuncCall(iden_name, funcArgs)

                else:
                    raise ValueError('Erro ao declarar variável.')

            elif token_atual.type == 'RETURN':
                Parser.tokenizer.selectNext()
                this_node = Return([Parser.parseRelExpression()])
            
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

            elif token_atual.type == 'FUNCTION':
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next

                if token_atual.type == 'IDEN':
                    iden_name = token_atual.value
                    Parser.tokenizer.selectNext()
                    token_atual = Parser.tokenizer.next

                    if token_atual.value == '(':
                        funcArgs = [Identifier(iden_name)]

                        Parser.tokenizer.selectNext()
                        token_atual = Parser.tokenizer.next

                        while token_atual.value != ')':

                            if token_atual.type == 'IDEN':
                                param_ident = Identifier(token_atual.value)
                                Parser.tokenizer.selectNext()
                                token_atual = Parser.tokenizer.next
                                
                                if token_atual.type == 'DEC':
                                    Parser.tokenizer.selectNext()
                                    token_atual = Parser.tokenizer.next
                                    
                                    if token_atual.type == 'TYPE':
                                        varType = token_atual.value.lower()
                                        Parser.tokenizer.selectNext()
                                        token_atual = Parser.tokenizer.next
                                        if token_atual.type == 'INT':
                                            funcArgs.append(VarDec(varType, [param_ident, IntVal(0)]))
                                        elif varType == 'STRING':
                                            funcArgs.append(VarDec(varType, [param_ident, StrVal("")]))
                                        
                                        if token_atual.type == 'COMMA':
                                            Parser.tokenizer.selectNext()
                                            token_atual = Parser.tokenizer.next
                                            
                                        elif token_atual.value == ')':
                                            break
                                            
                                        else:
                                            raise Exception("Erro de sintaxe")                                    
                                    else:
                                        raise Exception("Erro de sintaxe")
                                else:
                                    raise Exception("Erro de sintaxe")
                            else:
                                raise Exception("Erro de sintaxe")

                        if token_atual.value == ')':
                            Parser.tokenizer.selectNext()
                            token_atual = Parser.tokenizer.next
                            
                            if token_atual.type == 'DEC':
                                Parser.tokenizer.selectNext()
                                token_atual = Parser.tokenizer.next
                                
                                if token_atual.type == 'TYPE':
                                    funcType = Parser.tokenizer.next.value
                                    Parser.tokenizer.selectNext()
                                    token_atual = Parser.tokenizer.next
                                    
                                    if token_atual.type == 'LINE':
                                        Parser.tokenizer.selectNext()
                                        token_atual = Parser.tokenizer.next
                                        
                                        funcStatements = []
                                        while token_atual.type != 'END':
                                            # guarda os statements em uma variavel e depois passa pra children como Block
                                            funcStatements.append(Parser.parseStatement())
                                            token_atual = Parser.tokenizer.next
                                            
                                        funcArgs.append(Block(funcStatements))
                                        
                                        if token_atual.type == 'END':
                                            Parser.tokenizer.selectNext()
                                            token_atual = Parser.tokenizer.next    
                                            this_node =  FuncDec(funcType, funcArgs)
                                        
                                        else:
                                            raise Exception("Erro de sintaxe")
                                    else:
                                        raise Exception("Erro de sintaxe")
                                else:
                                    raise Exception("Erro de sintaxe")
                            else:
                                raise Exception("Erro de sintaxe")
                        else:
                            raise Exception("Erro de sintaxe") 
                    else:
                        raise ValueError('Não abriu parênteses ao declarar função')

                else:
                    raise ValueError('Erro ao declarar função')


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

            if Parser.tokenizer.next.value == '(':
                Parser.tokenizer.selectNext()
                token_atual = Parser.tokenizer.next
                
                funcArgs = []
                while token_atual.value != ')':
                    funcArgs.append(Parser.parseRelExpression())
                    token_atual = Parser.tokenizer.next
                    
                    if token_atual.type == 'COMMA':
                        Parser.tokenizer.selectNext()
                        token_atual = Parser.tokenizer.next
                    else:
                        break
                    
                
                this_node = FuncCall(this_node.value, funcArgs)
                
                if token_atual.value != ')':
                    raise Exception("Não fechou o parênteses")
                
                Parser.tokenizer.selectNext() ### possivel erro
                token_atual = Parser.tokenizer.next ### possivel erro

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
        Parser.symbolTable = symbolTable()

        prepro = PrePro()
        code_filtered = prepro.filter(code)

        Parser.tokenizer = Tokenizer(code_filtered)
        Parser.tokenizer.selectNext()

        parent_node = Parser.parseBlock()
        result = parent_node.evaluate(Parser.symbolTable)

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
# print(parser.run('2+5*4'))

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

    # parser.run(word)

    # print('-------------------------')