#!/usr/bin/env python3
"""
VCF JSON → Markdown Summary v3.6
Převádí analýzu VCF souborů z JSON na přehledný MD report.
Plně přizpůsobeno novému sémantickému JSON schématu v18.0:
- Zobrazuje sekvenci operací a analýzu správnosti technologického řazení (ořez na konci)
- Zobrazuje sémantickou klasifikaci panelů (např. podélně dělené na 2x 600 mm ze standardní 1220 mm šíře)
- Zobrazuje normalizované koordináty u elementů (bbox_norm, centroid_norm)
- Dynamicky generuje ASCII hustotní mřížku přímo z numerických dat (density_grid.grid_data)
- Formátuje strukturovaný objekt symetrie (symmetry.summary)
- Zobrazuje detailní sémantické operace, RGB složky u barev vrstev a numerická ID nástrojů/směrů
- Zpětně kompatibilní se staršími schématy (s fallbacks na N/A)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional
from collections import defaultdict


def format_length(mm: Any) -> str:
    """Bezpečně formátuje délku v mm."""
    if mm is None:
        return "N/A"
    try:
        mm_float = float(mm)
    except (ValueError, TypeError):
        return "N/A"
    return f"{mm_float:,.1f} mm" if mm_float >= 1000 else f"{mm_float:.1f} mm"


def safe_get(data: Dict, key: str, default: Any = "N/A") -> Any:
    """Vrátí hodnotu nebo zástupný řetězec, pokud je None."""
    val = data.get(key, default)
    return default if val is None else val


def get_color_name(hex_val: Any) -> str:
    """Vrátí čitelný český název barvy ze slovníku pro známé hex kódy."""
    if hex_val is None:
        return "Neznámá"
    val = str(hex_val).lower().replace("0x", "").strip()
    val = val.zfill(8)
    
    rgb = val[2:] if len(val) == 8 else val
    
    color_map = {
        "000000": "Černá",
        "00ff00": "Zelená",
        "0000ff": "Modrá",
        "ffff00": "Žlutá",
        "ff0000": "Červená",
        "00cccc": "Azurová (Cyan)",
        "800040": "Vínová / Fialová",
        "5790fa": "Světle modrá",
        "73dd75": "Světle zelená",
        "ffffff": "Bílá",
        "808080": "Šedá",
        "ff00ff": "Růžová / Purpurová",
        "ffa500": "Oranžová",
        "00ffff": "Tyrkysová"
    }
    
    if rgb in color_map:
        return color_map[rgb]
    return "Vlastní"


def format_heights(layer: Dict) -> str:
    """
    Zformátuje výšky podle toho, zda JSON obsahuje height0/1/2,
    nebo starší start_height_h1_mm / end_height_h2_mm.
    Pokud chybí obě sady, použij 'N/A'.
    """
    has_new = all(layer.get(k) is not None for k in ("height0", "height1", "height2"))
    has_old = layer.get("start_height_h1_mm") is not None or layer.get("end_height_h2_mm") is not None

    if has_new:
        h0 = safe_get(layer, "height0")
        h1 = safe_get(layer, "height1")
        h2 = safe_get(layer, "height2")
        return f"height0: {h0}, height1: {h1}, height2: {h2} mm"
    elif has_old:
        start = safe_get(layer, "start_height_h1_mm")
        end = safe_get(layer, "end_height_h2_mm")
        return f"H1: {start} mm, H2: {end} mm"
    else:
        return "N/A"


def generate_md_report(data: Any, summary_mode: bool = False) -> str:
    """Generuje Markdown report z JSON dat."""
    md = []
    md.append("# VCF Files Analysis Report")
    md.append(f"**Generováno:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    if isinstance(data, dict):
        files = [data]
    elif isinstance(data, list):
        files = data
    else:
        raise ValueError("JSON data musí být objekt (slovník) nebo pole (seznam)")

    for file in files:
        if not isinstance(file, dict):
            continue

        filename = safe_get(file, "filename", "Neznámý soubor")
        elements = file.get("elements", [])
        layers = file.get("layers", [])

        if not isinstance(elements, list):
            elements = []
        if not isinstance(layers, list):
            layers = []

        active_elements = sum(1 for e in elements if e.get("is_output_yes") is True)
        total_elements = len(elements)

        # Počty geometrických typů na vrstvu
        layer_geom_counts = defaultdict(lambda: defaultdict(int))
        for el in elements:
            if not isinstance(el, dict):
                continue
            layer_idx = el.get("layer_index")
            geom_type = el.get("geom_type")
            if isinstance(layer_idx, int) and 0 <= layer_idx < len(layers) and geom_type is not None:
                layer_geom_counts[layer_idx][geom_type] += 1

        md.append(f"## {filename}")
        md.append(f"**Cesta:** `{safe_get(file, 'filepath')}`")
        md.append("")

        # === HLAVIČKA ===
        md.append("### Souhrn")
        md.append(f"- **Počet elementů celkem:** {total_elements}")
        md.append(f"- **Aktivní (output=yes):** {active_elements}")
        md.append(f"- **Neaktivní (output=no):** {total_elements - active_elements}")
        md.append(f"- **Počet vrstev:** {len(layers)}")
        if file.get("canvas_width_mm") is not None and file.get("canvas_height_mm") is not None:
            width = file.get("canvas_width_mm")
            height = file.get("canvas_height_mm")
            bbox = file.get("canvas_bbox", "N/A")
            md.append(f"- **Rozměry aktivní plochy (Canvas):** {width:.1f} x {height:.1f} mm (BBox: {bbox})")
            
            # Formát panelu
            format_name = file.get("detected_panel_format_name", file.get("detected_panel_format"))
            if format_name:
                panel_w = file.get("detected_panel_width_mm")
                panel_h = file.get("detected_panel_height_mm")
                if panel_w and panel_h:
                    md.append(f"- **Detekovaný formát panelu:** {format_name} ({panel_w:.0f} x {panel_h:.0f} mm)")
                else:
                    md.append(f"- **Detekovaný formát panelu:** {format_name}")
            
            md.append(f"- **Odhadovaná tloušťka feltu:** {safe_get(file, 'material_thickness_mm')} mm")
            
            # Sémantická klasifikace (v18.0)
            tech_class = file.get("technological_classification")
            if tech_class:
                md.append(f"- **Sémantická klasifikace:** `{tech_class}`")
        md.append("")

        # === TECHNOLOGICKÁ SEKVENČNÍ ANALÝZA (v18.0) ===
        seq = file.get("operation_sequence")
        if isinstance(seq, dict) and seq.get("layer_order") is not None:
            md.append("### ⚙️ Technologická sekvence a analýza")
            status_seq = "✅ V pořádku (ořez je na konci)" if seq.get("sequence_is_correct") is True else "❌ CHYBA SEKENCE (ořez probíhá dříve!)"
            md.append(f"- **Pořadí vrstev podle offsetů (aktivní):** `{seq.get('layer_order')}`")
            md.append(f"- **První aktivní nástroj:** `{seq.get('first_cut_type')}`")
            md.append(f"- **Poslední aktivní nástroj:** `{seq.get('last_cut_type')}`")
            md.append(f"- **Status sekvence:** {status_seq}")
            md.append("")

        # === PROSTOROVÁ ANALÝZA ===
        if not file.get("fail_safe_flag") and file.get("layout_type") is not None:
            md.append("### 🌐 Prostorová analýza")
            md.append(f"- **Klasifikace rozvržení (Layout):** `{safe_get(file, 'layout_type')}`")
            
            sym = file.get("symmetry")
            if isinstance(sym, dict):
                md.append(f"- **Symetrie výkresu:** {sym.get('summary')}")
            else:
                md.append(f"- **Symetrie výkresu:** {sym}")
                
            grid_info = file.get("density_grid")
            if isinstance(grid_info, dict) and grid_info.get("grid_data"):
                grid = grid_info["grid_data"]
                ascii_rows = []
                for r in range(7, -1, -1):
                    row_str = " | ".join(f"{grid[r][c]:2d}" for c in range(8))
                    ascii_rows.append(f"| {row_str} |")
                ascii_grid = "\n".join(ascii_rows)
                
                cell_size = grid_info.get("cell_size_mm", ["?", "?"])
                md.append(f"- **Hustotní analýza:** {grid_info.get('summary')} (Buňka: {cell_size[0]}x{cell_size[1]} mm)")
                md.append(f"```\n{ascii_grid}\n```")
            md.append("")

        # === OPAKUJÍCÍ SE TVARY ===
        groups = file.get("shape_groups")
        if isinstance(groups, list) and groups:
            md.append("### 🗃️ Detekované opakující se tvary (Shape Groups)")
            for sg in groups:
                count_val = sg.get("total_instances_count", sg.get("count", 1))
                md.append(f"- **{sg['id']}:** {sg['geom_type']}, Segmentů: {sg['point_count']}, Délka: {sg['length_mm']} mm, Velikost BBoxu: {sg['bbox_size'][0]}x{sg['bbox_size'][1]} mm \u2192 **{count_val}x výskyt**")
            md.append("")

        # === VRSTVY ===
        md.append("### Vrstvy")
        for i, layer in enumerate(layers):
            if not isinstance(layer, dict):
                continue
            status = "✅ **Aktivní**" if layer.get("is_output_yes") is True else "❌ Neaktivní"
            md.append(f"**Vrstva {i}:** {status}")
            
            cutter_id_str = f" (ID: {layer.get('cutter_type_id')})" if layer.get("cutter_type_id") is not None else ""
            md.append(f"- **Řezací hlava:** {safe_get(layer, 'cutter_type')}{cutter_id_str}")
            md.append(f"- **Rychlost:** {safe_get(layer, 'speed_mms')} mm/s")
            
            op_type = layer.get("operation_type")
            if op_type:
                md.append(f"- **Operace:** `{op_type}`")
                
            md.append(f"- **Délka dráhy:** {format_length(layer.get('total_cut_length_mm'))}")
            # Výšky
            md.append(f"- **Výšky:** {format_heights(layer)}")
            
            dir_id_str = f" (ID: {layer.get('direction_id')})" if layer.get("direction_id") is not None else ""
            md.append(f"- **Směr:** {safe_get(layer, 'direction')}{dir_id_str}")
            
            # Počet podávání
            feeding = layer.get("number_of_feeding")
            if feeding is not None:
                md.append(f"- **Počet podávání (number_of_feeding):** {feeding}")
            
            # Přídavky
            start_ext = layer.get("starting_extension_mm")
            end_ext = layer.get("ending_extension_mm")
            if start_ext is not None or end_ext is not None:
                start_val = start_ext if start_ext is not None else 'N/A'
                end_val = end_ext if end_ext is not None else 'N/A'
                md.append(f"- **Přídavky:** start {start_val} mm, end {end_val} mm")
            
            # Barvy (Pojmenované + hex + rgb složky v17.8)
            color_hex = layer.get("color_hex")
            color_val = layer.get("color_val")
            color_rgb = layer.get("color_rgb")
            if color_hex is not None or color_val is not None:
                hex_str = color_hex if color_hex is not None else 'N/A'
                color_name = get_color_name(color_hex)
                if color_rgb:
                    md.append(f"- **Barva:** {color_name} (hex={hex_str}, rgb={color_rgb})")
                else:
                    md.append(f"- **Barva:** {color_name} (hex={hex_str})")
            
            # Geometrické prvky
            geom_counts = layer_geom_counts.get(i, {})
            if geom_counts:
                geom_items = [f"{geom}: {cnt}" for geom, cnt in sorted(geom_counts.items())]
                md.append(f"- **Geometrické prvky:** {', '.join(geom_items)}")
            else:
                md.append("- **Geometrické prvky:** (žádné elementy v této vrstvě)")
            md.append("")

        # === CELKOVÁ PREDIKCE ===
        pred = file.get("erp_time_prediction")
        if isinstance(pred, dict):
            md.append("### Predikce času (pouze aktivní dráha)")
            md.append(f"- **Celková délka:** {format_length(pred.get('total_path_length_mm'))}")
            md.append(f"- **Odhadovaný čas:** {safe_get(pred, 'predicted_time_formatted')}")
            md.append("")

        # === DETAILNÍ ELEMENTY ===
        md.append("### Detaily elementů (s normalizovanými souřadnicemi)")
        elements_to_show = elements
        is_truncated = False
        if summary_mode and len(elements) > 15:
            elements_to_show = elements[:15]
            is_truncated = True

        for el in elements_to_show:
            if not isinstance(el, dict):
                continue
            status = "✅" if el.get("is_output_yes") is True else "❌"
            geom = safe_get(el, "geom_type")
            point_count = el.get("point_count")
            length = format_length(el.get("length_mm"))
            layer_idx = safe_get(el, "layer_index")
            pt_str = str(point_count) if point_count else "?"
            
            bbox_str = ""
            if el.get("bbox"):
                b = el["bbox"]
                bbox_str = f" | BBox: [{b[0]:.1f}, {b[1]:.1f}]→[{b[2]:.1f}, {b[3]:.1f}]"
            
            centroid_str = ""
            if el.get("centroid"):
                c = el["centroid"]
                centroid_str = f" | Centroid: ({c[0]:.1f}, {c[1]:.1f})"
                
            norm_str = ""
            if el.get("centroid_norm"):
                cn = el["centroid_norm"]
                norm_str = f" | Norm-Centroid: ({cn[0]:.2f}, {cn[1]:.2f})"
                
            md.append(f"- **{geom}** {status} | {pt_str} segmentů | {length}{bbox_str}{centroid_str}{norm_str} | vrstva {layer_idx}")
        
        if is_truncated:
            md.append(f"- ... a dalších {len(elements) - 15} elementů")
        md.append("")

        # === TECHNICKÉ METADATA ===
        md.append("### Další technická metadata")
        extracted = file.get("extracted_metadata")
        if isinstance(extracted, list) and extracted:
            tags_str = ", ".join(str(tag) for tag in extracted[:30])
            if len(extracted) > 30:
                tags_str += f", ... a dalších {len(extracted)-30}"
            md.append(f"**Extracted tags:** {tags_str}")
        elif extracted is not None and extracted != "":
            md.append(f"**Extracted metadata:** {extracted}")
        else:
            md.append("**Extracted tags:** žádné")

        md.append(f"**File hash:** `{safe_get(file, 'file_hash')}`")

        size = safe_get(file, 'file_size_bytes', 0)
        try:
            size_formatted = f"{int(size):,} bytes"
        except (ValueError, TypeError):
            size_formatted = "0 bytes"
        md.append(f"**Velikost:** {size_formatted}")

        warnings = file.get("warnings")
        if warnings is not None and (not isinstance(warnings, list) or len(warnings) > 0):
            md.append(f"**Warnings:** {len(warnings) if isinstance(warnings, list) else warnings}")
        tech_notes = file.get("tech_notes")
        if tech_notes is not None and (not isinstance(tech_notes, list) or len(tech_notes) > 0):
            md.append(f"**Tech notes:** {len(tech_notes) if isinstance(tech_notes, list) else tech_notes}")
        if file.get("fail_safe_flag") is True:
            md.append("**⚠️ Fail-safe flag: True**")

        md.append("\n---\n")

    return "\n".join(md)


def main():
    # Reconfigure stdout and stderr to handle UTF-8 printing safely on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')  # type: ignore
        except Exception:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8')  # type: ignore
        except Exception:
            pass

    args = sys.argv[1:]
    
    summary_mode = False
    if "--summary" in args:
        summary_mode = True
        args.remove("--summary")
    if "-s" in args:
        summary_mode = True
        args.remove("-s")

    if len(args) < 1:
        print("Použití: python json_vcf_to_md_v3_6.py <vstupni_json.json> [vystup.md] [--summary]")
        sys.exit(1)

    input_path = Path(args[0])
    output_path = Path(args[1]) if len(args) > 1 else input_path.with_suffix('.md')

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Chyba: Vstupní soubor není platný JSON – {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Chyba při načítání souboru: {e}")
        sys.exit(1)

    try:
        markdown = generate_md_report(data, summary_mode=summary_mode)
    except Exception as e:
        print(f"Chyba při generování reportu: {e}")
        sys.exit(1)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
    except Exception as e:
        print(f"Chyba při zápisu výstupu: {e}")
        sys.exit(1)

    print(f"✅ Report vygenerován: {output_path}")
    print(f"   Počet zpracovaných souborů: {len(data) if isinstance(data, list) else 1}")
    if summary_mode:
        print("   Aktivní režim zkráceného výpisu elementů (--summary).")


if __name__ == "__main__":
    main()
