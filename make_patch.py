#!/usr/bin/env python3
"""make_patch.py original.gbc patched.gbc out.ips  -- writes an IPS patch containing only the differences."""
import sys
a = open(sys.argv[1], 'rb').read(); b = open(sys.argv[2], 'rb').read()
assert len(a) == len(b)
out = bytearray(b'PATCH'); i = 0; n = len(a)
while i < n:
    if a[i] == b[i]: i += 1; continue
    j = i
    while j < n and (a[j] != b[j] or (j + 1 < n and a[j+1] != b[j+1] and j - i < 65000)):
        j += 1
    j = min(j, i + 65535)
    out += i.to_bytes(3, 'big') + (j - i).to_bytes(2, 'big') + b[i:j]
    i = j
out += b'EOF'
open(sys.argv[3], 'wb').write(out)
print(f"patch size: {len(out)} bytes")
