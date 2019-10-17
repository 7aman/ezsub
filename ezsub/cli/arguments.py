#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import argparse
from pathlib import Path
from ezsub import const
from ezsub.conf import UserConf


logger = logging.getLogger(__name__)

SORT_OPTIONS = ['t', 's', 'n']
# common arguments as a parser
destination = argparse.ArgumentParser(add_help=False)
destination.add_argument(
    '-d',
    '--destination',
    dest='destination',
    metavar="DESTINATION",
    help='Destination folder.')

title = argparse.ArgumentParser(add_help=False)
title.add_argument(
    '-t',
    '--title',
    dest='title',
    metavar="TITLE",
    nargs='+',
    help='Title to search')

lngs = argparse.ArgumentParser(add_help=False)
lngs.add_argument(
    '-l',
    '--lngs',
    dest='lngs',
    nargs='+',
    choices=const.SUPPORTED_LNGS,
    metavar=('LNG1', 'LNG2',),
    help='Language(s) which you are interested in.')

site = argparse.ArgumentParser(add_help=False)
site.add_argument(
    '-s',
    '--site',
    dest='site',
    nargs='+',
    choices=const.MIRRORS,
    metavar=('Site1', 'Site2'),
    help='Site to download from.')


verbose = argparse.ArgumentParser(add_help=False)
verbose.add_argument(
    '-v',
    dest='verbosity',
    action='count',
    help='increase verbosity. use -v, -vv, -vvv ...')

group = argparse.ArgumentParser(add_help=False)
_group = group.add_mutually_exclusive_group()
_group.add_argument(
    '-g',
    dest='group',
    action='store_true',
    help="Extract subtitles to folders like './destination/title/language'")
_group.add_argument(
    '-G',
    dest='group',
    action='store_false',
    help='Extract all subtitles to the root of the destination')

ask = argparse.ArgumentParser(add_help=False)
_ask = ask.add_mutually_exclusive_group()
_ask.add_argument(
    '-a',
    '--auto-select',
    dest='auto_select',
    action='store_true',
    help='Select first title in search results automatically.')
_ask.add_argument(
    '-A',
    '--ask',
    dest='auto_select',
    action='store_false',
    help='Ask user to select best match in search results.')

open_after = argparse.ArgumentParser(add_help=False)
_open = open_after.add_mutually_exclusive_group()
_open.add_argument(
    '-o',
    '--open-after',
    dest='open_after',
    action='store_true',
    help='Open destination folder after.')
_open.add_argument(
    '-O',
    '--no-open-after',
    dest='open_after',
    action='store_false',
    help='Do not open destination folder after.')

examples = f'''
Examples:
{const.PROGRAMNAME} dl -t riverdale third season -l fa en -a
'''


def get_parser():
    parser = argparse.ArgumentParser(
        prog=const.PROGRAMNAME,
        description='Downloads subtitles from subscene and its mirrors',
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
        epilog=examples)

    parser.add_argument(
        "--version",
        action="version",
        version=f'%(prog)s version {const.__version__}',
        help="show version and exit")

    commands = parser.add_subparsers(
        title='commands',
        dest="command",
        metavar='COMMAND')

    download = commands.add_parser(
        'download',
        parents=[title, destination, _open, _ask, _group, site, lngs],
        aliases=['d', 'dl'],
        help='Download subtitles for a given title.')

    _ = commands.add_parser(
        'unzip',
        parents=[title, destination, _open, _ask, _group, lngs],
        aliases=['x', 'ex'],
        help='Extract downloaded title.')

    info = commands.add_parser(
        'info',
        parents=[verbose],
        aliases=['i'],
        help='Show Useful Information.')

    config = commands.add_parser(
        'config',
        parents=[],
        aliases=['cfg'],
        help='Set or reset options in user.conf')

    clean = commands.add_parser(
        'clean',
        parents=[title, lngs, ask],
        help='Delete downloaded subtitles for a title.')

    _ = commands.add_parser(
        'backup',
        parents=[destination, open_after],
        aliases=['b'],
        help='Backup cache folder as a zip file.')

    commands.add_parser(
        'login',
        parents=[],
        aliases=['l'],
        help='Login and get required cookies values.')

    commands.add_parser(
        'update',
        parents=[],
        aliases=['u'],
        help=f"Update {const.PROGRAMNAME} if a new version is available.")

    history = commands.add_parser(
        'history',
        aliases=['h'],
        help='Show or execute previous commands.')



    config_commands = config.add_subparsers(
        dest="subcommand",
        title="subcommand",
        metavar="SUBCOMMAND")
    _ = config_commands.add_parser(
        'show',
        help="show current options.")
    set_command = config_commands.add_parser(
        'set',
        help="Set an option to a value.")
    set_command.add_argument(
        'option',
        metavar="OPTION",
        help="Option to set in form of 'section.option'")
    set_command.add_argument(
        'value',
        metavar="VALUE",
        nargs='+',
        help="Value to set")

    download.add_argument(
        '-S',
        '--simulation',
        dest='simulation',
        action='store_true',
        help='Do not download, just create empty zip files.')

    _sort = info.add_mutually_exclusive_group()
    _sort.add_argument(
        "-t",
        action='store_true',
        dest='title_sort',
        help="sort output based on titles. (only with -v)")
    _sort.add_argument(
        "-n",
        action='store_true',
        dest='number_sort',
        help="sort output based on number of files of a title. (only with -v)")
    _sort.add_argument(
        "-s",
        action='store_true',
        dest='size_sort',
        help="sort output based on size of files of a title. (only with -v)")

    # clean
    clean.add_argument(
        "-0",
        "--zero",
        dest='zero',
        action='store_true',
        help="do not delete, just empty the files.")


    history_commands = history.add_subparsers(
        dest="subcommand",
        title="subcommand",
        metavar="SUBCOMMAND")
    _ = history_commands.add_parser(
        'show',
        help="show current options.")
    run_command = history_commands.add_parser(
        'run',
        help="Run a previous command again.")
    run_command.add_argument(
        'line',
        metavar="LINE",
        type=int,
        default=1,
        help="Line number of history entries to run again.")

    for _, sp in commands.choices.items():
        sp._optionals.title = "Arguments"
    # print(download.format_help())
    return parser


class CliArgs(UserConf):
    def __init__(self, argv):
        super().__init__()
        super().read()
        parser = get_parser()
        args = parser.parse_args(argv)
        self.command = args.command
        # parser.print_usage()
        if args.__contains__('title'):
            if args.title:
                self.title = " ".join(args.title)
            else:
                self.title = ''

        if args.__contains__('lngs'):
            if args.lngs:
                self.lngs = " ".join(args.lngs)

        if args.__contains__('destination'):
            if args.destination:
                self.destination = args.destination

        if args.__contains__('site'):
            if args.site:
                self.site = " ".join(args.site)

        if args.__contains__('group'):
            # TODO: find better logic
            if '-G' in str(argv):
                self.group = args.group
            else:
                self.group = args.group or self.group

        if args.__contains__('auto_select'):
            # TODO: find better logic
            if '-A' in str(argv):
                self.auto_select = args.auto_select
            else:
                self.auto_select = args.auto_select or self.auto_select

        if args.__contains__('open_after'):
            # TODO: find better logic
            if '-O' in str(argv):
                self.open_after = args.open_after
            else:
                self.open_after = args.open_after or self.open_after

        if args.__contains__('zero'):
            self.zero = args.zero

        if args.__contains__('simulation'):
            self.simulation = args.simulation

        if args.__contains__('subcommand'):
            self.subcommand = args.subcommand

        if args.__contains__('option'):
            self.option = args.option

        if args.__contains__('value'):
            self.value = " ".join(args.value)

        if args.__contains__('line'):
            if args.line < 1:
                parser.error("Line number must be an integer greater than zero")
            else:
                self.line = args.line

        if args.__contains__('verbosity'):
            self.verbosity = args.verbosity or 0

        if args.__contains__('number_sort'):
            if args.number_sort:
                self.sort = 'n'
            elif args.size_sort:
                self.sort = 's'
            else:
                self.sort = 't'
