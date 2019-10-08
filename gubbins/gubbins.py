# SPDX-License-Identifier: MIT

from functools import reduce, partial
from more_itertools import sliced

class Gubbins:
    __mask = 2**32 - 1
    __separator = '-'
    __alphabet = b"ybndrfg8ejkmcpqxot1uwvsza345h769" # modified zbase32
    __normalizer = str.maketrans(
        "0O2ZiIlL ABCDEFGHJKMNPQRSTUVWXY",
        "oozz1111 abcdefghjkmnpqrstuvwxy",
        )
    __prefix_fixer = str.maketrans(
        "oOiIlLzZ",
        "00111122",
        )
    __formatter = str.maketrans(
        "ajnrtuv BCDEFGHIKLMOPQSWXYZ",
        "AJNRTUV bcdefghiklmopqswxyz",
        )
    __checksum = partial(reduce, lambda x,y: x^y)

    from hashlib import shake_128 as __hash
    from anybase32 import encode as __encode, decode as __decode

    class Error(Exception): pass
    class ChecksumError(Error): pass

    @staticmethod
    def __prefix_to_seed(prefix, ad):
        assert prefix == Gubbins._fix_prefix(prefix)
        if ad is not None:
            prefix = "-".join((ad, prefix))
        hash = Gubbins.__hash(prefix.lower().encode()).digest(4)
        seed = int.from_bytes(hash, byteorder='big')
        checksum = Gubbins.__checksum(hash)
        return seed, checksum

    @staticmethod
    def __hash_id(x):
        assert 0 <= x <= Gubbins.__mask
        x += 1
        x ^= (x >> 17)
        x *= 0xed5ad4bb
        x &= Gubbins.__mask
        x ^= (x >> 11)
        x *= 0xac4c1b51
        x &= Gubbins.__mask
        x ^= (x >> 15)
        x *= 0x31848bab
        x &= Gubbins.__mask
        x ^= (x >> 14)
        assert 0 <= x <= Gubbins.__mask
        return x

    @staticmethod
    def __unhash_id(x):
        assert 0 <= x <= Gubbins.__mask
        x ^= (x >> 14) ^ (x >> 28)
        x *= 0x32b21703
        x &= Gubbins.__mask
        x ^= (x >> 15) ^ (x >> 30)
        x *= 0x469e0db1
        x &= Gubbins.__mask
        x ^= (x >> 11) ^ (x >> 22)
        x *= 0x79a85073
        x &= Gubbins.__mask
        x ^= (x >> 17)
        x -= 1
        assert 0 <= x <= Gubbins.__mask
        return x

    @staticmethod
    def _fix_prefix(prefix):
        return prefix.translate(Gubbins.__prefix_fixer).translate(Gubbins.__formatter)

    @staticmethod
    def prefix(serial):
        return serial.split(Gubbins.__separator)[0].translate(Gubbins.__prefix_fixer).translate(Gubbins.__formatter)

    @staticmethod
    def generate(prefix, id, ad=None):
        prefix = Gubbins._fix_prefix(prefix)
        prefix_seed, prefix_checksum = Gubbins.__prefix_to_seed(prefix, ad)

        assert 0 <= id <= Gubbins.__mask
        id_point = prefix_seed ^ Gubbins.__hash_id(prefix_seed ^ id)
        id_bytes = id_point.to_bytes(length=4, byteorder='big')
        checksum = prefix_checksum ^ Gubbins.__checksum(id_bytes)
        id_bytes += bytes((checksum,))
        assert prefix_checksum == Gubbins.__checksum(id_bytes)

        id_value = Gubbins.__encode(id_bytes, Gubbins.__alphabet).decode()
        return Gubbins.__separator.join((prefix, *sliced(id_value, 4))).translate(Gubbins.__formatter)

    @staticmethod
    def canonicalize(serial, ad=None):
        prefix, id = Gubbins.validate(serial, ad)
        return Gubbins.generate(prefix, id, ad)

    @staticmethod
    def validate(serial, ad=None):
        prefix, *id_chunks = serial.split(Gubbins.__separator)
        prefix = Gubbins._fix_prefix(prefix)
        prefix_seed, prefix_checksum = Gubbins.__prefix_to_seed(prefix, ad)

        id_value = ''.join(id_chunks).translate(Gubbins.__normalizer)
        id_bytes = Gubbins.__decode(id_value.encode(), Gubbins.__alphabet)
        if prefix_checksum != Gubbins.__checksum(id_bytes):
            raise Gubbins.ChecksumError()

        assert 5 == len(id_bytes)

        id_point = int.from_bytes(id_bytes[:-1], byteorder='big')
        id = prefix_seed ^ Gubbins.__unhash_id(prefix_seed ^ id_point)
        assert 0 <= id <= Gubbins.__mask

        return prefix, id

#
