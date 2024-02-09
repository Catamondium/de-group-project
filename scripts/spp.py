#!/usr/bin/env python3
import re
from io import TextIOWrapper as TFile
from typing import Dict


def template(infile: TFile, outfile: TFile, vars: Dict[str, str]):
    for line in infile:
        for sym, val in vars.items():
            line = line.replace(sym, val)
        outfile.write(line)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    def kvpair(arg):
        return arg.split('=')

    parser = ArgumentParser(
        description="Simple PreProcessor, substitution based")

    parser.add_argument('infile', type=FileType(encoding='utf-8'))
    parser.add_argument('outfile', type=FileType('wt'))
    parser.add_argument('pairs', type=kvpair, nargs='*',
                        help='macro variables')

    args = parser.parse_args()
    vars = {key.upper(): value for key, value in args.pairs}
    template(args.infile, args.outfile, vars)
