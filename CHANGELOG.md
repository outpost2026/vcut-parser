# Changelog — VCF Parser (Ruida/VCutWorks)

## Phase 0 — Tacit Knowledge Acquisition (leden–únor 2026)
- 9 dní stínování hlavního technologa (Karel Pruška) ve firmě Moodpasta (Wynwood s.r.o.)
- Ruční zápisky: kalibrace nuly, oscilační frekvence, barevná nomenklatura vrstev, nesting pravidla
- Digitalizace deníků: `denik_day_01.txt`, `denik_day_03.txt`, `denik_day_05-06-07-08.txt`

## Phase 1 — Synthetic Ground Truth (únor–březen 2026)
- Vytvoření testovacích VCF souborů v trial VcutWorks: `rectangle_01.vcf`, `circle_01.vcf`, `diamond_01.vcf`
- Diferenciální analýza párů (`vcf_pair_analysis.txt`)

## Phase 2 — Hex Analysis & Reverse Engineering (březen–duben 2026)
- `hex_diff.py`, `hex_diff_v2.py` — hex dump a diff testovacích souborů
- Identifikace magických signatur: `RDVCUTFILEVER1.0.012/013`
- Objev IEEE 754 double float (souřadnice) a kódování Windows-1250 (metadata)
- Zjištění: formát je binární serializace C++ struktur (little-endian), ne šifrovaný

## Phase 3 — Initial Parser v1–v9 (duben 2026)
- **v1** — První extrakce metadat (jméno DXF, tagy, fonty)
- **v2–v8** — Iterativní zpřesňování parametrů vrstev (rychlost, nástroj, směr řezu, přesahy, Width Comp, Tool Feeding)
- **v9** — Empirický odhad času z instruction_count. Geometrie zatím neextrahována.
- Artefakty: `ruida_parser_v9.py`, `vcf_analysis_report_v9.md`, `vcf_deep_analysis_v9_final.json`

## Phase 4 — Precision Improvement v10–v13 (květen 2026)
- **v10** — Exaktní dekódování geometrie z IEEE 754 float, výpočet délky dráhy
- **v11** — Mapování elementů: Line, Polygon, Circle
- **v12** — Edge Completion Engine (rekonstrukce chybějících CAM hran)
- **v13** — Grouping Mode Fix (sloučené geometrie v GUI)

## Phase 5 — Layer Mapping & Stabilization v14–v16 (květen 2026)
- **v14** — Perfect Layer Mapping (color-to-layer bitovým posunem)
- **v15** — Circle Regression Fix, robustní cutter_type_id maskování
- **v16** — Kompletní strojově čitelná dokumentace formátu: `RUIDA_VCF_PARSER_HANDOFF_V16.json`

## Phase 6 — Advanced Physical Models v17–v18 (květen–červen 2026)
- **v17** — Predikce rizika posunu dílů (malá plocha → nedostatečný vakuový přítlak)
- **v17.1–v17.8** — Iterativní vylepšení: detekce problémového pořadí řezu, technologické poznámky
- **v18.0–v18.3** — Finální standalone parser s plnou geometrií, layer mappingem, edge completion
- **v18.3** — Poslední verze standalone parseru (90 KB)

## Phase 7 — Cloud Deployment & Web App (červen 2026)
- **v20 (GCP)** — Migrace parseru do cloudové architektury
  - Flask web app (`app.py`) s REST API
  - Knowledge Base engine (`Knowledge_base/`) pro technologická pravidla
  - Docker kontejner pro GCP Cloud Run
  - Skript `deploy.ps1` pro automatizované nasazení
- **v1.6 → v1.7** — Iterace: app_config.json, machine_profile.json, vylepšený parser
- Google Apps Scripty (`vcf_parser_integrace_v1–v3.gs`) pro integraci s Google Sheets

## Aktuální stav
- **src/vcf_parser_v20.py** — Hlavní parser (63 KB)
- **src/ruida_parser_v18.3.py** — Standalone varianta (90 KB)
- **src/app.py** — Flask web app
- **deploy/** — Docker + GCP deployment
- **docs/** — Kompletní RE dokumentace, handoff JSONy, deníky
