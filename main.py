import sys
import re
def roteiro_0_1 (input_string):
    #Tratando erros:
        # Léxica: - não começar e terminar sem aspas
        #         - qualquer input sem ser um inteiro ou + e -
        #         
        # Sintática: - começar com operação
        #            - duas operações seguidas
        #            - espaço entre dois números ???
        
    operations = ['+', '-']
    input_no_brackets = input_string.replace('"', '')
    if re.search("[^0-9\s+-]", input_no_brackets):
        raise ValueError('Erro Léxico: Argumento possui caracteres inválidos.')
    if re.search('\d\s+\d', input_no_brackets):
        raise ValueError('Erro Sintático: Argumento possui números seguidos.')
    input_no_spaces = input_no_brackets.replace(' ',  '')
    if input_no_spaces[0] in operations or input_no_spaces[-1] in operations:
        raise ValueError('Erro Sintático: Argumento começa ou termina com operação.')
    if re.search('[+-]{2,}',input_no_spaces):
        raise ValueError('Erro Sintático: Argumento com operações seguidas.')

    last_result = 0
    number = ''
    last_operation = ''
    for i, letter in enumerate(input_no_spaces):
        if letter in operations or i == len(input_no_spaces) - 1:
            if letter not in operations:
                number += letter
            if last_operation == operations[0]:
                last_result += int(number)
            elif last_operation == operations[1]:
                last_result -= int(number)
            else:
                last_result = int(number)
            last_operation = letter
            number = ''
        else:
            number += letter
    return last_result

print(roteiro_0_1(sys.argv[1]))