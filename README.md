# VCut-Parser — Reverse Engineered Ruida VCF Parser

[![CI](https://github.com/outpost2026/vcut-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/outpost2026/vcut-parser/actions/workflows/ci.yml)

Parser a analyzátor proprietárního binárního formátu `.VCF` (Ruida/VCutWorks CNC plotry). Vznikl procesem reverzního inženýrství z testovacích souborů a systematické dokumentace CAM parametrů.

## Schopnosti

- Extrakce geometrie (Line, Polyline, Polygon, Circle) z IEEE 754 double float souřadnic
- Barevné mapování vrstev (color-to-layer bitovým posunem)
- Edge Completion Engine (rekonstrukce chybějících CAM hran pro CNC nulu)
- Predikce času řezu (±2–5 % na testovacích datech)
- Technologická varování: riziko posunu dílů, problémové pořadí řezu, vakuový přítlak
- Grouping Mode Fix pro sloučené geometrie
- Machine profile konfigurace pro různé CNC stroje

## Struktura

```
src/              — Hlavní parser (v20), standalone (v18.3), Flask app
scripts/          — Utility: hex_diff, analyze_vcf_pairs, json_to_md, Google Apps Scripts
docs/
  handoffs/       — JSON dokumentace formátu, RE handoffy
  reports/        — Analytické reporty jednotlivých verzí
  deniky/         — Digitalizované deníky z provozu CNC
deploy/           — Docker, .gcloudignore, deploy.ps1
data/
  synthetic/      — Vlastní testovací VCF soubory (rectangle)
  demo/           — Ukázková výrobní data
analysis/         — JSON výstupy analýz (< 2 MB)
```

## Deployment

```bash
cd deploy
docker build -t vcf-parser .
docker run -p 8080:8080 vcf-parser
```

## Formát .VCF

Proprietární binární serializace C++ struktur (little-endian):
- Magic: `RDVCUTFILEVER1.0.012` / `013`
- Geometrie: IEEE 754 double (X, Y) v 74B segmentech
- Metadata: Windows-1250
- Kompletní specifikace: `docs/handoffs/RUIDA_VCF_PARSER_HANDOFF_V16.json`

## Historie

Viz `CHANGELOG.md` — 6 fází vývoje od tacitních znalostí po cloud deployment.

## Licence

Všechna práva vyhrazena. Tento software je výsledkem nezávislého reverzního inženýrství.
