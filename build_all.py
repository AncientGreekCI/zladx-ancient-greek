#!/usr/bin/env python3
"""build_all.py <repo> <outdir> -- dialogue + menus -> Greek ROMs for v1.0, Rev A, Rev B and one IPS patch each.
Needs: RGBDS 1.0.x on PATH, the LADX-Disassembly checkout, and clean English ROMs built from the same checkout
(azle_original.gbc, azle_r1_original.gbc, azle_r2_original.gbc in <outdir>)."""
import subprocess, sys, pathlib, hashlib, glob, os
repo, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); here = pathlib.Path(__file__).parent
run = lambda *a, **k: subprocess.check_call(list(map(str, a)), **k)
run('python3', here / 'apply_greek.py', repo, here / 'greek_dialog.txt')
run('python3', here / 'apply_menus.py', repo)
for f in glob.glob(str(repo / 'azle*.gbc')) + glob.glob(str(repo / 'src/main.azle*.o')) + glob.glob(str(repo / 'src/gfx/*/*.2bpp')): os.remove(f)
for target, orig, name in [('azle', 'azle_original', 'v1.0'), ('azle-r1', 'azle_r1_original', 'RevA'), ('azle-r2', 'azle_r2_original', 'RevB')]:
    run('make', f'{target}.gbc', cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    patch = out / f'LA_Greek_{name}.ips'
    run('python3', here / 'make_patch.py', out / f'{orig}.gbc', repo / f'{target}.gbc', patch, stdout=subprocess.DEVNULL)
    run('python3', here / 'apply_ips.py', out / f'{orig}.gbc', patch, '/tmp/_rt.gbc')
    ok = hashlib.md5(open('/tmp/_rt.gbc', 'rb').read()).hexdigest() == hashlib.md5(open(repo / f'{target}.gbc', 'rb').read()).hexdigest()
    print(f'{name:<5} patch {patch.stat().st_size:>6} bytes, round-trip {"OK" if ok else "MISMATCH"}')
