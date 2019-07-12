#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

from .gubbins import Gubbins

if __name__ == "__main__":
    from sys import stdin
    from argparse import ArgumentParser
    from pynumparser import NumberSequence
    from itertools import chain

    parser = ArgumentParser()
    parser.add_argument("-p", "--prefix", help="serial prefix", default="A0")
    parser.add_argument("-s", "--solo", help="only output serial", action="store_true")
    parser.add_argument("-v", "--validate", help="validate generator", action="store_true")
    parser.add_argument("args", nargs="*", type=NumberSequence(limits=(0, 2**32 - 1)))
    args = parser.parse_args()

    for i in chain.from_iterable(args.args or map(lambda line: map(lambda line: int(line,0), line.split()), stdin)):
        serial = Gubbins.generate(args.prefix, i)

        if args.validate:
            validation = (args.prefix, i)
            assert validation == Gubbins.validate(serial)
            assert validation == Gubbins.validate(serial.upper())
            assert validation == Gubbins.validate(serial.lower())

        if args.solo:
            print(serial)
        else:
            print(i, serial)

#
