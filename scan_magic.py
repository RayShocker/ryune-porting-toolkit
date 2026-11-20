import sys
data = open(sys.argv[1], "rb").read()
magics = {
    "cpio-newc (070701)": b"070701",
    "gzip": b"\x1f\x8b\x08",
    "lz4-frame": b"\x04\x22\x4d\x18",
    "xz": b"\xfd7zXZ\x00",
    "bzip2": b"BZh",
    "zstd": b"\x28\xb5\x2f\xfd",
    "lzma-legacy": b"\x5d\x00\x00",
}
for name, m in magics.items():
    offs, i = [], 0
    while len(offs) < 8:
        i = data.find(m, i)
        if i < 0:
            break
        offs.append(i)
        i += 1
    print(f"{name:20s} {len(offs)} hit(s): {offs}")
print("ukuran:", len(data))
