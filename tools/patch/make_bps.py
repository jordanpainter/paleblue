"""Make a BPS patch from vanilla Pokémon Blue to Pale Blue, so players can patch their own ROM.

Usage: python3 tools/patch/make_bps.py VANILLA.gbc PALEBLUE.gbc OUT.bps
Same-size ROMs, so it only needs BPS's two simplest actions: SourceRead (keep these bytes)
and TargetRead (write these new ones). Spec: https://www.romhacking.net/documents/746/
"""
import sys
import zlib


def number(n):
    """BPS variable-length number."""
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            return out
        out.append(x)
        n -= 1


def make(source, target, metadata=b""):
    assert len(source) == len(target), "ROMs differ in size"
    out = bytearray(b"BPS1") + number(len(source)) + number(len(target)) + number(len(metadata)) + metadata
    i, n = 0, len(target)
    while i < n:
        j = i
        same = source[i] == target[i]
        # a short run of equal bytes inside a changed stretch isn't worth its own action
        while j < n and (source[j] == target[j]) == same:
            j += 1
        length = j - i
        if same:
            out += number(((length - 1) << 2) | 0)  # SourceRead
        else:
            out += number(((length - 1) << 2) | 1) + target[i:j]  # TargetRead
        i = j
    for data in (source, target):
        out += zlib.crc32(data).to_bytes(4, "little")
    out += zlib.crc32(out).to_bytes(4, "little")
    return bytes(out)


def apply(patch, source):
    """Minimal applier for the two actions above, to check a patch round-trips."""
    assert patch[:4] == b"BPS1"
    pos = 4

    def read():
        nonlocal pos
        data, shift = 0, 1
        while True:
            x = patch[pos]; pos += 1
            data += (x & 0x7F) * shift
            if x & 0x80:
                return data
            shift <<= 7
            data += shift
    read(); size = read()
    meta = read()  # not "pos += read()": that reads pos before read() moves it
    pos += meta
    out = bytearray()
    while pos < len(patch) - 12:
        d = read()
        action, length = d & 3, (d >> 2) + 1
        if action == 0:
            out += source[len(out):len(out) + length]
        elif action == 1:
            out += patch[pos:pos + length]; pos += length
        else:
            raise ValueError("unsupported action")
    assert len(out) == size and zlib.crc32(out).to_bytes(4, "little") == patch[-8:-4]
    return bytes(out)


if __name__ == "__main__":
    src, tgt = open(sys.argv[1], "rb").read(), open(sys.argv[2], "rb").read()
    patch = make(src, tgt)
    assert apply(patch, src) == tgt
    open(sys.argv[3], "wb").write(patch)
    print(f"wrote {sys.argv[3]}: {len(patch)} bytes, round-trip checked")
