import os
import sys
import struct
import json
import hashlib
import re
import math
import datetime
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    from Knowledge_base.engine import KnowledgeBaseEngine
    from Knowledge_base.models import ThicknessConfidence, Severity
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False
    KnowledgeBaseEngine = None
    class ThicknessConfidence:
        HIGH = "HIGH"
        LOW = "LOW"
    class Severity:
        INFO = "INFO"
        WARNING = "WARNING"
        CRITICAL = "CRITICAL"


class RuidaVcfDeepParserV18_3:
    def __init__(self, directory_path: str, output_dir: Optional[str] = None, output_mode: str = "both"):
        self.directory_path = Path(directory_path)
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.directory_path
        self.output_mode = output_mode
        self.parsed_files = {}

    def _get_color_name(self, hex_val: str) -> str:
        val = hex_val.lower().replace("0x", "").strip()
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
        return f"Vlastní ({hex_val})"

    def _extract_strings(self, binary_data: bytes) -> list:
        strings = re.findall(b'[A-Za-z0-9_ \\-\\.]{4,}', binary_data)
        decoded = set()
        for s in strings:
            try:
                text = s.decode('windows-1250').strip()
                if ".dxf" in text.lower():
                    decoded.add(text)
                elif any(c.isalpha() for c in text) and len(text) > 3:
                    decoded.add(text)
            except:
                continue
        return sorted(list(decoded))

    def _extract_active_layers_details(self, binary_data: bytes) -> list:
        sig = b'\x01\x00\x01\x00\x00\xff\xff\xff'
        offset = 0
        geom_colors = set()
        first_geometry_pos = len(binary_data)
        
        while True:
            pos = binary_data.find(sig, offset)
            if pos == -1:
                break
            if first_geometry_pos == len(binary_data):
                first_geometry_pos = pos
            geom_color = struct.unpack_from('<I', binary_data, pos + 8)[0]
            geom_colors.add(geom_color)
            offset = pos + 1

        version = "1.0.013"
        for s in [b"RDVCUTFILEVER1.0.012", b"VER1.0.012"]:
            if s in binary_data:
                version = "1.0.012"
                break
                
        block_size = 610 if version == "1.0.013" else 210
        
        active_layers = []
        cutter_map = {0: "Vibrate cutter", 1: "Wheel", 2: "Milling cutter", 3: "V-slot", 4: "Vibrate cut"}
        dir_map = {0: "Left", 1: "Right", 2: "Cut both side"}
        
        cutter_id_map = {"Vibrate cutter": 1, "Wheel": 2, "Milling cutter": 3, "V-slot": 4, "Vibrate cut": 5}
        dir_id_map = {"Left": 1, "Right": 2, "Cut both side": 3, "N/A": 0}
        
        for k in range(1, 32):
            pos = first_geometry_pos - k * block_size
            if pos < 0:
                break
                
            S = pos + 4
            try:
                speed = struct.unpack('<d', binary_data[S:S+8])[0]
                color_val = struct.unpack_from('<I', binary_data, S-8)[0]
                
                expected_geom_color = (color_val << 8) & 0xffffffff
                if 1.0 <= speed <= 2000.0 and speed.is_integer() and speed % 5 == 0:
                    if (not geom_colors) or (expected_geom_color in geom_colors):
                        output_flag = struct.unpack_from('<I', binary_data, pos)[0]
                        is_output_yes = (output_flag == 1)
                        
                        cutter_type_raw = struct.unpack('<i', binary_data[S+28:S+32])[0]
                        # Fix Bug A: Map tool strictly to low-word (ID port), ignoring start_height_h1 elevation (safety clearance)
                        cutter_type = cutter_type_raw & 0xffff
                        
                        feed_num = struct.unpack('<i', binary_data[S+84:S+88])[0]
                        start_height_h1 = struct.unpack('<d', binary_data[S+76:S+84])[0]
                        end_height_h2 = struct.unpack('<d', binary_data[S+92:S+100])[0]
                        
                        b_comp = color_val & 0xff
                        g_comp = (color_val >> 8) & 0xff
                        r_comp = (color_val >> 16) & 0xff
                        
                        cutter_name = cutter_map.get(cutter_type, "Unknown")
                        
                        layer_info = {
                            "speed_mms": int(speed),
                            "cutter_type": cutter_name,
                            "cutter_type_id": cutter_id_map.get(cutter_name, 0),
                            "number_of_feeding": feed_num,
                            "start_height_h1_mm": round(start_height_h1, 3),
                            "travel_safety_height_mm": round(start_height_h1, 3), # Explicitly interpret H1 as travel safety height
                            "end_height_h2_mm": round(end_height_h2, 3),
                            "total_cut_length_mm": 0.0,
                            "color_hex": f"0x{color_val:08x}",
                            "color_val": color_val,
                            "color_rgb": [r_comp, g_comp, b_comp],
                            "direction": "N/A",
                            "direction_id": 0,
                            "v_slot_width_comp_mm": 0.0,
                            "starting_extension_mm": 0.0,
                            "ending_extension_mm": 0.0,
                            "is_output_yes": is_output_yes,
                            "operation_type": "N/A",
                            "complexity": {
                                "avg_segment_length_mm": 0.0,
                                "curvature_index": 0.0,
                                "sharp_corners_count": 0,
                                "total_direction_changes": 0
                            }
                        }
                        
                        # General starting/ending extension parsing at offsets S+110 and S+118 for all layer types
                        try:
                            start_ext = struct.unpack('<d', binary_data[S+110:S+118])[0]
                            end_ext = struct.unpack('<d', binary_data[S+118:S+126])[0]
                            if not (math.isnan(start_ext) or math.isinf(start_ext)):
                                layer_info["starting_extension_mm"] = round(start_ext, 3)
                            if not (math.isnan(end_ext) or math.isinf(end_ext)):
                                layer_info["ending_extension_mm"] = round(end_ext, 3)
                        except:
                            pass
                        
                        if cutter_type == 3: 
                            try:
                                direction_raw = struct.unpack('<H', binary_data[S+100:S+102])[0]
                                v_slot_comp = struct.unpack('<d', binary_data[S+102:S+110])[0]

                                dir_name = dir_map.get(direction_raw, "Unknown")
                                layer_info["direction"] = dir_name
                                layer_info["direction_id"] = dir_id_map.get(dir_name, -1)
                                if not (math.isnan(v_slot_comp) or math.isinf(v_slot_comp)):
                                    layer_info["v_slot_width_comp_mm"] = round(v_slot_comp, 3)
                            except:
                                pass
                            
                        active_layers.append(layer_info)
            except:
                pass
                
        active_layers.reverse()
        return active_layers

    def _parse_geometry_v18_2(self, binary_data: bytes, layers: list) -> list:
        sig = b'\x01\x00\x01\x00\x00\xff\xff\xff'
        offset = 0
        elements = []
        
        geom_type_ids = {"Circle": 1, "Line": 2, "Polyline": 3, "Polygon": 4}
        
        while True:
            pos = binary_data.find(sig, offset)
            if pos == -1: break
            
            p = pos + 45
            if p >= len(binary_data):
                break
                
            geom_color = struct.unpack_from('<I', binary_data, pos + 8)[0]
            
            mapped_layer_idx = -1
            for idx, l in enumerate(layers):
                if geom_color == ((l["color_val"] << 8) & 0xffffffff):
                    mapped_layer_idx = idx
                    break
            
            try:
                type_id = struct.unpack_from('<I', binary_data, p)[0]
                pt_count = struct.unpack_from('<I', binary_data, p+4)[0]
                subtype = struct.unpack_from('<I', binary_data, p+8)[0]
            except Exception as e:
                offset = pos + 1
                continue
            
            geom_type = "Unknown"
            length = 0.0
            bbox = None
            centroid = None
            vertices = []
            
            # Inicializujeme komplexní matematické charakteristiky (Fáze v18.1 - B1)
            is_closed_loop = False
            avg_segment_length_mm = 0.0
            total_absolute_curvature_rad = 0.0
            curvature_index = 0.0
            sharp_corners_count = 0
            total_direction_changes = 0
            
            if type_id == 1 and (subtype & 0xffff) == 3:  # Circle
                geom_type = "Circle"
                try:
                    cx = struct.unpack_from('<d', binary_data, p+14)[0]
                    cy = struct.unpack_from('<d', binary_data, p+22)[0]
                    px = struct.unpack_from('<d', binary_data, p+30)[0]
                    py = struct.unpack_from('<d', binary_data, p+38)[0]
                    
                    radius = abs(px - cx)
                    length = 2 * math.pi * radius
                    
                    if not (math.isinf(cx) or math.isnan(cx) or math.isinf(cy) or math.isnan(cy) or
                            math.isinf(px) or math.isnan(px) or math.isinf(py) or math.isnan(py)):
                        bbox = [
                            round(cx - radius, 2),
                            round(cy - radius, 2),
                            round(cx + radius, 2),
                            round(cy + radius, 2)
                        ]
                        centroid = [round(cx, 2), round(cy, 2)]
                        # Pro kruh nepoužíváme ray-casting, ale pro hierarchii uložíme centroid
                        is_closed_loop = True
                        avg_segment_length_mm = round(length, 2)
                        total_absolute_curvature_rad = round(2 * math.pi, 4)
                        curvature_index = round(total_absolute_curvature_rad / length, 4) if length > 0 else 0.0
                        sharp_corners_count = 0
                        total_direction_changes = 0
                except:
                    pass
            else:
                if type_id == 0:
                    geom_type = "Line" if pt_count == 1 else "Polyline"
                elif type_id == 1:
                    geom_type = "Polygon"
                
                try:
                    points_x = []
                    points_y = []
                    vectors = []
                    
                    for i in range(pt_count):
                        seg_offset = p + i * 74
                        if seg_offset + 74 <= len(binary_data):
                            x1, y1 = struct.unpack_from('<dd', binary_data, seg_offset + 14)
                            x2, y2 = struct.unpack_from('<dd', binary_data, seg_offset + 30)
                            if not (math.isinf(x1) or math.isnan(x1) or math.isinf(y1) or math.isnan(y1) or
                                    math.isinf(x2) or math.isnan(x2) or math.isinf(y2) or math.isnan(y2)):
                                length += math.hypot(x2 - x1, y2 - y1)
                                points_x.extend([x1, x2])
                                points_y.extend([y1, y2])
                                
                                # Rekonstrukce vrcholů pro polygon/polyline a výpočet směrových vektorů
                                if i == 0:
                                    vertices.append((x1, y1))
                                vertices.append((x2, y2))
                                vectors.append((x2 - x1, y2 - y1))
                    
                    if points_x and points_y:
                        bbox = [
                            round(min(points_x), 2),
                            round(min(points_y), 2),
                            round(max(points_x), 2),
                            round(max(points_y), 2)
                        ]
                        centroid = [
                            round(sum(points_x) / len(points_x), 2),
                            round(sum(points_y) / len(points_y), 2)
                        ]
                    
                    # Výpočet úhlových podpisů (Angular Signature)
                    if len(vectors) > 1:
                        angles = []
                        for idx in range(len(vectors) - 1):
                            ux, uy = vectors[idx]
                            vx, vy = vectors[idx+1]
                            mag_u = math.hypot(ux, uy)
                            mag_v = math.hypot(vx, vy)
                            if mag_u > 1e-6 and mag_v > 1e-6:
                                dot_p = ux * vx + uy * vy
                                cross_p = ux * vy - uy * vx
                                angle = math.atan2(cross_p, dot_p)
                                angles.append(angle)
                        
                        if angles:
                            total_absolute_curvature_rad = sum(abs(a) for a in angles)
                            curvature_index = total_absolute_curvature_rad / length if length > 0 else 0.0
                            
                            # Ostré rohy (85° - 95°)
                            for a in angles:
                                deg = abs(a * 180.0 / math.pi)
                                if 85.0 <= deg <= 95.0:
                                    sharp_corners_count += 1
                                    
                            # Detekce vlnění / změny směru (Inflection points)
                            filtered_angles = [a for a in angles if abs(a) >= 0.01]
                            for idx in range(len(filtered_angles) - 1):
                                if (filtered_angles[idx] > 0 and filtered_angles[idx+1] < 0) or \
                                   (filtered_angles[idx] < 0 and filtered_angles[idx+1] > 0):
                                    total_direction_changes += 1
                    
                    # Detekce uzavřenosti smyčky
                    if geom_type == "Polygon":
                        is_closed_loop = True
                    elif geom_type == "Polyline" and vertices:
                        # Porovnat první a poslední bod s tolerancí 0.01 mm
                        p_start = vertices[0]
                        p_end = vertices[-1]
                        if math.hypot(p_start[0] - p_end[0], p_start[1] - p_end[1]) <= 0.01:
                            is_closed_loop = True
                            
                    avg_segment_length_mm = length / pt_count if pt_count > 0 else 0.0
                except:
                    pass
            
            # Fix Bug B: Implement Low-Pass Filter. Discard micro-elements with length < 0.5 mm from the calculation
            if length >= 0.5 and length < 100000000:
                is_output_yes = layers[mapped_layer_idx]["is_output_yes"] if (mapped_layer_idx != -1 and mapped_layer_idx < len(layers)) else True
                elements.append({
                    "offset": hex(pos),
                    "geom_type": geom_type,
                    "geom_type_id": geom_type_ids.get(geom_type, 0),
                    "type_id": type_id,
                    "point_count": pt_count,
                    "length_mm": round(length, 2),
                    "layer_index": mapped_layer_idx,
                    "is_output_yes": is_output_yes,
                    "bbox": bbox,
                    "centroid": centroid,
                    "vertices": vertices,
                    "is_closed_loop": is_closed_loop,
                    "complexity": {
                        "avg_segment_length_mm": round(avg_segment_length_mm, 2),
                        "curvature_index": round(curvature_index, 4),
                        "sharp_corners_count": sharp_corners_count,
                        "total_direction_changes": total_direction_changes
                    }
                })
            
            offset = pos + 1
            
        return elements

    def _group_elements(self, elements: list) -> list:
        groups = {}
        for el in elements:
            if not el.get("is_output_yes"):
                continue
            geom_type = el["geom_type"]
            pt_count = el["point_count"]
            length = el["length_mm"]
            bbox = el.get("bbox")
            centroid = el.get("centroid")
            
            if bbox:
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                aspect_ratio = round(w / h, 1) if h > 0 else 0.0
            else:
                aspect_ratio = 0.0
                
            if geom_type == "Circle" and bbox:
                r = (bbox[2] - bbox[0]) / 2.0
                key = ("Circle", pt_count, round(length / 2.0) * 2.0, round(r, 1))
            else:
                key = (geom_type, pt_count, round(length / 2.0) * 2.0, round(aspect_ratio, 1))
                
            if key not in groups:
                groups[key] = {
                    "geom_type": geom_type,
                    "point_count": pt_count,
                    "length_mm": length,
                    "aspect_ratio": aspect_ratio,
                    "count": 0,
                    "instances": [],
                    "bbox": bbox
                }
            groups[key]["count"] += 1
            groups[key]["instances"].append({
                "centroid": centroid,
                "bbox": bbox
            })
            
        shape_groups = []
        for idx, (key, val) in enumerate(groups.items()):
            shape_groups.append({
                "id": f"Group_{idx+1}",
                "geom_type": val["geom_type"],
                "point_count": val["point_count"],
                "length_mm": round(val["length_mm"], 1),
                "count": val["count"],
                "instances": val["instances"],
                "total_instances_count": val["count"],
                "bbox_size": [round(val["bbox"][2] - val["bbox"][0], 1), round(val["bbox"][3] - val["bbox"][1], 1)] if val["bbox"] else [0.0, 0.0]
            })
        return shape_groups

    def _detect_panel_format(self, canvas_width: float, canvas_height: float) -> Dict[str, Any]:
        formats = [
            (1200, 2790, "1200x2790 mm (Standardní Echoblock)"),
            (1200, 2800, "1200x2800 mm (Echoblock nominální)"),
            (600, 2800, "600x2800 mm (Poloviční panel)"),
            (1220, 2900, "1220x2900 mm (Plsť Savanna surová)"),
            (1200, 2500, "1200x2500 mm (Atypická zakázka Capexus)"),
            (600, 1200, "600x1200 mm (Obkladový dlaždicový formát)")
        ]
        
        for w_std, h_std, name in formats:
            if (abs(canvas_width - w_std) <= 20.0 and abs(canvas_height - h_std) <= 20.0):
                return {
                    "format_name": name,
                    "panel_width_mm": float(w_std),
                    "panel_height_mm": float(h_std),
                    "is_atypical": False
                }
            elif (abs(canvas_width - h_std) <= 20.0 and abs(canvas_height - w_std) <= 20.0):
                return {
                    "format_name": f"{name} (Otočený)",
                    "panel_width_mm": float(h_std),
                    "panel_height_mm": float(w_std),
                    "is_atypical": False
                }
                
        return {
            "format_name": f"Atypický formát ({canvas_width:.1f} x {canvas_height:.1f} mm)",
            "panel_width_mm": round(canvas_width, 1),
            "panel_height_mm": round(canvas_height, 1),
            "is_atypical": True
        }

    def _compute_density_grid(self, elements: list, canvas_bbox: list) -> Optional[dict]:
        if not canvas_bbox or canvas_bbox == [0.0, 0.0, 0.0, 0.0]:
            return None
        min_x, min_y, max_x, max_y = canvas_bbox
        w = max_x - min_x
        h = max_y - min_y
        if w == 0 or h == 0:
            return None
            
        grid = [[0 for _ in range(8)] for _ in range(8)]
        for el in elements:
            if el["is_output_yes"] and el.get("centroid"):
                cx, cy = el["centroid"]
                ix = int((cx - min_x) / w * 8)
                iy = int((cy - min_y) / h * 8)
                ix = min(max(ix, 0), 7)
                iy = min(max(iy, 0), 7)
                grid[iy][ix] += 1
                
        row_sums = [sum(grid[r]) for r in range(8)]
        col_sums = [sum(grid[r][c] for r in range(8)) for c in range(8)]
        
        max_row = row_sums.index(max(row_sums)) if sum(row_sums) > 0 else 0
        max_col = col_sums.index(max(col_sums)) if sum(col_sums) > 0 else 0
        
        summary = f"Nejvyšší koncentrace prvků je ve vertikální zóně {max_row+1}/8 a horizontálním sloupci {max_col+1}/8."
        return {
            "grid_data": grid,
            "summary": summary,
            "cell_size_mm": [round(h / 8.0, 1), round(w / 8.0, 1)]
        }

    def _detect_symmetry(self, elements: list, canvas_bbox: list) -> dict:
        default_res = {
            "has_vertical": False,
            "vertical_score_percent": 0,
            "has_horizontal": False,
            "horizontal_score_percent": 0,
            "summary": "Symetrie nebyla detekována (chybí geometrie)"
        }
        if not canvas_bbox or canvas_bbox == [0.0, 0.0, 0.0, 0.0]:
            return default_res
        min_x, min_y, max_x, max_y = canvas_bbox
        w = max_x - min_x
        h = max_y - min_y
        if w == 0 or h == 0:
            return default_res
            
        intervals = 12
        hist_x = [0] * intervals
        hist_y = [0] * intervals
        
        total_active = 0
        for el in elements:
            if el["is_output_yes"] and el.get("centroid"):
                cx, cy = el["centroid"]
                ix = min(int((cx - min_x) / w * intervals), intervals - 1)
                iy = min(int((cy - min_y) / h * intervals), intervals - 1)
                hist_x[ix] += 1
                hist_y[iy] += 1
                total_active += 1
                
        if total_active == 0:
            return {
                "has_vertical": False,
                "vertical_score_percent": 0,
                "has_horizontal": False,
                "horizontal_score_percent": 0,
                "summary": "Symetrie nebyla detekována (žádná aktivní geometrie)"
            }
            
        vert_diff = sum(abs(hist_x[i] - hist_x[intervals - 1 - i]) for i in range(intervals // 2))
        vert_score = max(0, 100 - int((vert_diff / total_active) * 100)) if total_active > 0 else 0
        
        horiz_diff = sum(abs(hist_y[i] - hist_y[intervals - 1 - i]) for i in range(intervals // 2))
        horiz_score = max(0, 100 - int((horiz_diff / total_active) * 100)) if total_active > 0 else 0
        
        has_v = vert_score >= 85
        has_h = horiz_score >= 85
        
        res = []
        if has_v:
            res.append(f"vertikální (shoda {vert_score} %)")
        if has_h:
            res.append(f"horizontální (shoda {horiz_score} %)")
            
        summary_str = "Symetrie nebyla detekována"
        if res:
            summary_str = f"Detekována " + " a ".join(res)
            
        return {
            "has_vertical": has_v,
            "vertical_score_percent": vert_score,
            "has_horizontal": has_h,
            "horizontal_score_percent": horiz_score,
            "summary": summary_str
        }

    def _classify_layout(self, shape_groups: list, canvas_bbox: list) -> str:
        if not canvas_bbox or canvas_bbox == [0.0, 0.0, 0.0, 0.0]:
            return "freeform"
        
        total_instances = sum(g["total_instances_count"] for g in shape_groups)
        if total_instances <= 2:
            return "single_piece"
            
        centroids = []
        for g in shape_groups:
            centroids.extend([inst["centroid"] for inst in g["instances"] if inst.get("centroid")])
            
        if len(centroids) < 3:
            return "freeform"
            
        xs = [c[0] for c in centroids]
        ys = [c[1] for c in centroids]
        
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        
        var_x = sum((x - mean_x)**2 for x in xs) / len(xs)
        var_y = sum((y - mean_y)**2 for y in ys) / len(ys)
        
        std_x = math.sqrt(var_x)
        std_y = math.sqrt(var_y)
        
        if std_x < 50.0 and std_y > 150.0:
            return "linear_along_y"
        elif std_y < 50.0 and std_x > 150.0:
            return "linear_along_x"
            
        unique_xs = set(round(x / 30.0) for x in xs)
        unique_ys = set(round(y / 30.0) for y in ys)
        
        if len(unique_xs) > 1 and len(unique_ys) > 1:
            if len(unique_xs) * len(unique_ys) >= len(centroids) * 0.6:
                return "grid"
                
        return "freeform"

    def _format_time(self, seconds: int) -> str:
        if seconds <= 0:
            return "0 s"
        if seconds < 60:
            return f"{seconds} s"
        minutes = seconds // 60
        secs = seconds % 60
        if minutes < 60:
            return f"{minutes} min {secs} s"
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours} h {mins} min {secs} s"

    def _bbox_distance(self, bbox1: list, bbox2: list) -> float:
        if not bbox1 or not bbox2:
            return float('inf')
        min_x1, min_y1, max_x1, max_y1 = bbox1
        min_x2, min_y2, max_x2, max_y2 = bbox2
        
        dx = max(0, min_x2 - max_x1, min_x1 - max_x2)
        dy = max(0, min_y2 - max_y1, min_y1 - max_y2)
        return math.hypot(dx, dy)

    def _point_in_polygon(self, px: float, py: float, poly_points: list) -> bool:
        inside = False
        n = len(poly_points)
        if n < 3:
            return False
        p1x, p1y = poly_points[0]
        for i in range(n + 1):
            p2x, p2y = poly_points[i % n]
            if py > min(p1y, p2y):
                if py <= max(p1y, p2y):
                    if px <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        else:
                            xints = p1x
                        if p1x == p2x or px <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def _is_point_inside_element(self, point: list, el: dict) -> bool:
        if not el.get("bbox") or not el.get("centroid"):
            return False
        
        if el["geom_type"] == "Circle":
            cx, cy = el["centroid"]
            radius = (el["bbox"][2] - el["bbox"][0]) / 2.0
            return math.hypot(point[0] - cx, point[1] - cy) <= radius
        elif el["geom_type"] in ("Polygon", "Polyline") and el.get("vertices"):
            return self._point_in_polygon(point[0], point[1], el["vertices"])
        return False

    def _analyze_sub_jobs_relation(self, sub_jobs: list) -> str:
        if len(sub_jobs) <= 1:
            return ""
        xs = [sj["centroid"][0] for sj in sub_jobs if "centroid" in sj]
        ys = [sj["centroid"][1] for sj in sub_jobs if "centroid" in sj]
        if not xs or not ys:
            return ""
        range_x = max(xs) - min(xs)
        range_y = max(ys) - min(ys)
        if range_x > range_y and range_x > 50.0:
            return f"Sub-zakázky jsou uspořádány horizontálně v řadě za sebou (osa X). Celkový počet panelů: {len(sub_jobs)}. Každý panel je ohraničen samostatným obvodovým řezem (Vibrate cutter)."
        elif range_y > range_x and range_y > 50.0:
            return f"Sub-zakázky jsou uspořádány vertikálně v řadě nad sebou (osa Y). Celkový počet panelů: {len(sub_jobs)}. Každý panel je ohraničen samostatným obvodovým řezem (Vibrate cutter)."
        else:
            return f"Sub-zakázky tvoří volné nebo mřížkové uspořádání na desce. Celkový počet panelů: {len(sub_jobs)}."

    def parse(self, file_path: Path):
        file_path = Path(file_path)
        file_key = str(file_path.resolve())
        if file_key in self.parsed_files:
            return

        try:
            with open(file_path, 'rb') as f:
                binary_data = f.read()
                
            if len(binary_data) < 64:
                raise ValueError("Soubor je příliš malý (méně než 64 bajtů)")

            file_hash = hashlib.md5(binary_data).hexdigest()

            warnings = []
            tech_notes = []
            fail_safe_flag = False
            thickness_confidence = "LOW"

            if not any(header in binary_data for header in [b"RDVCUT", b"VER1.0.012", b"VER1.0.013", b"VER"]):
                warnings.append("⚠️ Detekována nová verze VCF – vyžadován zásah vývojáře")
                tech_notes.append("⚠️ Detekována nová verze VCF – vyžadován zásah vývojáře")
                fail_safe_flag = True

            try:
                layers_details = self._extract_active_layers_details(binary_data)
                elements = self._parse_geometry_v18_2(binary_data, layers_details)
            except Exception as e:
                warnings.append(f"⚠️ Detekována nová verze VCF nebo chyba parsování – vyžadován zásah vývojáře ({e})")
                tech_notes.append(f"⚠️ Detekována nová verze VCF nebo chyba parsování – vyžadován zásah vývojáře ({e})")
                fail_safe_flag = True
                layers_details = []
                elements = []

            if not fail_safe_flag:
                for el in elements:
                    layer_idx = el["layer_index"]
                    if layer_idx != -1 and layer_idx < len(layers_details):
                        layers_details[layer_idx]["total_cut_length_mm"] += el["length_mm"]

                for l in layers_details:
                    l["total_cut_length_mm"] = round(l["total_cut_length_mm"], 2)

                total_path_length = sum(l["total_cut_length_mm"] for l in layers_details if l["is_output_yes"])
                
                # Výpočet globálního bounding boxu (canvas) a velikosti plochy
                g_min_x, g_min_y = float('inf'), float('inf')
                g_max_x, g_max_y = float('-inf'), float('-inf')
                active_elements_for_canvas = 0

                for el in elements:
                    if el["is_output_yes"] and el.get("bbox") is not None:
                        el_min_x, el_min_y, el_max_x, el_max_y = el["bbox"]
                        if el_min_x < g_min_x: g_min_x = el_min_x
                        if el_min_y < g_min_y: g_min_y = el_min_y
                        if el_max_x > g_max_x: g_max_x = el_max_x
                        if el_max_y > g_max_y: g_max_y = el_max_y
                        active_elements_for_canvas += 1

                if active_elements_for_canvas > 0:
                    canvas_width = g_max_x - g_min_x
                    canvas_height = g_max_y - g_min_y
                    canvas_bbox = [round(g_min_x, 2), round(g_min_y, 2), round(g_max_x, 2), round(g_max_y, 2)]
                else:
                    canvas_width = 0.0
                    canvas_height = 0.0
                    canvas_bbox = [0.0, 0.0, 0.0, 0.0]

                # Normalizace souřadnic elementů k aktivnímu canvasu (Fáze v18.0 / A2)
                if active_elements_for_canvas > 0 and canvas_width > 0 and canvas_height > 0:
                    for el in elements:
                        if el.get("bbox"):
                            el_min_x, el_min_y, el_max_x, el_max_y = el["bbox"]
                            el["bbox_norm"] = [
                                round((el_min_x - g_min_x) / canvas_width, 4),
                                round((el_min_y - g_min_y) / canvas_height, 4),
                                round((el_max_x - g_min_x) / canvas_width, 4),
                                round((el_max_y - g_min_y) / canvas_height, 4)
                            ]
                        else:
                            el["bbox_norm"] = [0.0, 0.0, 0.0, 0.0]
                            
                        if el.get("centroid"):
                            cx, cy = el["centroid"]
                            el["centroid_norm"] = [
                                round((cx - g_min_x) / canvas_width, 4),
                                round((cy - g_min_y) / canvas_height, 4)
                            ]
                        else:
                            el["centroid_norm"] = [0.0, 0.0]
                else:
                    for el in elements:
                        el["bbox_norm"] = [0.0, 0.0, 0.0, 0.0]
                        el["centroid_norm"] = [0.0, 0.0]

                # Heuristika pro odhad tloušťky desky (PET felt 12 vs 24 mm) s detekcí jistoty (Náprava Pitfall 2)
                thickness_confidence = "LOW"
                material_thickness = 12.0
                for l in layers_details:
                    if l["cutter_type"] == "V-slot" and l["is_output_yes"]:
                        h2 = l["end_height_h2_mm"]
                        if abs(h2 - 6.0) < 0.5:
                            material_thickness = 12.0
                            thickness_confidence = "HIGH"
                        elif abs(h2 - 18.0) < 0.5 or abs(h2 - 15.0) < 1.0:
                            material_thickness = 24.0
                            thickness_confidence = "HIGH"
                
                if thickness_confidence == "LOW":
                    fn_lower = file_path.name.lower()
                    if any(pattern in fn_lower for pattern in ["12mm", "12_mm", "12 mm"]):
                        material_thickness = 12.0
                        thickness_confidence = "HIGH"
                    elif any(pattern in fn_lower for pattern in ["24mm", "24_mm", "24 mm"]):
                        material_thickness = 24.0
                        thickness_confidence = "HIGH"

                # Sémantický rozbor vrstev a operací (Fáze v21)
                for idx, l in enumerate(layers_details):
                    h2 = l["end_height_h2_mm"]
                    if l["cutter_type"] == "Vibrate cutter":
                        # Tacit corection: H2 represents height from flatbed, where full cut is <= 0.1 mm
                        if h2 <= 0.1:
                            l["operation_type"] = "Průřez celou tloušťkou materiálu (through-cut)"
                        else:
                            l["operation_type"] = "Mělké řezání / kiss-cut / gravírování"
                    elif l["cutter_type"] == "V-slot":
                        depth = material_thickness - h2
                        l["operation_type"] = f"Dekorativní V-drážka (hloubka řezu: {depth:.1f} mm)"
                    else:
                        l["operation_type"] = "Neznámá CAM operace"

                # Agregace matematických a komplexních metrik pro jednotlivé vrstvy (Fáze v18.1 - B1)
                for idx, l in enumerate(layers_details):
                    layer_elements = [el for el in elements if el["layer_index"] == idx and el["is_output_yes"]]
                    if layer_elements:
                        total_pts = sum(el["point_count"] for el in layer_elements)
                        total_layer_length = sum(el["length_mm"] for el in layer_elements)
                        
                        # Průměrná délka segmentu
                        avg_seg = total_layer_length / total_pts if total_pts > 0 else 0.0
                        
                        # Suma kurvaturních indexů
                        sum_curv_rad = sum(el["complexity"]["curvature_index"] * el["length_mm"] for el in layer_elements)
                        layer_curv_index = sum_curv_rad / total_layer_length if total_layer_length > 0 else 0.0
                        
                        # Ostré rohy a změny směru
                        sharp_corners = sum(el["complexity"]["sharp_corners_count"] for el in layer_elements)
                        dir_changes = sum(el["complexity"]["total_direction_changes"] for el in layer_elements)
                        
                        l["complexity"] = {
                            "avg_segment_length_mm": round(avg_seg, 2),
                            "curvature_index": round(layer_curv_index, 4),
                            "sharp_corners_count": sharp_corners,
                            "total_direction_changes": dir_changes
                        }
                    else:
                        l["complexity"] = {
                            "avg_segment_length_mm": 0.0,
                            "curvature_index": 0.0,
                            "sharp_corners_count": 0,
                            "total_direction_changes": 0
                        }

                # Extrakce a sémantický rozbor sekvence drah (Fáze v18.0 / A1)
                cut_layer_indices = []
                facet_layer_indices = []
                decor_layer_indices = []
                layer_order = []

                for idx, l in enumerate(layers_details):
                    if not l["is_output_yes"]:
                        continue
                    layer_order.append(idx)
                    if l["cutter_type"] == "Vibrate cutter" and l["end_height_h2_mm"] <= 0.1:
                        cut_layer_indices.append(idx)
                    elif l["cutter_type"] == "V-slot":
                        if l.get("direction") in ("Left", "Right"):
                            facet_layer_indices.append(idx)
                        elif l.get("direction") == "Cut both side":
                            decor_layer_indices.append(idx)

                sequence_is_correct = True
                first_cut_type = "N/A"
                last_cut_type = "N/A"

                if layer_order:
                    first_idx = layer_order[0]
                    last_idx = layer_order[-1]
                    first_cut_type = layers_details[first_idx]["cutter_type"]
                    last_cut_type = layers_details[last_idx]["cutter_type"]
                    
                    # Ověření kritického pravidla: Ořez vibračním nožem se provádí vždy jako poslední!
                    if cut_layer_indices:
                        max_cut = max(cut_layer_indices)
                        all_other = facet_layer_indices + decor_layer_indices
                        if all_other and max_cut < max(all_other):
                            sequence_is_correct = False
                            msg = "⚠️ Kritická chyba sekvence: Obvodový ořez (vibrate cutter) probíhá PŘED fasetováním nebo gravírováním! Hrozí posun materiálu a zničení panelu."
                            if msg not in warnings: warnings.append(msg)
                            if msg not in tech_notes: tech_notes.append(msg)
                            
                    # Ověření pořadí faseta -> dekor
                    if facet_layer_indices and decor_layer_indices:
                        if max(facet_layer_indices) > min(decor_layer_indices):
                            tech_notes.append("📝 Sémantická sekvence: Fasetování hran a tvorba dekoru jsou prokládané (interleaved).")
                        else:
                            tech_notes.append("📝 Sémantická sekvence: Výkres správně fasetuje hrany před zahájením vnitřního dekoru.")

                operation_sequence_info = {
                    "layer_order": layer_order,
                    "first_cut_type": first_cut_type,
                    "last_cut_type": last_cut_type,
                    "sequence_is_correct": sequence_is_correct
                }

                # Adaptace na reálné prostředí: Detekce nadrozměrných desek (agregované zakázky)
                # Fyzický stůl plotru je 1600x3000 mm, standardní raw formát desky je 2900x1220 mm (bezpečně sedí celou plochou)
                max_dim = max(canvas_width, canvas_height)
                min_dim = min(canvas_width, canvas_height)
                is_aggregated_job = False
                sub_jobs = []
                spatial_arrangement_description = ""
                
                if max_dim > 3000.0 or min_dim > 1600.0:
                    is_aggregated_job = True
                    msg = f"⚠️ Detekován nadrozměrný bounding box ({canvas_width:.1f} x {canvas_height:.1f} mm). Soubor pravděpodobně obsahuje agregovaná data z více zakázek nebo překračuje standardní formát desky PET feltu (2900 x 1220 mm)."
                    if msg not in warnings: warnings.append(msg)
                    if msg not in tech_notes: tech_notes.append(msg)
                    
                    # Prostorové shlukování (Spatial Clustering) pro rozdělení na samostatné sub-zakázky
                    # Použijeme jednoduchý a rychlý BFS algoritmus s prahem distanční tolerance 250 mm
                    active_elements = [el for el in elements if el["is_output_yes"] and el.get("bbox") is not None]
                    n_el = len(active_elements)
                    visited = [False] * n_el
                    components = []
                    
                    for i in range(n_el):
                        if visited[i]:
                            continue
                        queue = [i]
                        visited[i] = True
                        comp = []
                        head = 0
                        while head < len(queue):
                            curr = queue[head]
                            head += 1
                            comp.append(active_elements[curr])
                            for neighbor in range(n_el):
                                if not visited[neighbor]:
                                    if self._bbox_distance(active_elements[curr]["bbox"], active_elements[neighbor]["bbox"]) <= 250.0:
                                        visited[neighbor] = True
                                        queue.append(neighbor)
                        components.append(comp)
                    
                    # Seřadíme komponenty zleva doprava (podle min_x)
                    components = sorted(components, key=lambda c: min(el["bbox"][0] for el in c))
                    
                    for s_idx, comp in enumerate(components):
                        sub_min_x = min(el["bbox"][0] for el in comp)
                        sub_min_y = min(el["bbox"][1] for el in comp)
                        sub_max_x = max(el["bbox"][0] for el in comp)
                        sub_max_y = max(el["bbox"][1] for el in comp)
                        
                        sub_w = sub_max_x - sub_min_x
                        sub_h = sub_max_y - sub_min_y
                        sub_len = sum(el["length_mm"] for el in comp)
                        
                        sub_jobs.append({
                            "sub_job_id": f"Sub_Job_{s_idx+1}",
                            "bbox": [round(sub_min_x, 2), round(sub_min_y, 2), round(sub_max_x, 2), round(sub_max_y, 2)],
                            "width_mm": round(sub_w, 1),
                            "height_mm": round(sub_h, 1),
                            "num_elements": len(comp),
                            "total_length_mm": round(sub_len, 2),
                            "centroid": [round((sub_min_x + sub_max_x) / 2.0, 2), round((sub_min_y + sub_max_y) / 2.0, 2)]
                        })
                    
                    spatial_arrangement_description = self._analyze_sub_jobs_relation(sub_jobs)
                    tech_notes.append(f"🤖 Prostorový algoritmus úspěšně rozdělil agregovaný soubor na {len(sub_jobs)} samostatných technologických sub-zakázek.")
                    if spatial_arrangement_description:
                        tech_notes.append(f"🗺️ {spatial_arrangement_description}")

                # Sémantická detekce a klasifikace podélného půlení (empirické stínování)
                technological_classification = "Standardní celoplošný panel"
                if active_elements_for_canvas > 0:
                    if 570.0 <= canvas_width <= 620.0 and 2400.0 <= canvas_height <= 2950.0:
                        technological_classification = "Podélně dělený panel (půlený na 2x 600 mm ze standardní šířky 1220 mm s 10mm rezervou prořezu)"
                        tech_notes.append(f"📝 Sémantické zařazení: {technological_classification}")

                # Podezřelé nastavení nulové výšky hrotu
                for idx, l in enumerate(layers_details):
                    if l["is_output_yes"] and l["cutter_type"] in ("Vibrate cutter", "Vibrate cut") and l["end_height_h2_mm"] == 0.0:
                        msg = f"⚠️ Optimalizace výšky: Vrstva {idx+1} ({l['cutter_type']}) má výšku hrotu v ose Z (H2) rovnu 0.0 mm. Hrozí nedoříznutí spodních feltových vláken (ideální výška hrotu v podložce je -0.3 až -0.1 mm)."
                        if msg not in warnings: warnings.append(msg)
                        if msg not in tech_notes: tech_notes.append(msg)

                # Varování o fixaci malých panelů (< 1.67 m² neboli 50 % standardu)
                if active_elements_for_canvas > 0:
                    area_m2 = (canvas_width * canvas_height) / 1000000.0
                    if area_m2 < 1.67:
                        msg = "⚠️ Pozor: Výkres má malou celkovou plochu (odřezek / malý díl). Nutná zvýšená mechanická fixace papírovou páskou (minimálně 80-90 % obvodu) kvůli nízkému vakuovému přítlaku!"
                        if msg not in warnings: warnings.append(msg)
                        if msg not in tech_notes: tech_notes.append(msg)

                # Hluboké zanoření
                for idx, l in enumerate(layers_details):
                    if l["is_output_yes"] and l["total_cut_length_mm"] > 0:
                        if l["cutter_type"] == "V-slot" and abs(l["end_height_h2_mm"] - 9.0) < 0.1:
                            note = "⚠️ Pozor: Hluboké zanoření 9mm (Sandwich 24mm)"
                            if note not in tech_notes:
                                tech_notes.append(note)

                metadata_strings = self._extract_strings(binary_data)
                
                # Panelový kontext, symetrie, mřížka, layout (Fáze v19 / v20 / v17.8)
                shape_groups = self._group_elements(elements)
                format_info = self._detect_panel_format(canvas_width, canvas_height)
                symmetry_info = self._detect_symmetry(elements, canvas_bbox)
                density_grid_info = self._compute_density_grid(elements, canvas_bbox)
                layout_type = self._classify_layout(shape_groups, canvas_bbox)

                # Výpočet topologického stromu hierarchie (Nesting Tree & Containment Hierarchy - Fáze v18.1 - B2)
                # Přiřadíme ID a parent/child indexy všem elementům
                parents_map = {}
                for idx_A, el_A in enumerate(elements):
                    if not el_A.get("is_output_yes") or el_A.get("centroid") is None:
                        continue
                    centroid_A = el_A["centroid"]
                    containing_elements = []
                    for idx_B, el_B in enumerate(elements):
                        if idx_A == idx_B or not el_B.get("is_output_yes") or not el_B.get("is_closed_loop"):
                            continue
                        if self._is_point_inside_element(centroid_A, el_B):
                            containing_elements.append(idx_B)
                    
                    if containing_elements:
                        # Zvolíme rodiče s nejmenší plochou BBoxu (nejbližší obklopující prvek)
                        parent_idx = min(containing_elements, key=lambda idx: (elements[idx]["bbox"][2] - elements[idx]["bbox"][0]) * (elements[idx]["bbox"][3] - elements[idx]["bbox"][1]))
                        parents_map[idx_A] = parent_idx
                        
                # Zapíšeme ID a Parent ID do elementů
                for idx, el in enumerate(elements):
                    el["element_id"] = f"Element_{idx}"
                    if idx in parents_map:
                        el["parent_id"] = f"Element_{parents_map[idx]}"
                    else:
                        el["parent_id"] = None
                        
                    el["children_ids"] = []
                    
                for idx, parent_idx in parents_map.items():
                    elements[parent_idx]["children_ids"].append(f"Element_{idx}")

                # Konstrukce hierarchického stromu
                children_indices_map = {idx: [] for idx in range(len(elements))}
                for idx, parent_idx in parents_map.items():
                    children_indices_map[parent_idx].append(idx)
                    
                root_indices = [idx for idx in range(len(elements)) if elements[idx].get("is_output_yes") and idx not in parents_map]
                
                def build_node(idx):
                    el = elements[idx]
                    return {
                        "element_id": el["element_id"],
                        "geom_type": el["geom_type"],
                        "length_mm": el["length_mm"],
                        "centroid": el["centroid"],
                        "bbox": el["bbox"],
                        "is_closed_loop": el["is_closed_loop"],
                        "children": [build_node(child_idx) for child_idx in children_indices_map[idx]]
                    }
                    
                topology_tree = [build_node(idx) for idx in root_indices]

                # Výpočet matice prostorových rozestupů pro Shape Groups (Proximity Matrix - Fáze v18.1 - B4)
                proximity_matrix = {}
                for sg_i in shape_groups:
                    sg_id_i = sg_i["id"]
                    proximity_matrix[sg_id_i] = {}
                    for sg_j in shape_groups:
                        sg_id_j = sg_j["id"]
                        if sg_id_i == sg_id_j:
                            continue
                        
                        # Hledáme nejkratší vzdálenost mezi libovolnou instancí i a j
                        min_dist = float('inf')
                        for inst_i in sg_i["instances"]:
                            for inst_j in sg_j["instances"]:
                                d = self._bbox_distance(inst_i["bbox"], inst_j["bbox"])
                                if d < min_dist:
                                    min_dist = d
                        proximity_matrix[sg_id_i][sg_id_j] = round(min_dist, 2) if min_dist != float('inf') else 0.0

                # Ploché ML příznaky na úrovni celého souboru (Fáze v18.0 / A4)
                grid_values = []
                if density_grid_info:
                    for row in density_grid_info["grid_data"]:
                        grid_values.extend(row)
                mean_grid = sum(grid_values) / len(grid_values) if grid_values else 0.0
                var_grid = sum((x - mean_grid)**2 for x in grid_values) / len(grid_values) if grid_values else 0.0
                std_grid = math.sqrt(var_grid)

                ml_features = {
                    "total_length_mm": round(total_path_length, 2),
                    "num_layers": len(layers_details),
                    "num_elements": len(elements),
                    "num_shape_groups": len(shape_groups),
                    "max_group_repetitions": max((sg["total_instances_count"] for sg in shape_groups), default=0),
                    "vertical_symmetry_score": symmetry_info["vertical_score_percent"],
                    "horizontal_symmetry_score": symmetry_info["horizontal_score_percent"],
                    "density_grid_mean": round(mean_grid, 4),
                    "density_grid_std": round(std_grid, 4),
                    "has_warning": 1 if warnings else 0,
                    "material_thickness_mm": material_thickness,
                    "panel_width_mm": format_info["panel_width_mm"],
                    "panel_height_mm": format_info["panel_height_mm"],
                    "is_aggregated_job": 1 if is_aggregated_job else 0,
                    "num_sub_jobs": len(sub_jobs) if is_aggregated_job else 1
                }

                # Dynamické vlastnosti vrstev a jejich složitosti do ml_features (až pro 5 vrstev, zbytek nuly)
                for k in range(5):
                    if k < len(layers_details):
                        l = layers_details[k]
                        ml_features[f"layer{k}_speed_mms"] = float(l["speed_mms"])
                        ml_features[f"layer{k}_length_mm"] = float(l["total_cut_length_mm"])
                        ml_features[f"layer{k}_cutter_type_id"] = int(l["cutter_type_id"])
                        ml_features[f"layer{k}_end_height_h2_mm"] = float(l["end_height_h2_mm"])
                        ml_features[f"layer{k}_has_extension"] = 1 if (l.get("starting_extension_mm", 0) > 0 or l.get("ending_extension_mm", 0) > 0) else 0
                        ml_features[f"layer{k}_complexity_avg_seg"] = float(l["complexity"]["avg_segment_length_mm"])
                        ml_features[f"layer{k}_complexity_curvature"] = float(l["complexity"]["curvature_index"])
                        ml_features[f"layer{k}_complexity_corners"] = int(l["complexity"]["sharp_corners_count"])
                        ml_features[f"layer{k}_complexity_dir_changes"] = int(l["complexity"]["total_direction_changes"])
                    else:
                        ml_features[f"layer{k}_speed_mms"] = 0.0
                        ml_features[f"layer{k}_length_mm"] = 0.0
                        ml_features[f"layer{k}_cutter_type_id"] = 0
                        ml_features[f"layer{k}_end_height_h2_mm"] = 0.0
                        ml_features[f"layer{k}_has_extension"] = 0
                        ml_features[f"layer{k}_complexity_avg_seg"] = 0.0
                        ml_features[f"layer{k}_complexity_curvature"] = 0.0
                        ml_features[f"layer{k}_complexity_corners"] = 0
                        ml_features[f"layer{k}_complexity_dir_changes"] = 0

                is_organic = any(kw in file_path.name.lower() for kw in ["deska", "botanic", "circle", "fluenz", "curve", "pcb"])
                t_corner = 0.30 if is_organic else 0.66
                t_lift = 2.2
                t_rot_vslot = 1.5
                vibrate_curve_threshold = 0.2
                vibrate_curve_point_penalty = 1.2
                setup_overhead = 50.0
                
                cut_time_seconds = 0.0
                for idx, l in enumerate(layers_details):
                    if l["is_output_yes"] and l["total_cut_length_mm"] > 0 and l["speed_mms"] > 0:
                        L_cut = l["total_cut_length_mm"]
                        v_cut = l["speed_mms"]
                        
                        if l["cutter_type"] == "V-slot":
                            is_both_side = (l.get("direction") == "Cut both side")
                            mult = 2.0 if is_both_side else 1.0
                            t_cut = (mult * L_cut) / v_cut
                            
                            N_elements = sum(1 for el in elements if el["layer_index"] == idx and el["is_output_yes"])
                            t_lift_layer = N_elements * t_lift
                            t_rot_layer = (N_elements * t_rot_vslot) if is_both_side else 0.0
                            
                            cut_time_seconds += t_cut + t_lift_layer + t_rot_layer
                        else:
                            t_cut = L_cut / v_cut
                            
                            layer_elements = [el for el in elements if el["layer_index"] == idx and el["is_output_yes"]]
                            N_elements = len(layer_elements)
                            t_lift_layer = N_elements * t_lift
                            
                            t_corners_layer = 0.0
                            for el in layer_elements:
                                pts = el["point_count"]
                                length = el["length_mm"]
                                avg_seg_len = length / pts if pts > 0 else 0.0
                                
                                if avg_seg_len < vibrate_curve_threshold and l["cutter_type"] == "Vibrate cutter":
                                    t_corners_layer += pts * vibrate_curve_point_penalty
                                else:
                                    t_corners_layer += pts * t_corner
                            
                            cut_time_seconds += t_cut + t_lift_layer + t_corners_layer
                
                N_active = sum(1 for el in elements if el["is_output_yes"])
                t_traverse = ((N_active - 1) * 150.0) / 500.0 if N_active > 1 else 0.0
                t_return = 15.0 if N_active > 0 else 0.0
                
                predicted_seconds = setup_overhead + cut_time_seconds + t_traverse + t_return
            else:
                total_path_length = 0.0
                predicted_seconds = 0.0
                metadata_strings = []
                canvas_width = 0.0
                canvas_height = 0.0
                canvas_bbox = [0.0, 0.0, 0.0, 0.0]
                shape_groups = []
                format_info = {"format_name": "Atypický", "panel_width_mm": 0.0, "panel_height_mm": 0.0, "is_atypical": True}
                symmetry_info = {"has_vertical": False, "vertical_score_percent": 0, "has_horizontal": False, "horizontal_score_percent": 0, "summary": "Symetrie chybí"}
                density_grid_info = None
                layout_type = "freeform"
                material_thickness = 12.0
                operation_sequence_info = {"layer_order": [], "first_cut_type": "N/A", "last_cut_type": "N/A", "sequence_is_correct": True}
                technological_classification = "Atypický"
                ml_features = {}
                topology_tree = []
                proximity_matrix = {}
                is_aggregated_job = False
                sub_jobs = []
                spatial_arrangement_description = ""

            # --- INTEGRACE SEMANTICKEHO VALIDAČNÍHO ENGINE (v18.3) ---
            semantic_warnings = []
            kb_enabled = False
            risk_score = 0.0
            
            if KB_AVAILABLE and not fail_safe_flag:
                try:
                    current_dir = Path(__file__).resolve().parent
                    rules_json_path = current_dir / "Knowledge_base" / "rules.json"
                    kb_engine = KnowledgeBaseEngine(str(rules_json_path))
                    
                    kb_results = kb_engine.validate_all(
                        layers=layers_details,
                        elements=elements,
                        material_thickness=material_thickness,
                        thickness_confidence=thickness_confidence,
                        canvas_width=canvas_width,
                        canvas_height=canvas_height,
                        filename=file_path.name
                    )
                    
                    for res in kb_results:
                        semantic_warnings.append(res.to_dict())
                        
                        # Přidání sémantických varování pro zpětnou kompatibilitu
                        if res.severity in ["WARNING", "CRITICAL"]:
                            msg = f"⚠️ {res.message}"
                            if msg not in warnings:
                                warnings.append(msg)
                        msg_tech = f"📝 [{res.severity.value}] {res.message}"
                        if msg_tech not in tech_notes:
                            tech_notes.append(msg_tech)
                    
                    risk_score = len([w for w in semantic_warnings if w["severity"] == "CRITICAL"]) * 0.5 + \
                                 len([w for w in semantic_warnings if w["severity"] == "WARNING"]) * 0.2
                    kb_enabled = True
                except Exception as e:
                    tech_notes.append(f"❌ Chyba vyhodnocení sémantické vrstvy: {str(e)}")

            # Čisté odstraňování nepotřebných velkých polí před serializací, aby byl JSON čitelný
            # Odstraníme "vertices" z elements, protože pro JSON je to příliš velké (ale necháme bbox a centroid)
            for el in elements:
                if "vertices" in el:
                    del el["vertices"]

            self.parsed_files[file_key] = {
                "filename": file_path.name,
                "filepath": str(file_path),
                "file_hash": file_hash,
                "warnings": warnings,
                "tech_notes": tech_notes,
                "file_size_bytes": len(binary_data),
                "extracted_metadata": metadata_strings,
                "elements_parsed": len(elements),
                "elements": elements,
                "layers": layers_details,
                "fail_safe_flag": fail_safe_flag,
                "canvas_width_mm": round(canvas_width, 1) if not fail_safe_flag else 0.0,
                "canvas_height_mm": round(canvas_height, 1) if not fail_safe_flag else 0.0,
                "canvas_bbox": canvas_bbox if not fail_safe_flag else [0.0, 0.0, 0.0, 0.0],
                "shape_groups": shape_groups,
                "detected_panel_format_name": format_info["format_name"],
                "detected_panel_width_mm": format_info["panel_width_mm"],
                "detected_panel_height_mm": format_info["panel_height_mm"],
                "symmetry": symmetry_info,
                "density_grid": density_grid_info,
                "layout_type": layout_type,
                "material_thickness_mm": material_thickness,
                "manufacturing_intelligence": {
                    "enabled": kb_enabled,
                    "semantic_warnings": semantic_warnings,
                    "risk_score": round(risk_score, 2),
                    "material_thickness_confidence": str(thickness_confidence)
                },
                "operation_sequence": operation_sequence_info,
                "technological_classification": technological_classification,
                "normalized_coords_included": True if not fail_safe_flag else False,
                "is_aggregated_job": is_aggregated_job,
                "spatial_arrangement_description": spatial_arrangement_description,
                "sub_jobs": sub_jobs,
                "topology_tree": topology_tree,
                "proximity_matrix": proximity_matrix,
                "ml_features": ml_features,
                "erp_time_prediction": {
                    "total_path_length_mm": round(total_path_length, 2),
                    "predicted_time_seconds": int(predicted_seconds),
                    "predicted_time_formatted": self._format_time(int(predicted_seconds)) if not fail_safe_flag else "⚠️ Neanalyzováno"
                }
            }

        except Exception as e:
            self.parsed_files[file_key] = {
                "filename": file_path.name,
                "filepath": str(file_path),
                "file_hash": "unknown",
                "warnings": [f"⚠️ Detekována nová verze VCF nebo chyba parsování – vyžadován zásah vývojáře ({e})"],
                "tech_notes": [f"⚠️ Detekována nová verze VCF nebo chyba parsování – vyžadován zásah vývojáře ({e})"],
                "file_size_bytes": 0,
                "extracted_metadata": [],
                "elements_parsed": 0,
                "elements": [],
                "layers": [],
                "fail_safe_flag": True,
                "canvas_width_mm": 0.0,
                "canvas_height_mm": 0.0,
                "canvas_bbox": [0.0, 0.0, 0.0, 0.0],
                "shape_groups": [],
                "detected_panel_format_name": "Atypický",
                "detected_panel_width_mm": 0.0,
                "detected_panel_height_mm": 0.0,
                "symmetry": {"has_vertical": False, "vertical_score_percent": 0, "has_horizontal": False, "horizontal_score_percent": 0, "summary": "Symetrie chybí"},
                "density_grid": None,
                "layout_type": "freeform",
                "material_thickness_mm": 12.0,
                "operation_sequence": {"layer_order": [], "first_cut_type": "N/A", "last_cut_type": "N/A", "sequence_is_correct": True},
                "technological_classification": "Neznámá",
                "normalized_coords_included": False,
                "is_aggregated_job": False,
                "spatial_arrangement_description": "",
                "sub_jobs": [],
                "topology_tree": [],
                "proximity_matrix": {},
                "ml_features": {},
                "erp_time_prediction": {
                    "total_path_length_mm": 0.0,
                    "predicted_time_seconds": 0,
                    "predicted_time_formatted": "⚠️ Neanalyzováno"
                }
            }

    def run(self):
        raw_vcfs = list(self.directory_path.rglob('*.VCF')) + list(self.directory_path.rglob('*.vcf'))
        vcfs = set()
        for p in raw_vcfs:
            if "_report.json" in p.name or "CNC_cas_report.json" in p.name:
                continue
            vcfs.add(p.resolve())
            
        vcfs_list = sorted(list(vcfs))
        
        print(f"[*] Nalezeno souborů k analýze: {len(vcfs_list)}")
        
        for p in vcfs_list:
            self.parse(p)

        run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_timestamp_display = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Generování sidecarů
        if self.output_mode in ("sidecar", "both"):
            for file_key, item in self.parsed_files.items():
                filepath = Path(item["filepath"])
                parent_dir = filepath.parent
                vcf_base_name = filepath.stem
                vcf_base_name = re.sub(r'[^\w\-]', '_', vcf_base_name)
                
                sidecar_json_name = f"{vcf_base_name}_analysis_v18_3.json"
                sidecar_md_name = f"{vcf_base_name}_analysis_v18_3.md"
                
                sidecar_json_path = parent_dir / sidecar_json_name
                sidecar_md_path = parent_dir / sidecar_md_name
                
                try:
                    with open(sidecar_json_path, 'w', encoding='utf-8') as sf:
                        json.dump(item, sf, indent=4, ensure_ascii=False)
                except Exception as e:
                    print(f"[-] Chyba zápisu JSON sidecaru {sidecar_json_path}: {e}")
                    
                try:
                    ascii_grid_md = ""
                    grid_info = item.get("density_grid")
                    if grid_info and item.get("canvas_bbox") and item["canvas_bbox"] != [0.0, 0.0, 0.0, 0.0]:
                        grid = grid_info["grid_data"]
                        ascii_rows = []
                        for r in range(7, -1, -1):
                            row_str = " | ".join(f"{grid[r][c]:2d}" for c in range(8))
                            ascii_rows.append(f"| {row_str} |")
                        ascii_grid_md = "\n".join(ascii_rows)

                    with open(sidecar_md_path, 'w', encoding='utf-8') as sf:
                        sf.write(f"# 🔬 VCF Report v18.2: {item['filename']} (ML-Enhanced)\n\n")
                        sf.write(f"- **Složka:** {parent_dir.name}\n")
                        sf.write(f"- **Čas analýzy:** {run_timestamp_display}\n")
                        if item.get('warnings'):
                            sf.write(f"- ⚠️ **Varování:** {', '.join(item['warnings'])}\n")
                        if item.get('tech_notes'):
                            sf.write(f"- 📝 **Technologické poznámky:** {', '.join(item['tech_notes'])}\n")
                        
                        sf.write(f"- **Predikce času (Kinematický model):** {item['erp_time_prediction']['predicted_time_formatted']} (na základě aktivní dráhy: **{item['erp_time_prediction']['total_path_length_mm']} mm**)\n")
                        if not item.get("fail_safe_flag"):
                            sf.write(f"- **Rozměry aktivní plochy (Canvas):** {item['canvas_width_mm']:.1f} x {item['canvas_height_mm']:.1f} mm (BBox: {item['canvas_bbox']})\n")
                            sf.write(f"- **Detekovaný formát panelu:** {item['detected_panel_format_name']} ({item['detected_panel_width_mm']:.0f} x {item['detected_panel_height_mm']:.0f} mm)\n")
                            sf.write(f"- **Odhadovaná tloušťka feltu:** {item['material_thickness_mm']:.0f} mm\n")
                            if "manufacturing_intelligence" in item and item["manufacturing_intelligence"]["enabled"]:
                                mi = item["manufacturing_intelligence"]
                                sf.write(f"- **Sémantický index rizika (Risk Score):** `{mi['risk_score']}`\n")
                                sf.write(f"- **Jistota odhadu tloušťky:** `{mi['material_thickness_confidence']}`\n")
                            sf.write(f"- **Sémantická klasifikace:** `{item['technological_classification']}`\n")
                            sf.write(f"- **Agregovaný soubor (Oversized):** `{'Ano' if item['is_aggregated_job'] else 'Ne'}`\n")
                        sf.write(f"- **Počet uložených elementů/instrukcí:** {item['elements_parsed']}\n\n")
                        
                        # Sub-zakázky
                        if item.get("is_aggregated_job") and item.get("sub_jobs"):
                            sf.write(f"### 📦 Rozdělení na samostatné sub-zakázky (Prostorové shlukování)\n")
                            sf.write("Surový soubor přesahuje standardní rozměr desky. Algoritmus identifikoval následující technologické celky:\n\n")
                            if item.get("spatial_arrangement_description"):
                                sf.write(f"🗺️ **Uspořádání:** {item['spatial_arrangement_description']}\n\n")
                            for sj in item["sub_jobs"]:
                                sf.write(f"  - **{sj['sub_job_id']}:** Rozměry: {sj['width_mm']:.1f} x {sj['height_mm']:.1f} mm, BBox: {sj['bbox']}, Prvků: {sj['num_elements']}, Délka řezu: {sj['total_length_mm']} mm\n")
                            sf.write("\n")

                        # Technologická analýza sekvence
                        if not item.get("fail_safe_flag"):
                            sf.write(f"### ⚙️ Technologická sekvence a analýza\n")
                            seq = item["operation_sequence"]
                            status_seq = "✅ V pořádku (ořez je na konci)" if seq["sequence_is_correct"] else "❌ CHYBA SEKENCE (ořez probíhá dříve!)"
                            sf.write(f"- **Pořadí vrstev (Indexy):** `{seq['layer_order']}`\n")
                            sf.write(f"- **První aktivní nástroj:** `{seq['first_cut_type']}`\n")
                            sf.write(f"- **Poslední aktivní nástroj:** `{seq['last_cut_type']}`\n")
                            sf.write(f"- **Status sekvence:** {status_seq}\n\n")

                        # Prostorová analýza
                        if not item.get("fail_safe_flag"):
                            sf.write(f"### 🌐 Prostorová analýza\n")
                            sf.write(f"- **Klasifikace rozvržení (Layout):** `{item['layout_type']}`\n")
                            sf.write(f"- **Symetrie výkresu:** {item['symmetry']['summary']}\n")
                            if grid_info:
                                sf.write(f"- **Hustotní analýza:** {grid_info['summary']} (Buňka: {grid_info['cell_size_mm'][0]}x{grid_info['cell_size_mm'][1]} mm)\n")
                                sf.write(f"```\n{ascii_grid_md}\n```\n")
                            sf.write("\n")

                        # Proximity Matrix
                        if item.get("proximity_matrix"):
                            sf.write(f"### 📐 Matice prostorových rozestupů (Proximity Matrix, mm)\n")
                            sf.write("Nejkratší vzdálenosti mezi ohraničujícími obdélníky jednotlivých Shape Groups:\n\n")
                            groups_list = sorted(item["proximity_matrix"].keys())
                            sf.write("| Skupina | " + " | ".join(groups_list) + " |\n")
                            sf.write("| --- | " + " | ".join("---" for _ in groups_list) + " |\n")
                            for g_i in groups_list:
                                row_cells = []
                                for g_j in groups_list:
                                    if g_i == g_j:
                                        row_cells.append("-")
                                    else:
                                        row_cells.append(f"{item['proximity_matrix'][g_i].get(g_j, 0.0):.1f}")
                                sf.write(f"| **{g_i}** | " + " | ".join(row_cells) + " |\n")
                            sf.write("\n")

                        # Opakující se tvary (Shape Groups)
                        if item.get("shape_groups"):
                            sf.write(f"### 🗃️ Detekované opakující se tvary (Shape Groups):\n")
                            for sg in item["shape_groups"]:
                                sf.write(f"  - **{sg['id']}:** {sg['geom_type']}, Segmentů: {sg['point_count']}, Délka: {sg['length_mm']} mm, Velikost BBoxu: {sg['bbox_size'][0]}x{sg['bbox_size'][1]} mm \u2192 **{sg['total_instances_count']}x výskyt**\n")
                            sf.write("\n")

                        # Hierarchické uspořádání
                        if item.get("topology_tree"):
                            sf.write(f"### 🌳 Topologická hierarchie a hnízdění (Topology Tree)\n")
                            sf.write("Sémantická struktura vnořených prvků (Ray-Casting):\n\n")
                            def write_tree_node(node, depth=0):
                                indent = "  " * depth
                                loop_status = "Uzavřená smyčka" if node["is_closed_loop"] else "Otevřená dráha"
                                sf.write(f"{indent}- **{node['element_id']}** ({node['geom_type']}, {node['length_mm']:.1f} mm, {loop_status})\n")
                                for child in node["children"]:
                                    write_tree_node(child, depth + 1)
                            for root_node in item["topology_tree"][:10]: # Vypisujeme prvních 10 hlavních uzlů pro čitelnost
                                write_tree_node(root_node)
                            if len(item["topology_tree"]) > 10:
                                sf.write(f"  - *... a dalších {len(item['topology_tree']) - 10} hlavních prvků.*\n")
                            sf.write("\n")

                        sf.write(f"### Ukázka elementů (prvních 15 s normalizovanými souřadnicemi a matematikou):\n")
                        for el in item['elements'][:15]:
                            layer_name = f"Vrstva {el['layer_index']+1}" if el['layer_index'] != -1 else "Neznámá"
                            out_status = "OUTPUT: YES" if el["is_output_yes"] else "OUTPUT: NO"
                            bbox_str = f"BBox: [{el['bbox'][0]:.1f}, {el['bbox'][1]:.1f}] -> [{el['bbox'][2]:.1f}, {el['bbox'][3]:.1f}]" if el.get('bbox') else "BBox: N/A"
                            centroid_str = f"Centroid: ({el['centroid'][0]:.1f}, {el['centroid'][1]:.1f})" if el.get('centroid') else "Centroid: N/A"
                            norm_str = f"Norm-Centroid: ({el['centroid_norm'][0]:.2f}, {el['centroid_norm'][1]:.2f})" if el.get('centroid_norm') else ""
                            loop_str = "Uzavřená" if el["is_closed_loop"] else "Otevřená"
                            comp_str = f"Zatáčky: {el['complexity']['total_direction_changes']} | Rohy: {el['complexity']['sharp_corners_count']} | Křivost: {el['complexity']['curvature_index']:.4f}"
                            sf.write(f"  - Geometrie: {el['geom_type']} [@ {el['offset']}], Délka: {el['length_mm']} mm | {bbox_str} | {centroid_str} | {norm_str} | {loop_str} | {comp_str} | Vrstva: {layer_name} ({out_status})\n")
                        if len(item['elements']) > 15:
                            sf.write(f"  - *... a dalších {len(item['elements']) - 15} elementů.*\n")
                        sf.write("\n")

                        sf.write(f"### Vrstvy (Fyzikální a matematická složitost):\n")
                        for idx, layer in enumerate(item['layers']):
                            out_status = "Aktivní (Output: YES)" if layer["is_output_yes"] else "Pouze vizuální (Output: NO)"
                            readable_color = self._get_color_name(layer['color_hex'])
                            sf.write(f"  - **Vrstva {idx+1}:** Rychlost {layer['speed_mms']} mm/s | Nástroj: {layer['cutter_type']} (ID: {layer['cutter_type_id']}) | Operace: `{layer['operation_type']}` | Barva: {readable_color} | Status: {out_status}\n")
                            sf.write(f"    - Délka dráhy vrstvy: {layer['total_cut_length_mm']} mm\n")
                            sf.write(f"    - Složitost vrstvy (Complexity): Prům. segment: {layer['complexity']['avg_segment_length_mm']:.1f} mm | Ostré rohy: {layer['complexity']['sharp_corners_count']} | Změny směru: {layer['complexity']['total_direction_changes']} | Index křivosti: {layer['complexity']['curvature_index']:.4f}\n")
                            sf.write(f"    - Tool feeding (Počet: {layer['number_of_feeding']}, Bezpečnostní rovina H1: {layer['travel_safety_height_mm']} mm, Výška hrotu H2: {layer['end_height_h2_mm']} mm)\n")
                            sf.write(f"    - Starting Extension: {layer['starting_extension_mm']} mm | Ending Extension: {layer['ending_extension_mm']} mm\n")
                            if layer['cutter_type'] == "V-slot":
                                sf.write(f"    - Směr řezu (Direction): {layer['direction']} (ID: {layer['direction_id']})\n")
                                sf.write(f"    - V-slot Width Comp: {layer['v_slot_width_comp_mm']} mm\n")
                        sf.write("\n")
                except Exception as e:
                    print(f"[-] Chyba zápisu MD sidecaru {sidecar_md_path}: {e}")

        # Generování master reportů
        if self.output_mode in ("master", "both"):
            folder_name = self.directory_path.name if self.directory_path.name else "root"
            folder_name = re.sub(r'[^\w\-]', '_', folder_name)
            
            json_output = self.output_dir / f"vcf_deep_analysis_v18_3_{folder_name}_final.json"
            md_output = self.output_dir / f"vcf_analysis_report_v18_3_{folder_name}.md"

            try:
                with open(json_output, 'w', encoding='utf-8') as f:
                    json.dump(list(self.parsed_files.values()), f, indent=4, ensure_ascii=False)
                    
                with open(md_output, 'w', encoding='utf-8') as f:
                    f.write(f"# 🔬 V18.3 Report: Advanced Physical & Kinematic Model Solver (ML-Enhanced)\n\n")
                    f.write(f"- **Analyzovaná složka:** {self.directory_path}\n")
                    f.write(f"- **Čas generování:** {run_timestamp_display}\n")
                    f.write("Tento přehled obsahuje agregované výsledky analýzy pro všechny zpracované soubory.\n\n")
                    
                    for item in sorted(self.parsed_files.values(), key=lambda x: x["filename"]):
                        f.write(f"## 📄 {item['filename']}\n")
                        if item.get('warnings'):
                            f.write(f"⚠️ **Varování:** {', '.join(item['warnings'])}\n")
                        if item.get('tech_notes'):
                            f.write(f"📝 **Technologické poznámky:** {', '.join(item['tech_notes'])}\n")
                        
                        f.write(f"- **Predikce času (Kinematický model):** {item['erp_time_prediction']['predicted_time_formatted']} (na základě aktivní dráhy: **{item['erp_time_prediction']['total_path_length_mm']} mm**)\n")
                        if not item.get("fail_safe_flag"):
                            f.write(f"- **Rozměry aktivní plochy (Canvas):** {item['canvas_width_mm']:.1f} x {item['canvas_height_mm']:.1f} mm (BBox: {item['canvas_bbox']})\n")
                            f.write(f"- **Detekovaný formát panelu:** {item['detected_panel_format_name']} ({item['detected_panel_width_mm']:.0f} x {item['detected_panel_height_mm']:.0f} mm)\n")
                            f.write(f"- **Odhadovaná tloušťka feltu:** {item['material_thickness_mm']:.0f} mm\n")
                            if "manufacturing_intelligence" in item and item["manufacturing_intelligence"]["enabled"]:
                                mi = item["manufacturing_intelligence"]
                                f.write(f"- **Sémantický index rizika (Risk Score):** `{mi['risk_score']}`\n")
                                f.write(f"- **Jistota odhadu tloušťky:** `{mi['material_thickness_confidence']}`\n")
                            f.write(f"- **Sémantická klasifikace:** `{item['technological_classification']}`\n")
                            f.write(f"- **Agregovaný soubor (Oversized):** `{'Ano' if item['is_aggregated_job'] else 'Ne'}`\n")
                        f.write(f"- **Počet uložených elementů/instrukcí:** {item['elements_parsed']}\n")
                        
                        # Sub-zakázky
                        if item.get("is_aggregated_job") and item.get("sub_jobs"):
                            f.write(f"#### 📦 Rozdělení na sub-zakázky\n")
                            if item.get("spatial_arrangement_description"):
                                f.write(f"  - **Uspořádání:** {item['spatial_arrangement_description']}\n\n")
                            for sj in item["sub_jobs"]:
                                f.write(f"  - **{sj['sub_job_id']}:** Rozměry: {sj['width_mm']:.1f} x {sj['height_mm']:.1f} mm, BBox: {sj['bbox']}, Prvků: {sj['num_elements']}, Délka řezu: {sj['total_length_mm']} mm\n")
                            f.write("\n")

                        # Technologická sekvence
                        if not item.get("fail_safe_flag"):
                            f.write(f"#### ⚙️ Technologická sekvence a analýza\n")
                            seq = item["operation_sequence"]
                            status_seq = "✅ V pořádku (ořez je na konci)" if seq["sequence_is_correct"] else "❌ CHYBA SEKENCE (ořez probíhá dříve!)"
                            f.write(f"  - **Pořadí vrstev (Indexy):** `{seq['layer_order']}`\n")
                            f.write(f"  - **První aktivní nástroj:** `{seq['first_cut_type']}`\n")
                            f.write(f"  - **Poslední aktivní nástroj:** `{seq['last_cut_type']}`\n")
                            f.write(f"  - **Status sekvence:** {status_seq}\n\n")

                        if not item.get("fail_safe_flag"):
                            f.write(f"#### 🌐 Prostorová analýza\n")
                            f.write(f"  - **Klasifikace rozvržení (Layout):** `{item['layout_type']}`\n")
                            f.write(f"  - **Symetrie výkresu:** {item['symmetry']['summary']}\n")
                            grid_info = item.get("density_grid")
                            if grid_info:
                                f.write(f"  - **Hustotní analýza:** {grid_info['summary']} (Buňka: {grid_info['cell_size_mm'][0]}x{grid_info['cell_size_mm'][1]} mm)\n")
                            f.write("\n")

                        if item.get("shape_groups"):
                            f.write(f"#### 🗃️ Detekované opakující se tvary (Shape Groups):\n")
                            for sg in item["shape_groups"]:
                                f.write(f"  - **{sg['id']}:** {sg['geom_type']}, Segmentů: {sg['point_count']}, Délka: {sg['length_mm']} mm, Velikost BBoxu: {sg['bbox_size'][0]}x{sg['bbox_size'][1]} mm \u2192 **{sg['total_instances_count']}x výskyt**\n")
                            f.write("\n")

                        f.write(f"#### Vrstvy (Fyzikální a matematická složitost):\n")
                        for idx, layer in enumerate(item['layers']):
                            out_status = "Aktivní (Output: YES)" if layer["is_output_yes"] else "Pouze vizuální (Output: NO)"
                            readable_color = self._get_color_name(layer['color_hex'])
                            f.write(f"  - **Vrstva {idx+1}:** Rychlost {layer['speed_mms']} mm/s | Nástroj: {layer['cutter_type']} (ID: {layer['cutter_type_id']}) | Operace: `{layer['operation_type']}` | Barva: {readable_color} | Status: {out_status}\n")
                            f.write(f"    - Délka dráhy vrstvy: {layer['total_cut_length_mm']} mm\n")
                            f.write(f"    - Složitost vrstvy (Complexity): Prům. segment: {layer['complexity']['avg_segment_length_mm']:.1f} mm | Ostré rohy: {layer['complexity']['sharp_corners_count']} | Změny směru: {layer['complexity']['total_direction_changes']} | Index křivosti: {layer['complexity']['curvature_index']:.4f}\n")
                            f.write(f"    - Tool feeding (Počet: {layer['number_of_feeding']}, Bezpečnostní rovina H1: {layer['travel_safety_height_mm']} mm, Výška hrotu H2: {layer['end_height_h2_mm']} mm)\n")
                        f.write("\n")
                print(f"[+] Globální reporty úspěšně vytvořeny!")
            except Exception as e:
                print(f"[-] Chyba při generování globálních reportů: {e}")

def main():
    parser = argparse.ArgumentParser(description="Ruida VCF Deep Parser V18.3")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory with VCF files")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory for master reports")
    parser.add_argument("--output-mode", "-m", choices=["master", "sidecar", "both"], default="both", help="Generate master, sidecars, or both")

    args = parser.parse_args()

    input_path = Path(args.input_dir)
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    r_parser = RuidaVcfDeepParserV18_3(
        directory_path=str(input_path),
        output_dir=args.output_dir,
        output_mode=args.output_mode
    )
    r_parser.run()

if __name__ == "__main__":
    main()
