import pytest
from pathlib import Path
from vcf_parser_v20 import RuidaVcfEngineV20

DEMO_FILES = [
    "1ks.VCF",
    "Ofset_3x.VCF",
    "fluenz_l.VCF",
    "vyrobni_data_pernerka_service_for_office_dark_knight_12mm.VCF",
]

REQUIRED_TOP_KEYS = [
    "filename", "file_hash", "file_size_bytes", "extracted_metadata",
    "elements_parsed", "elements", "layers", "canvas_width_mm", "canvas_height_mm",
]


@pytest.mark.parametrize("fname", DEMO_FILES)
def test_parse_demo_file(demo_dir, fname):
    path = Path(demo_dir) / fname
    assert path.exists(), f"Demo file not found: {path}"
    raw = path.read_bytes()
    engine = RuidaVcfEngineV20(raw, fname)
    pd = engine.parsed_data
    assert pd is not None
    for key in REQUIRED_TOP_KEYS:
        assert key in pd, f"Missing key '{key}' in parsed_data for {fname}"
    assert pd["filename"] == fname
    assert pd["file_size_bytes"] > 0


def test_parse_returns_different_hashes(demo_dir):
    hashes = set()
    for fname in DEMO_FILES:
        path = Path(demo_dir) / fname
        raw = path.read_bytes()
        engine = RuidaVcfEngineV20(raw, fname)
        hashes.add(engine.parsed_data["file_hash"])
    assert len(hashes) == len(DEMO_FILES), "Each file should have a unique hash"


def test_parse_no_exceptions(demo_dir):
    for fname in DEMO_FILES:
        path = Path(demo_dir) / fname
        raw = path.read_bytes()
        engine = RuidaVcfEngineV20(raw, fname)
        assert isinstance(engine.parsed_data, dict)
