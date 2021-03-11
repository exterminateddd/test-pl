import errors
from define_command import *
import time
import sys

file = open(sys.argv[1], "r", encoding='UTF-8').read()

lines = file.split('\n')


variables = {}
functions = {}


def split(word):
    return [char for char in word]


lines = [l for l in lines if l != '']


if not lines:
    exit('Пустой файл')


def math(expression):
    for char in expression:
        if char.isalpha():
            raise errors.expectedNumber
    try:
        return eval(f'{expression}')
    except SyntaxError:
        pass


def reformat_string(var_repr: str):
    var_repr_new = var_repr
    if var_repr.count('%') >= 2:
        for i in range(var_repr_new.count('%')//2):
            open_pos = var_repr_new.find('%')
            close_pos = var_repr_new.find('%', open_pos+1)
            var_list = []
            for k, v in variables.items():
                var_list.append(k)
            if var_repr_new[open_pos+1:close_pos] in var_list:
                var_repr_new = var_repr_new.replace(var_repr_new[open_pos:close_pos+1], str(variables[var_repr_new[open_pos+1:close_pos]]))
            elif ' ' not in var_repr_new[open_pos+1:close_pos]:
                raise errors.unknownVariable
    elif var_repr.count('%') % 2 != 0 and var_repr[var_repr.find('%')+1] != ' ' and var_repr[var_repr.find('%')+1] != '.':
        raise errors.expectedReformatClosure
    open_pos_str = -666
    close_pos_str = -666
    if var_repr_new.count("'") >= 2:
        for i in range(var_repr_new.count("'")//2):
            open_pos_str = var_repr_new.find("'")
            close_pos_str = var_repr_new.find("'", open_pos_str+1)
            var_repr_new.replace(var_repr_new[open_pos_str:close_pos_str+1], str(var_repr_new[open_pos_str:close_pos_str+1]))
    open_pos_digit = -666
    close_pos_digit = -666
    if var_repr_new.count('~') >= 2:
        for i in range(var_repr_new.count('~')//2):
            open_pos_digit = var_repr_new.find('~')
            close_pos_digit = var_repr_new.find('~', open_pos_digit+1)
            if var_repr_new[open_pos_digit:close_pos_digit] not in var_repr_new[open_pos_str:close_pos_str]:
                digit_expr = var_repr_new[open_pos_digit+1:close_pos_digit]
                var_repr_new = var_repr_new.replace(var_repr_new[open_pos_digit:close_pos_digit+1], str(math(digit_expr)))
    return var_repr_new


def log(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    log_ref = content.split(' ', 1)
    if len(log_ref[1]) > 1 or log_ref[-1] != '':
        if log_ref[1]:
            print(reformat_string(log_ref[1]))
        else:
            raise errors.emptyVariable
    else:
        raise errors.expectedString


def insert(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if 'to' in content:
        var_list = []
        for k, v in variables.items():
            var_list.append(k)
        insert_ref = content.split(' ', 1)[1]
        insert_var = content.rsplit(' ', 1)[1]
        insert_text = reformat_string(insert_ref[:insert_ref.rfind('to')])
        if insert_var in var_list:
            variables[insert_var] = input(insert_text)
        else:
            raise errors.unknownVariable
    else:
        raise errors.expectedTargetVariable


def wait(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    time.sleep(int(content.split(' ', 1)[1]))


def stop(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    close_code = ''
    if content.strip() != 'stop':
        close_code = content.split(' ', 1)[1]
    else:
        raise errors.expectedString
    exit(close_code)


def error(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if content.strip() != 'error':
        raise Exception(content.split(' ', 1)[1])
    else:
        raise errors.expectedString


def let(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if '=' in content:
        statement_1 = content.split(' ', 1)[1]
        statement = statement_1.split('=')
        for y in range(len(statement)):
            statement[y] = statement[y].strip()
        statement_key = statement[0]
        statement_value = statement[1]
        variables[f'{statement_key}'] = reformat_string(statement_value)
    else:
        raise errors.expectedStatement


def function(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if lines[index+1].startswith('$') and content.endswith(':'):
        func_name = content.split(' ', 1)[1][:-1]
        func_commands = []
        for l in range(len(lines)):
            if l > index:
                if lines[l].startswith('$'):
                    func_commands.append(l)
                else:
                    break
        functions[func_name] = []
        for i in func_commands:
            functions[func_name].append(i)
    else:
        raise errors.emptyFunction


def call(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if content.strip().split(' ', 1)[1] in functions.keys():
        for c in list(functions[content.strip().split(' ', 1)[1]]):
            exec(define_command(lines, c)['command'] + '(' + define_command(lines, c)['index'] + ')')


def passby(index):
    pass


def condition(index):
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if content.strip() != 'if' and 'then' in content:
        if_statement = content.split(' ', 1)[1].split('then', 1)[0]
        if_func_name = content.strip().split(' ')[-1]
        if eval(str(reformat_string(if_statement))):
            if if_func_name.strip() in functions.keys():
                for c in list(functions[if_func_name]):
                    exec(define_command(lines, c)['command'] + '(' + define_command(lines, c)['index'] + ')')


for i in range(len(lines)):
    try:
        if not lines[i].startswith('$'):
            exec(define_command(lines, i)['command']+'('+define_command(lines, i)['index']+')')
    except NameError:
        pass
