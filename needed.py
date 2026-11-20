#!/usr/bin/env python3
import os, subprocess, sys, collections

vendor, system, outfile = sys.argv[1:4]

def libnames(root, subdirs):
    names = set()
    for sd in subdirs:
        base = os.path.join(root, sd)
        for dp, dn, fn in os.walk(base, followlinks=False):
            for f in fn:
                if f.endswith(".so"):
                    names.add(f)
    return names

def apex_libs(root):
    names = set()
    base = os.path.join(root, "apex")
    if not os.path.isdir(base):
        return names
    for dp, dn, fn in os.walk(base, followlinks=False):
        for f in fn:
            if f.endswith(".so"):
                names.add(f)
    return names

have_vendor = libnames(vendor, ["lib", "lib64"])
have_sys = (libnames(system, ["lib", "lib64"])
            | libnames(system, ["system_ext/lib", "system_ext/lib64"])
            | apex_libs(system))

def is_elf(p):
    try:
        with open(p, "rb") as f:
            return f.read(4) == b"\x7fELF"
    except OSError:
        return False

missing = collections.defaultdict(set)
count = 0
for sd in ["bin", "lib", "lib64"]:
    base = os.path.join(vendor, sd)
    for dp, dn, fn in os.walk(base):
        for f in fn:
            p = os.path.join(dp, f)
            if os.path.islink(p) or not is_elf(p):
                continue
            count += 1
            out = subprocess.run(["readelf", "-d", p], capture_output=True, text=True).stdout
            for line in out.splitlines():
                if "(NEEDED)" in line and "[" in line:
                    lib = line.split("[", 1)[1].split("]")[0]
                    if lib not in have_vendor and lib not in have_sys:
                        missing[lib].add(os.path.relpath(p, vendor))

with open(outfile, "w") as o:
    o.write(f"ELF diperiksa: {count}; vendor so: {len(have_vendor)}; system so: {len(have_sys)}\n")
    o.write(f"Pustaka yang hilang: {len(missing)}\n\n")
    for lib, users in sorted(missing.items(), key=lambda kv: -len(kv[1])):
        o.write(f"{lib}  <- {len(users)} berkas: {', '.join(sorted(users)[:6])}\n")
print(open(outfile).read()[:1500])
