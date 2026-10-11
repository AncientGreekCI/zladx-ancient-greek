import sys
rom = bytearray(open(sys.argv[1],'rb').read()); p = open(sys.argv[2],'rb').read()
assert p[:5] == b'PATCH'; i = 5
while p[i:i+3] != b'EOF':
    off = int.from_bytes(p[i:i+3],'big'); sz = int.from_bytes(p[i+3:i+5],'big'); i += 5
    rom[off:off+sz] = p[i:i+sz]; i += sz
open(sys.argv[3],'wb').write(rom)
