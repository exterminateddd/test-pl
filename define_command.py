def define_command(lines: list, index: int):
    command = 'aaa'
    content = lines[index]
    if lines[index].startswith('$'):
        content = content.split('$')[-1]
    if content.startswith('log'):
        command = 'log'
    elif content.startswith('insert'):
        command = 'insert'
    elif content.startswith('let'):
        command = 'let'
    elif content.startswith('function'):
        command = 'function'
    elif content.startswith('wait'):
        command = 'wait'
    elif content.startswith('stop'):
        command = 'stop'
    elif content.startswith('error'):
        command = 'error'
    elif content.startswith('call'):
        command = 'call'
    elif content.startswith('repeat'):
        command = 'repeat'
    elif content.startswith('passby'):
        command = 'passby'
    elif content.startswith('if'):
        command = 'condition'
    return {'command': f'{command}', 'index': f'{index}'}


def define_command_from_function_by_content(line: str):
    command_2 = None
    if line.startswith('$'):
        line = line[1:]
    if line.startswith('log'):
        command = 'log'
    elif line.startswith('insert'):
        command = 'insert'
    elif line.startswith('let'):
        command = 'let'
    elif line.startswith('function'):
        command = 'function'
    if command_2:
        return {'command': f'{command_2}'}
