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
gubbins 1-10 --solo --prefix AX | ungubbins
```

Gubbins has several interesting features.  A Gubbins Serial
* is human-friendly,
* ignores case,
* fixes up typos,
* can be reversed,
* contains a checksum,
* avoids collisions, &
* attempts to prevent enumeration.

Modifying any of Prefix, ID, or Additional Data results in a different
Serial.

Gubbins uses a lightly modified
[z-base-32](https://philzimmermann.com/docs/human-oriented-base-32-encoding.txt)
alphabet, with the letters `AJNRTUV` canonically upper-case and all other
letters lower-case.  The validator will automatically fix up typos related
to `oO0`, `iIlL1`, & `zZ2`.

For best results,
* a Prefix can not contain the characters `-oOiIlLzZ`,
* IDs should not be sequential, &
* Additional Data may depend on the Prefix but must not be derived from it.

Note: we make no security claims about Gubbins. YMMV

Requires
* [more_itertools](https://github.com/erikrose/more-itertools),
* [anybase32](https://github.com/alanblevins/anybase32), &
* [pynumparser](https://gitlab.com/n2vram/pynumparser).

License: [MIT](https://opensource.org/licenses/MIT)
