#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

from .gubbins import Gubbins

if __name__ == "__main__":
    from sys import stdin
    from argparse import ArgumentParser
    from pynumparser import NumberSequence
    from itertools import chain

    parser = ArgumentParser()
    parser.add_argument("-p", "--prefix", help="require specific serial prefix")
    parser.add_argument("-s", "--solo", help="only output parsed results", action="store_true")
    parser.add_argument("-v", "--validate", help="validate validator", action="store_true")
    parser.add_argument("args", nargs="*")
    args = parser.parse_args()

    for serial in args.args or chain.from_iterable(map(lambda line: line.split(), stdin)):
        prefix, id = Gubbins.validate(serial)

        if args.prefix:
            assert prefix.lower() == args.prefix.lower()

        if args.validate:
            assert Gubbins.canonicalize(serial) == Gubbins.generate(prefix, id)

        if args.solo:
            print(':'.join((prefix, str(id))))
        else:
            print(serial, prefix, id)

#
