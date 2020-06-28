import string
from collections import deque


def parse_variable_assignment(input_string, my_vars):
    input_list = input_string.split('=')
    input_list = [input_str.strip() for input_str in input_list]
    if len(input_list) != 2:
        print('Invalid assignment')
    else:
        var_name = input_list[0]
        var_value = input_list[1]
        if not var_name.isalpha():
            print('Invalid identifier')
        elif not var_value.isdigit() and not var_value.isalpha():
            print('Invalid assignment')
        elif var_value.isalpha():
            if var_value in my_vars:
                my_vars[var_name] = my_vars[var_value]
            else:
                print('Unknown variable')
        elif var_value.isdigit():
            my_vars[var_name] = int(var_value)
    return my_vars


def parse_command(input_string):
    if input_string == '/exit':
        keep_going = False
        print('Bye!')
    elif input_string == '/help':
        keep_going = True
        print('The program calculates the sum of numbers')
    else:
        keep_going = True
        print('Unknown command')
    return keep_going


def normalize_input(input_string, my_vars):
    input_string = input_string.replace('(', ' ( ').replace(')', ' ) ')
    input_list = input_string.split()

    normalized_input_list = []
    unknown_variable = False
    invalid_identifier = False
    imbalanced_parentheses = False
    parentheses = 0

    for input_str in input_list:
        if input_str.isdigit() or input_str.isalpha():  # Digit/variable
            if input_str.isdigit():
                normalized_input_list.append(int(input_str))
            elif input_str.isalpha():
                if input_str in my_vars:
                    normalized_input_list.append(my_vars[input_str])
                else:
                    print('Unknown variable')
                    unknown_variable = True
            else:
                print('Invalid identifier')
                invalid_identifier = True
        else:  # Operator
            if '+' in input_str:
                normalized_input_list.append('+')
            elif '*' in input_str:
                normalized_input_list.append('*')
            elif '-' in input_str:
                if input_str.count('-') % 2 == 0:
                    normalized_input_list.append('+')
                else:
                    normalized_input_list.append('-')
            else:
                if input_str == '(':
                    parentheses += 1
                elif input_str == ')':
                    parentheses -= 1
                if parentheses < 0:
                    print('Invalid expression')
                    imbalanced_parentheses = True
                normalized_input_list.append(input_str)
    if parentheses != 0:
        print('Invalid expression')
        imbalanced_parentheses = True
    if not unknown_variable and not invalid_identifier and not imbalanced_parentheses:
        return normalized_input_list


def make_reverse_polish_list(normalized_input_list):
    operators = deque()
    priority = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    reverse_polish_list = []
    for el in normalized_input_list:
        if type(el) == int:
            reverse_polish_list.append(el)
        elif len(operators) == 0 or operators[-1] == '(':
            operators.append(el)
        elif el in priority and priority[el] > priority[operators[-1]]:
            operators.append(el)
        elif el in priority and priority[el] <= priority[operators[-1]]:
            keep_popping = True
            while keep_popping:
                reverse_polish_list.append(operators.pop())
                if len(operators) == 0 or priority[el] > priority[operators[-1]] or operators[-1] == '(':
                    keep_popping = False
                    operators.append(el)
        elif el == '(':
            operators.append(el)
        elif el == ')':
            keep_popping = True
            while keep_popping:
                reverse_polish_list.append(operators.pop())
                if operators[-1] == '(':
                    keep_popping = False
                    operators.pop()
    while len(operators) > 0:
        reverse_polish_list.append(operators.pop())
    return reverse_polish_list


def compute_answer(rp_list):
    holding = deque()
    for el in rp_list:
        if type(el) == int:
            holding.append(el)
        else:
            operand1 = holding.pop()
            operand2 = holding.pop()
            if el == '+':
                holding.append(operand2 + operand1)
            elif el == '-':
                holding.append(operand2 - operand1)
            elif el == '*':
                holding.append(operand2 * operand1)
            elif el == '/':
                holding.append(operand2 / operand1)
    return int(holding[-1])


def main():
    keep_going = True
    my_vars = {}
    while keep_going:
        input_string = input()
        if len(input_string) == 0:
            continue
        elif input_string[0] == '/':
            keep_going = parse_command(input_string)
        elif '=' in input_string:
            my_vars = parse_variable_assignment(input_string, my_vars)
        else:
            normalized_input_list = normalize_input(input_string, my_vars)
            if normalized_input_list:
                rp_list = make_reverse_polish_list(normalized_input_list)
                print(compute_answer(rp_list))


main()

# def parse_add_subtract_string(input_string, my_vars):
#     input_list = input_string.split()
#     input_ints = []
#     unknown_variable = False
#     invalid_identifier = False

#     for input_str in input_list[::2]:
#         if input_str.isdigit():
#             input_ints.append(int(input_str))
#         elif input_str.isalpha():
#             if input_str in my_vars:
#                 input_ints.append(my_vars[input_str])
#             else:
#                 print('Unknown variable')
#                 unknown_variable = True
#         else:
#             print('Invalid identifier')
#             invalid_identifier = True

#     if not unknown_variable and not invalid_identifier:
#         if len(input_ints) == 1:
#             return input_ints
#         else:
#             operations = input_list[1::2]
#             try:
#                 operations = ['+' if operation.count('-') % 2 == 0 else '-' for operation in operations]
#                 signs = [1] + [1 if operation == '+' else -1 for operation in operations]
#             except (ValueError, TypeError):
#                 print('Invalid expression')
#             else:
#                 return [signs[i] * input_ints[i] for i in range(len(signs))]
