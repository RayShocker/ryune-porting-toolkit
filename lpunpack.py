#!/usr/bin/env python3
"""Minimal lpunpack: python3 lpunpack.py super.raw.img OUTDIR [partition ...]"""
import os, struct, sys

GEOM_MAGIC = 0x616C4467   # liblp geometry
HDR_MAGIC = 0x414C5030    # liblp metadata header
RESERVED = 4096           # bytes before geometry
GEOM_SIZE = 4096
SECTOR = 512

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    img, out, only = sys.argv[1], sys.argv[2], set(sys.argv[3:])
    os.makedirs(out, exist_ok=True)
    f = open(img, "rb")

    f.seek(RESERVED)
    magic, gsize = struct.unpack("<II", f.read(8))
    if magic != GEOM_MAGIC:
        sys.exit("bukan image super (geometry magic salah)")
    f.seek(RESERVED + 8 + 32)
    max_size, slots, lbs = struct.unpack("<III", f.read(12))
    print(f"metadata_max_size={max_size} slots={slots} logical_block_size={lbs}")

    meta_off = RESERVED + 2 * GEOM_SIZE          # slot 0, primary copy
    f.seek(meta_off)
    h = f.read(256)
    (hmagic, major, minor, hsize) = struct.unpack_from("<IHHI", h, 0)
    if hmagic != HDR_MAGIC:
        sys.exit("header metadata tidak valid")
    tables_size = struct.unpack_from("<I", h, 44)[0]
    (p_off, p_n, p_sz, e_off, e_n, e_sz,
     g_off, g_n, g_sz, b_off, b_n, b_sz) = struct.unpack_from("<12I", h, 80)
    print(f"metadata v{major}.{minor}: {p_n} partisi, {e_n} extent")

    f.seek(meta_off + hsize)
    tables = f.read(tables_size)

    extents = []
    for i in range(e_n):
        ns, ttype, tdata, tsrc = struct.unpack_from("<QIQI", tables, e_off + i * e_sz)
        extents.append((ns, ttype, tdata, tsrc))

    for i in range(p_n):
        name_raw, attrs, first, num, grp = struct.unpack_from(
            "<36sIIII", tables, p_off + i * p_sz)
        name = name_raw.split(b"\0")[0].decode()
        size = sum(extents[first + k][0] for k in range(num)) * SECTOR
        if num == 0 or size == 0:
            print(f"lewati {name} (kosong)")
            continue
        if only and name not in only:
            continue
        path = os.path.join(out, name + ".img")
        print(f"tulis {name}: {size/1024/1024:.1f} MB -> {path}")
        with open(path, "wb") as o:
            for k in range(num):
                ns, ttype, tdata, tsrc = extents[first + k]
                left = ns * SECTOR
                if ttype == 1:                      # zero extent
                    o.write(b"\0" * left)
                    continue
                f.seek(tdata * SECTOR)
                while left:
                    chunk = f.read(min(left, 8 << 20))
                    if not chunk:
                        sys.exit("image terpotong")
                    o.write(chunk)
                    left -= len(chunk)

main()
