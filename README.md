# gubbins
Serial number generator/validator
======

A simple but powerful serial number generator and validator written in
Python.  Given a Prefix and a 32-bit ID, produces a Serial.  Given a valid
Serial, returns the Prefix and 32-bit ID.  Optionally takes Additional Data.

```python
from gubbins import Gubbins

for i in range(10):
	serial = Gubbins.generate("AX", i)
	prefix, id = Gubbins.validate(serial)
	assert prefix.lower() == "AX".lower()
	assert id == i
	print(i, serial)
```

or via the command-line,

```bash
python3 -m gubbins.generate 1-10 --solo --prefix AX | python3 -m gubbins.validate
```

Requires
* [more_itertools](https://github.com/erikrose/more-itertools),
* [anybase32](https://github.com/alanblevins/anybase32), &
* [pynumparser](https://gitlab.com/n2vram/pynumparser).

License: [MIT](https://opensource.org/licenses/MIT)
