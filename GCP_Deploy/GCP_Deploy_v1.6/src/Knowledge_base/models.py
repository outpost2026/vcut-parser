from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

class RuleClass(str, Enum):
    CLASS_A_PHYSICAL = "CLASS_A"
    CLASS_B_EMPIRICAL = "CLASS_B"
    CLASS_C_HEURISTIC = "CLASS_C"
    CLASS_D_HYPOTHESIS = "CLASS_D"

class ValidationStatus(str, Enum):
    ACCEPTED = "accepted"
    CONDITIONAL = "conditional"
    REJECTED = "rejected"
    UNKNOWN = "unknown"

class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class ThicknessConfidence(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"

@dataclass
class EpistemicMetadata:
    rule_id: str
    description: str
    source: str
    confidence: float
    validation_status: ValidationStatus = ValidationStatus.ACCEPTED
    rule_class: RuleClass = RuleClass.CLASS_B_EMPIRICAL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "description": self.description,
            "source": self.source,
            "confidence": self.confidence,
            "validation_status": self.validation_status.value,
            "rule_class": self.rule_class.value
        }

@dataclass
class H2Rule:
    metadata: EpistemicMetadata
    cutter_type_id: int
    material_thickness_mm: float
    ideal_h2_range: List[float]
    critical_h2_threshold: float

@dataclass
class SequenceRule:
    metadata: EpistemicMetadata
    check_nesting_hierarchy: bool = True
    must_cut_last_cutter_id: int = 1

@dataclass
class FixationRule:
    metadata: EpistemicMetadata
    min_area_m2_no_tape: float = 1.67
    critical_area_m2: float = 0.5
    tape_perimeter_coverage_pct: float = 80.0

@dataclass
class ValidationResult:
    rule_id: str
    rule_class: RuleClass
    severity: Severity
    code: str
    message: str
    confidence: float
    traceable_context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_class": self.rule_class.value,
            "severity": self.severity.value,
            "code": self.code,
            "message": self.message,
            "confidence": self.confidence,
            "traceable_context": self.traceable_context
        }
