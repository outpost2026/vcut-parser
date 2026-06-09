import sys
from pathlib import Path

def hex_diff(file1: str, file2: str, context_bytes: int = 32, output_file: str = "hex_diff_report.txt"):
    """Porovná dva binární soubory a vypíše odlišné bloky v hexadecimálním tvaru."""
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    max_len = max(len(data1), len(data2))
    diff_regions = []
    i = 0
    while i < max_len:
        b1 = data1[i] if i < len(data1) else None
        b2 = data2[i] if i < len(data2) else None
        if b1 != b2:
            # Zaznamenáme začátek odlišného bloku
            start = max(0, i - context_bytes)
            # Pokusíme se najít konec souvislé odlišné oblasti
            end = i
            while end < max_len and ((data1[end] if end < len(data1) else None) != (data2[end] if end < len(data2) else None)):
                end += 1
            end = min(max_len, end + context_bytes)
            
            block1 = data1[start:end] if start < len(data1) else b''
            block2 = data2[start:end] if start < len(data2) else b''
            diff_regions.append({
                'offset_start': i,
                'offset_end': end,
                'hex1': block1.hex(' '),
                'hex2': block2.hex(' '),
                'ascii1': ''.join(chr(b) if 32 <= b < 127 else '.' for b in block1),
                'ascii2': ''.join(chr(b) if 32 <= b < 127 else '.' for b in block2)
            })
            i = end  # Přeskočíme zpracovaný blok
        else:
            i += 1

    # Sestavení výstupního reportu
    out_lines = []
    out_lines.append(f"Hex diff between {file1} and {file2}\n")
    out_lines.append(f"File1 size: {len(data1)} bytes, File2 size: {len(data2)} bytes\n")
    out_lines.append(f"Found {len(diff_regions)} differing region(s).\n")
    out_lines.append("=" * 100 + "\n")

    for idx, reg in enumerate(diff_regions):
        out_lines.append(f"Region {idx+1}: offset 0x{reg['offset_start']:08X} - 0x{reg['offset_end']:08X} (length {reg['offset_end'] - reg['offset_start']} bytes)\n")
        out_lines.append(f"  File1 hex: {reg['hex1']}\n")
        out_lines.append(f"  File2 hex: {reg['hex2']}\n")
        out_lines.append(f"  File1 ASCII: {reg['ascii1']}\n")
        out_lines.append(f"  File2 ASCII: {reg['ascii2']}\n")
        out_lines.append("-" * 100 + "\n")

    # Uložení reportu
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    print(f"Diff report saved to {output_file}")

    # Uložení raw bloků jako samostatné binární soubory pro detailní analýzu
    for idx, reg in enumerate(diff_regions):
        raw1 = data1[reg['offset_start']:reg['offset_end']]
        raw2 = data2[reg['offset_start']:reg['offset_end']]
        with open(f"diff_region_{idx+1}_file1.bin", 'wb') as f:
            f.write(raw1)
        with open(f"diff_region_{idx+1}_file2.bin", 'wb') as f:
            f.write(raw2)
        print(f"Raw region {idx+1} saved to diff_region_{idx+1}_file1.bin and diff_region_{idx+1}_file2.bin")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hex_diff.py <file1> <file2>")
        sys.exit(1)
    hex_diff(sys.argv[1], sys.argv[2])