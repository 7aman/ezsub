#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub import const
from ezsub.utils import to_screen
from ezsub.cli.arguments import CliArgs
from ezsub.errors import JobDone, WrongLineNumberError


def history(argv):
    req = CliArgs(argv)
    if req.command not in ['history', 'h']:
        add_to_history(argv)
        return req
    else:
        if not req.subcommand or req.subcommand == 'show':
            show_history()
        elif req.subcommand == 'run':
            return get_from_history(req.line)
    return None


def add_to_history(argv):
    command = ' '.join(argv) + '\n'
    path = const.HISTORY
    if not path.exists():
        with open(path, 'w') as file:
            file.writelines(command)
    else:
        with open(path, 'r') as file:
            commands = file.readlines()
        if not command == commands[0]:
            commands.insert(0, command)
        with open(path, 'w') as file:
            file.writelines(commands)
    return None


def show_history():
    with open(const.HISTORY, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        to_screen(f'{i+1}: ezsub {line}', end='')
    raise JobDone

def get_from_history(linenumber):
    with open(const.HISTORY, 'r') as file:
        commands = file.readlines()
    if linenumber <= len(commands):
        command = commands[linenumber-1]
        return CliArgs(command.split())
    else:
        raise WrongLineNumberError
