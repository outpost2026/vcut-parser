"""Analyze VCF pairs for RE — writes vcf_pair_analysis.txt"""
import struct
import sys
from pathlib import Path

COUNT_OFF = 0x26633
STRIDE = 575
HDR = 33
GEOM = 509
ELEM_SIG = bytes([0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xFF, 0xFF])
OUT = Path(__file__).resolve().parent / "vcf_pair_analysis.txt"


def u32(d, o):
    return struct.unpack_from("<I", d, o)[0]


def f64(d, o):
    return struct.unpack_from("<d", d, o)[0]


def diff_regions(a, b):
    n = min(len(a), len(b))
    regions = []
    i = 0
    while i < n:
        if a[i] != b[i]:
            s = i
            while i < n and a[i] != b[i]:
                i += 1
            regions.append((s, i, i - s))
        else:
            i += 1
    if len(a) != len(b):
        s = n
        e = max(len(a), len(b))
        regions.append((s, e, e - s))
    return regions


def count_sig(data):
    c, pos = 0, 0
    while True:
        j = data.find(ELEM_SIG, pos)
        if j < 0:
            break
        c += 1
        pos = j + 1
    return c


def decode_element(data, start):
    hdr = data[start : start + HDR]
    gbase = start + HDR
    inner = []
    if gbase + 16 <= len(data):
        inner = [
            ("u32+0", u32(data, gbase)),
            ("u32+4", u32(data, gbase + 4)),
        ]
    coords = []
    for off in range(0, GEOM - 16, 1):
        go = gbase + off
        if go + 16 > len(data):
            break
        try:
            x, y = f64(data, go), f64(data, go + 8)
        except Exception:
            continue
        if not (abs(x) < 1e12 and abs(y) < 1e12):
            continue
        if abs(x) < 0.01 and abs(y) < 0.01:
            continue
        if -50 <= x <= 6000 and -50 <= y <= 6000:
            coords.append((go - gbase, round(x, 3), round(y, 3)))
    # dedupe nearby
    uniq = []
    seen = set()
    for rel, x, y in coords:
        key = (round(x, 1), round(y, 1))
        if key in seen:
            continue
        seen.add(key)
        uniq.append((rel, x, y))
    return hdr.hex(), inner, uniq[:16]


def analyze_pair(path1, path2, label, lines):
    b1, b2 = path1.read_bytes(), path2.read_bytes()
    lines.append("")
    lines.append("=" * 72)
    lines.append(f"PAIR: {label}")
    lines.append(f"  {path1.name}: {len(b1)} bytes (0x{len(b1):X})")
    lines.append(f"  {path2.name}: {len(b2)} bytes (0x{len(b2):X})")
    lines.append(f"  delta: {len(b2) - len(b1)} bytes (0x{len(b2) - len(b1):X})")
    lines.append(f"  expected delta if +N elements at {STRIDE}B: N*{STRIDE}")

    c1, c2 = u32(b1, COUNT_OFF), u32(b2, COUNT_OFF)
    lines.append(f"  element_count @ 0x{COUNT_OFF:X}: {c1} vs {c2}")
    lines.append(f"  elem sig count: {count_sig(b1)} vs {count_sig(b2)}")

    regions = diff_regions(b1, b2)
    lines.append(f"  diff regions: {len(regions)}")
    for s, e, L in regions[:12]:
        lines.append(f"    0x{s:08X}-0x{e:08X} len={L} (0x{L:X})")
        if L <= 16 and s < len(b1) and s < len(b2):
            lines.append(f"      f1: {b1[s:e].hex(' ')}")
            lines.append(f"      f2: {b2[s:e].hex(' ')}")

    # element starts: count field + stride from 0x26654
    start0 = 0x26654
    for name, buf, cnt in [
        (path1.name, b1, c1),
        (path2.name, b2, c2),
    ]:
        lines.append(f"  --- {name} elements={cnt} (parse @0x{start0:X} + n*{STRIDE}) ---")
        for e in range(min(cnt, 8)):
            st = start0 + e * STRIDE
            if st + STRIDE > len(buf):
                lines.append(f"    e{e}: OUT OF RANGE")
                break
            hdr_hex, inner, coords = decode_element(buf, st)
            lines.append(f"    e{e} @0x{st:X} inner={inner} coords={coords}")

    # stride check
    if c2 > c1 and len(regions) >= 2:
        tail = [r for r in regions if r[0] >= 0x26800]
        if tail:
            lines.append(f"  tail diff starts @ 0x{tail[0][0]:X}")


def main():
    base = Path(r"c:\Users\PC\Documents\Repozitar_Dev\Jobs_aplications\Wynwood\Data\Ondra_test_data")
    lines = ["VCF pair analysis for parser RE", f"generated from {Path(__file__).name}"]

    pairs = [
        (base / "rectangle_01.vcf", base / "rectangle_02.vcf", "rectangle 1 vs 2 squares"),
        (base / "line_01.VCF", base / "line_05.VCF", "line 1 vs 5 segments"),
    ]
    for p1, p2, lab in pairs:
        if p1.exists() and p2.exists():
            analyze_pair(p1, p2, lab, lines)
        else:
            lines.append(f"\nSKIP {lab}: missing {p1.name if not p1.exists() else p2.name}")

    # run hex_diff for line if present
    hex_diff_py = base / "hex_diff.py"
    if hex_diff_py.exists():
        import subprocess
        for a, b in [(base / "line_01.VCF", base / "line_05.VCF")]:
            if a.exists() and b.exists():
                subprocess.run(
                    [sys.executable, str(hex_diff_py), str(a), str(b)],
                    cwd=str(base),
                    capture_output=True,
                    text=True,
                )
                hr = base / "hex_diff_report.txt"
                if hr.exists():
                    lines.append("\n--- hex_diff_report.txt (line pair) head ---")
                    lines.extend(hr.read_text(encoding="utf-8", errors="replace").splitlines()[:25])

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
