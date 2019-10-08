#!/usr/bin/env python3
# SPDX-License-Identifier: Unlicense

from gubbins import Gubbins

for i in range(10):
    serial = Gubbins.generate("AX", i)
    prefix, id = Gubbins.validate(serial)
    assert prefix.lower() == "AX".lower()
    assert id == i
    print(i, serial)
