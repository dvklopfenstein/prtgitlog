#!/usr/bin/env python3

from argparse import ArgumentParser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    print(args)

def get_argparser():
    """Argument parser for Python wrapper of 'git log'"""
    parser = ArgumentParser(
        prog='gitlog',
        description='Concise "git log" for each affected file', add_help=True)
    parser.add_argument('filename')
    parser.add_argument('-g', '--group', choices=['day', 'week', 'year', 'all'])
    parser.add_argument('--au', action='store_false')
    return parser

if __name__ == '__main__':
    main()
