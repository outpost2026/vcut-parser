import json
import os
from typing import List, Dict, Any, Optional
from .models import (
    RuleClass, ValidationStatus, Severity, ThicknessConfidence,
    EpistemicMetadata, H2Rule, SequenceRule, FixationRule, ValidationResult
)

class KnowledgeBaseEngine:
    def __init__(self, rules_json_path: Optional[str] = None):
        if rules_json_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            rules_json_path = os.path.join(current_dir, "rules.json")
        self.rules_json_path = rules_json_path
        self.h2_rules: List[H2Rule] = []
        self.sequence_rules: List[SequenceRule] = []
        self.fixation_rules: List[FixationRule] = []
        self.load_rules()

    def load_rules(self):
        if not os.path.exists(self.rules_json_path):
            return
        with open(self.rules_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for r in data.get("h2_rules", []):
                meta_dict = r["metadata"]
                meta = EpistemicMetadata(
                    rule_id=meta_dict["rule_id"], description=meta_dict["description"],
                    source=meta_dict["source"], confidence=meta_dict["confidence"],
                    validation_status=ValidationStatus(meta_dict.get("validation_status", "accepted")),
                    rule_class=RuleClass(meta_dict["rule_class"])
                )
                self.h2_rules.append(H2Rule(
                    metadata=meta, cutter_type_id=r["cutter_type_id"],
                    material_thickness_mm=r["material_thickness_mm"],
                    ideal_h2_range=r["ideal_h2_range"], critical_h2_threshold=r["critical_h2_threshold"]
                ))
            for r in data.get("sequence_rules", []):
                meta_dict = r["metadata"]
                meta = EpistemicMetadata(
                    rule_id=meta_dict["rule_id"], description=meta_dict["description"],
                    source=meta_dict["source"], confidence=meta_dict["confidence"],
                    validation_status=ValidationStatus(meta_dict.get("validation_status", "accepted")),
                    rule_class=RuleClass(meta_dict["rule_class"])
                )
                self.sequence_rules.append(SequenceRule(
                    metadata=meta, check_nesting_hierarchy=r.get("check_nesting_hierarchy", True),
                    must_cut_last_cutter_id=r.get("must_cut_last_cutter_id", 1)
                ))
            for r in data.get("fixation_rules", []):
                meta_dict = r["metadata"]
                meta = EpistemicMetadata(
                    rule_id=meta_dict["rule_id"], description=meta_dict["description"],
                    source=meta_dict["source"], confidence=meta_dict["confidence"],
                    validation_status=ValidationStatus(meta_dict.get("validation_status", "accepted")),
                    rule_class=RuleClass(meta_dict["rule_class"])
                )
                self.fixation_rules.append(FixationRule(
                    metadata=meta, min_area_m2_no_tape=r.get("min_area_m2_no_tape", 1.67),
                    critical_area_m2=r.get("critical_area_m2", 0.5),
                    tape_perimeter_coverage_pct=r.get("tape_perimeter_coverage_pct", 80.0)
                ))

    def validate_h2(self, layer: Dict[str, Any], material_thickness: float, thickness_confidence: Any) -> List[ValidationResult]:
        results = []
        h2 = layer.get("end_height_h2_mm", 0.0)
        cutter_id = layer.get("cutter_type_id")
        cutter_type = layer.get("cutter_type", "Unknown")
        for rule in self.h2_rules:
            if rule.cutter_type_id == cutter_id and rule.material_thickness_mm == material_thickness:
                meta = rule.metadata
                depth_cut = material_thickness - h2
                is_low_conf = (str(thickness_confidence) == "LOW")
                if h2 > rule.critical_h2_threshold:
                    severity = Severity.INFO if is_low_conf else Severity.CRITICAL
                    msg_status = " (Odhad s nízkou jistotou)" if is_low_conf else ""
                    results.append(ValidationResult(
                        rule_id=meta.rule_id, rule_class=meta.rule_class,
                        severity=severity, code="H2_NO_CUT_THROUGH",
                        message=(f"Kritické riziko{msg_status}: Nástroj '{cutter_type}' má výšku hrotu H2={h2} mm. "
                                 f"Hloubka řezu pouze {depth_cut:.1f} mm do materiálu o tloušťce {material_thickness} mm."),
                        confidence=meta.confidence * (0.5 if is_low_conf else 1.0),
                        traceable_context={"layer_index": layer.get("layer_index"), "h2": h2, "estimated_thickness": material_thickness}
                    ))
                elif not (rule.ideal_h2_range[0] <= h2 <= rule.ideal_h2_range[1]):
                    severity = Severity.INFO if (is_low_conf or h2 == 0.0) else Severity.WARNING
                    results.append(ValidationResult(
                        rule_id=meta.rule_id, rule_class=meta.rule_class,
                        severity=severity, code="H2_SUBOPTIMAL",
                        message=(f"Optimalizace výšky: H2={h2} mm pro '{cutter_type}'. "
                                 f"Doporučená výška hrotu pro prořez je {rule.ideal_h2_range[0]} až {rule.ideal_h2_range[1]} mm."),
                        confidence=meta.confidence,
                        traceable_context={"layer_index": layer.get("layer_index"), "h2": h2, "estimated_thickness": material_thickness}
                    ))
        return results

    def validate_sequence(self, layers: List[Dict[str, Any]], elements: List[Dict[str, Any]]) -> List[ValidationResult]:
        results = []
        for rule in self.sequence_rules:
            meta = rule.metadata
            active_layers = [idx for idx, l in enumerate(layers) if l.get("is_output_yes") and l.get("total_cut_length_mm", 0.0) > 0.0]
            vibrate_layers = [idx for idx, l in enumerate(layers) if l.get("cutter_type_id") == rule.must_cut_last_cutter_id and l.get("is_output_yes") and l.get("total_cut_length_mm", 0.0) > 0.0]
            if vibrate_layers and active_layers:
                max_vibrate = max(vibrate_layers)
                if max_vibrate < max(active_layers):
                    results.append(ValidationResult(
                        rule_id=meta.rule_id, rule_class=meta.rule_class,
                        severity=Severity.CRITICAL, code="SEQUENCE_LAYER_ERROR",
                        message="Kritická chyba: Obvodový ořez vibračním nožem probíhá před dekorativními operacemi! Hrozí posun panelu.",
                        confidence=meta.confidence
                    ))
            if rule.check_nesting_hierarchy:
                for el in elements:
                    parent_id = el.get("parent_id")
                    if parent_id:
                        parent_el = next((x for x in elements if x["element_id"] == parent_id), None)
                        if parent_el:
                            try:
                                el_offset = int(el["offset"], 16)
                                parent_offset = int(parent_el["offset"], 16)
                                if el_offset > parent_offset:
                                    results.append(ValidationResult(
                                        rule_id=f"{meta.rule_id}_NESTING_OFFSET", rule_class=meta.rule_class,
                                        severity=Severity.WARNING, code="SEQUENCE_NESTING_ERROR",
                                        message=f"Riziko posunu: Vnitřní prvek ({el['element_id']}) se řeže PO svém vnějším obvodu ({parent_id}).",
                                        confidence=meta.confidence * 0.9,
                                        traceable_context={"element_id": el["element_id"], "parent_id": parent_id,
                                                           "element_offset": el["offset"], "parent_offset": parent_el["offset"]}
                                    ))
                            except (ValueError, KeyError):
                                pass
        return results

    def validate_fixation(self, canvas_width: float, canvas_height: float) -> List[ValidationResult]:
        results = []
        if canvas_width <= 0 or canvas_height <= 0:
            return results
        area_m2 = (canvas_width * canvas_height) / 1000000.0
        for rule in self.fixation_rules:
            meta = rule.metadata
            if area_m2 < rule.min_area_m2_no_tape:
                severity = Severity.CRITICAL if area_m2 < rule.critical_area_m2 else Severity.WARNING
                results.append(ValidationResult(
                    rule_id=meta.rule_id, rule_class=meta.rule_class,
                    severity=severity, code="VACUUM_FIXATION_RISK",
                    message=(f"Plocha výkresu je velmi malá ({area_m2:.2f} m²). "
                             f"Nutná mechanická fixace papírovou páskou podél {rule.tape_perimeter_coverage_pct}% obvodu!"),
                    confidence=meta.confidence,
                    traceable_context={"area_m2": round(area_m2, 3)}
                ))
        return results

    def validate_all(self, layers: List[Dict[str, Any]], elements: List[Dict[str, Any]],
                     material_thickness: float, thickness_confidence: Any,
                     canvas_width: float, canvas_height: float, filename: str) -> List[ValidationResult]:
        results = []
        for layer in layers:
            if layer.get("is_output_yes") and layer.get("total_cut_length_mm", 0.0) > 0.0:
                results.extend(self.validate_h2(layer, material_thickness, thickness_confidence))
        results.extend(self.validate_sequence(layers, elements))
        results.extend(self.validate_fixation(canvas_width, canvas_height))
        return results
