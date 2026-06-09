---
title: Master_Context_Dokumentace_RE_VCF
source_url: local_tree://C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Data_moodpasta\Vcf_vyvoj\Dokumentace_RE_VCF
scraped_at: 2026-06-09T11:54:38.239352
topic: code_context_map
data_type: markdown
---

# Zdrojový strom: Dokumentace_RE_VCF

```text
├── analyza_a_dekodovani_proprietarniho_formatu_vcf.md
├── context_indexer_v3.py
├── Dekonstrukce_automatizace_CAM_formatu_VCF.md
├── handoff_0.6.1.json
├── index_Dokumentace_RE_VCF.md
├── moodpasta_vcf_re_handoff_final.json
├── RUIDA_VCF_DEV_HISTORY_V2.0.json
├── RUIDA_VCF_PARSER_HANDOFF_V16.json
├── summary_proprietarni_format_vcf.json
├── VCF_COMPILER_KNOWLEDGE_BASE_V1.0.json
├── vcf_deep_parser_handoff.json
├── VCF_LAYER_PARAMETERS_RE_V1.0.json
├── vcf_pair_analysis.txt
└── vcf_parser_v10.json

```

---

## 📄 `analyza_a_dekodovani_proprietarniho_formatu_vcf.md`

```md
# 🔬 Výzkumný report: Analýza a dekódování proprietárního formátu .VCF

**Datum:** Březen 2024
**Kontext:** Reverzní inženýrství CAM formátu `.VCF` (Shenzhen Ruida Technology / VCutWorks) pro účely vývoje prediktivního modelu a automatizace ERP.
**Status:** Dekódováno a algoritmizováno.

---

## 1. Úvodní premisa a "Manifest nedotknutelnosti"

Cílem výzkumu bylo porozumět proprietární struktuře hexadecimální binárky souborů s příponou `.VCF`, do kterých program VCutWorks překládá vektorová data (DXF) pro odeslání do řídící jednotky stroje Ruida. Porozumění struktuře je nezbytné pro vytvoření skriptu, který dokáže automatizovaně vytěžit klíčové parametry řezu (čas, složitost, rychlosti) bez spuštění samotného CAM softwaru a poslat je do databáze ERP.

Průběh výzkumu zásadně ovlivnilo "odborné poselství" dosavadního operátora (Karel), který reprezentuje expertní, tacitní rovinu know-how ve výrobě. Jeho postoj k pokusům o dekódování dat byl rezolutní a zamítavý.

**Zkrácený manifest operát...
```

## 📄 `context_indexer_v3.py`

```py
def strip_html_tags(...):
def generate_tree(...):
def extract_openxml_text(...):
def is_text_file_heuristic(...):
def get_file_content(...):
def format_snippet(...):
def main(...):
```

## 📄 `Dekonstrukce_automatizace_CAM_formatu_VCF.md`

```md
# Report: Dekonstrukce a automatizace CAM formátu .VCF

**Projekt:** Reverzní inženýrství CAM formátu `.VCF` (Shenzhen Ruida Technology)
**Status:** V9 (Pokročilá analytika fyzikálních parametrů vrstev)
**Datum:** 17. 5. 2026

## 1. Výchozí bod (Mýtus)
Výchozí premisou byla nedotknutelnost proprietárního binárního formátu `.VCF`, vnímaného jako neřešitelná "čínská černá skříňka". Praxe potvrdila, že jde o deterministickou serializaci datových struktur C++, nikoliv o šifrovaný formát.

## 2. Dosažené milníky (Iterace V1 - V9)
- **V1-V4 (Základní dekódování):** Identifikace IEEE 754 struktur, zjištění kódování Windows-1250, eliminace balastních dat ("hřbitov palet").
- **V5-V8 (Algoritmizace):** Úspěšné vytvoření parseru `RuidaVcfDeepParser`, který extrahuje exaktní rychlosti (mm/s) aktivních vrstev a provádí první odhady času (shoda 100 % s GUI).
- **V9 (Fyzikální modely):** Propojení hexadecimálních dat s reálnými parametry řezu (screenshoty "Layer Parameter"). Parser nyní extrahuje:
 ...
```

## 📄 `handoff_0.6.1.json`

```json
{
  "handoff_metadata": {
    "version": "2.0",
    "timestamp": "2026-05-31T23:00:00",
    "author": "opencode (CAM & ML LLM Agent)",
    "target_version_draft": "v0.7.0",
    "status": "GROUND_TRUTH_FOR_NEXT_ITERATION",
    "description": "Analýza selhání v0.6.1, objev duplicitního ukládání parametrů vrstev (rychlost, extenze) ve dvou oblastech VCF a návrh systematického mapování offsetů pro bezpečné parametrické generování. v0.6.2 (globální search & replace) byl zamítnut jako dead end."
  },

  "current_state": {
    "active_compiler_version": "v0.6.1",
    "symptoms": "Syntetický VCF stále nevykazuje vlastnosti vrstev v GUI VCutWorks (---) a chybí Cutting Properties, přestože geometrie se zobrazuje správně.",
    "root_cause_identified": "Formát VCF ukládá parametry vrstvy (rychlost, extenze, výkon, …) minimálně dvakrát – v hlavičce souboru a v bloku těsně před geometrií. Kompilátor v0.6.1 aktualizuje pouze jednu kopii (blok před geometrií nalezený dynamickým vyhledávačem), čímž vz...
```

## 📄 `index_Dokumentace_RE_VCF.md`

```md
[Prázdný nebo nečitelný obsah]
```

## 📄 `moodpasta_vcf_re_handoff_final.json`

```json
{
    "handoff_id": "MOODPASTA_VCF_RE_FINAL_SYNTHESIS",
    "version": "3.0",
    "status": "REVERSE_ENGINEERING_COMPLETED_PENDING_CALIBRATION",
    "last_updated": "2026-05-17T12:00:00+02:00",
    "author_role": "Systems Architect / Reverse Engineer",
    "target_audience": "LLM Context / ERP Integration Developers",
    "semantic_summary": {
        "project_goal": "Reverzní inženýrství proprietárního formátu .VCF (Ruida / VCutWorks) pro automatizaci výrobního workflow a predikci času CNC řezu.",
        "methodology": "Iterativní analýza binárního kódu + fyzická validace z výroby (transfer learning z CNC Waterjet).",
        "key_breakthroughs": [
            "Dekódování textových vrstev (CERNA, ZLUTA) a absolutních cest k DXF souborům díky aplikaci kódování Windows-1250 namísto prostého ASCII.",
            "Objevení proxy-proměnné pro složitost: Extrakce X/Y/U souřadnic jako 64-bit IEEE 754 (Double Precision) floatů. Počet těchto floatů (instruction_count) přímo koreluje s časem ř...
```

## 📄 `RUIDA_VCF_DEV_HISTORY_V2.0.json`

```json
{
  "handoff_id": "RUIDA_VCF_DEV_HISTORY_V2.0",
  "version": "2.0",
  "created": "2026-05-24T12:00:00+02:00",
  "title": "Kronika vývoje parseru proprietárního CAM formátu .VCF – od V1 po V15",
  "project_phase": "V15 – Stabilizovaný parser s barevným mapováním a geometrickou rekonstrukcí",
  
  "executive_summary": {
    "problem_statement": "Firma Moodpasta potřebovala automatizovat predikci CNC časů pro ERP. Formát .VCF (Ruida/VCutWorks) byl považován za nečitelnou 'čínskou černou skříňku'.",
    "outcome": "Během 72 hodin prvního týdne vznikl funkční parser (V1–V9). Následné ground truth validace odhalily zásadní chyby v interpretaci délky dráhy a přiřazení vrstev. Tyto chyby vedly k iteracím V10–V15, které zavedly skutečnou rekonstrukci geometrie, edge completion, barevné mapování a opravu regrese kružnic. Aktuální parser V15 dosahuje přesnosti extrakce délek ±2–5 % na testovacích souborech.",
    "key_insight": "Formát neukládá předpočítanou délku, ale sekvenci bodů (Bézierovy kř...
```

## 📄 `RUIDA_VCF_PARSER_HANDOFF_V16.json`

```json
{
  "handoff_id": "RUIDA_VCF_PARSER_HANDOFF_V16",
  "version": "16.0",
  "created": "2026-05-24T22:00:00+02:00",
  "title": "Kompletní strojově čitelná dokumentace reverzního inženýrství formátu Ruida .VCF",
  "purpose": "Ground truth pro LLM asistovaný vývoj, další iterace (V17+) a komercializaci.",
  "project_context": {
    "origin": "Moodpasta/Wynnwood s.r.o. – CNC výroba PET panelů ECHOBLOCK",
    "reverse_engineer": "Ondřej (SAI profil)",
    "timeframe": "12. – 24. 5. 2026 (14 dní)",
    "total_effort_hours": "~80–100 hodin",
    "unique_value": "První a jediný veřejně známý plně funkční parser formátu .VCF; žádná konkurence."
  },
  "binary_format_specification": {
    "file_extension": ".VCF (případně .vf)",
    "encoding": "Windows-1250",
    "magic_signature": {
      "full_8bytes": "0x01 0x00 0x01 0x00 0x00 0xFF 0xFF 0xFF",
      "abbreviated_form": "0x01 0x00 0x01 0x00 0x00 0xFF 0xFF 0xFF? (some variants have leading 0x00)",
      "detection_note": "Hledat tuto signaturu p...
```

## 📄 `summary_proprietarni_format_vcf.json`

```json
{
  "document_title": "Proprietární formát .VCF — Kompletní technická dokumentace a status projektu (květen 2026)",
  "version": "V16.1+",
  "last_updated": "2026-05-25",
  "author": "Ondřej",
  "format": {
    "name": ".VCF",
    "full_name": "Ruida VCut File",
    "vendor": "Shenzhen Ruida Technology",
    "software": "VCutWorks",
    "type": "Proprietární binární serializace (C/C++)",
    "endianness": "Little-endian",
    "encoding": "Windows-1250 (textová metadata)"
  },
  "structure": {
    "header": "ASCII signatura RDVCUTFILEVER1.0.xxx + metadata",
    "palette_graveyard": "20 výchozích systémových palet (balast)",
    "geometry_payload": "IEEE 754 double souřadnice, 74B segmenty (Line/Polyline/Polygon)",
    "layer_mapping": "geom_color == (layer_color << 8)",
    "active_layers_section": "Koncová část souboru — pouze použité vrstvy + technologické parametry",
    "export_flag": "32-bit int (Output = Yes/No)"
  },
  "capabilities": {
    "extracted_data": [
      "Názvy vrstev...
```

## 📄 `VCF_COMPILER_KNOWLEDGE_BASE_V1.0.json`

```json
{
  "handoff_id": "VCF_COMPILER_KNOWLEDGE_BASE_V1.0",
  "title": "Znalostní korpus pro vývoj kompilátoru syntetických .VCF souborů (Ruida VCutWorks)",
  "version": "1.0",
  "created": "2026-05-31",
  "source_artifacts": [
    "summary_proprietarni_format_vcf.json",
    "RUIDA_VCF_PARSER_HANDOFF_V16.json",
    "RUIDA_VCF_DEV_HISTORY_V2.0.json",
    "vcf_deep_parser_handoff.json",
    "vcf_pair_analysis.txt",
    "vcf_parser_v10.json",
    "Dekonstrukce_automatizace_CAM_formatu_VCF.md",
    "analyza_a_dekodovani_proprietarniho_formatu_vcf.md",
    "moodpasta_vcf_re_handoff_final.json"
  ],
  "compiler_goal": "Generovat binární .VCF soubor (verze RDVCUTFILEVER1.0.013) z raw DXF geometrie a uživatelsky definovaných technologických parametrů (rychlosti, nástroje, přesahy, barvy vrstev).",

  "format_philosophy": {
    "summary": ".VCF je binární serializace C++ struktur s little-endian uspořádáním, IEEE 754 double pro souřadnice a Windows-1250 pro textová metadata. Není komprimovaný ani šif...
```

## 📄 `vcf_deep_parser_handoff.json`

```json
{
    "project_name": "VCutWorks (.VCF) Reverse Engineering & Parser",
    "last_updated": "2026-05-23",
    "goal": "Vytvořit přesný parser proprietárního formátu .vcf (VCutWorks CAM) pro extrakci vrstev a geometrie k výpočtu ERP obráběcích časů CNC.",
    "current_version": "V15.0",
    "key_achievements": [
        "Plné dešifrování hex struktur pro rychlost a nástroje vrstev (V9).",
        "Získání specifických parametrů pro V-slot nástroj (směr, šířka a přesahy) (V9).",
        "Nahrazení chybného čtení délky z float bounding boxu za matematickou rekonstrukci obrysu (V11).",
        "Zavedení 'Edge Completion Engine' nahrazujícího chybějící CAM hrany pro CNC nulu (V12).",
        "Pochopení sloučených geometrií (vícenásobné 74bajtové segmentové bloky pod jedním Polygonem s type_id == 1) (V14).",
        "Úspěšná realizace barevného mapování (Color-to-Layer mapping) drah do příslušných vrstev pomocí bitového posunu (V14).",
        "Oprava kritické regrese výpočtu kružnic (V15).",...
```

## 📄 `VCF_LAYER_PARAMETERS_RE_V1.0.json`

```json
{
  "handoff_id": "VCF_LAYER_PARAMETERS_RE_V1.0",
  "title": "Reverzní inženýrství parametrů vrstev, řezných vlastností a barevné nomenklatury formátu .VCF (Ruida VCutWorks)",
  "version": "1.0",
  "created": "2026-05-31",
  "scope": "Pouze sekce aktivních vrstev, technologické parametry, cutter_type, barvy, export flag. Geometrie není zahrnuta.",
  "source_artifacts": [
    "summary_proprietarni_format_vcf.json",
    "RUIDA_VCF_PARSER_HANDOFF_V16.json",
    "RUIDA_VCF_DEV_HISTORY_V2.0.json",
    "vcf_deep_parser_handoff.json"
  ],

  "layer_section_location": {
    "description": "Aktivní vrstvy jsou uloženy až na konci souboru, za všemi geometrickými elementy. Typicky posledních 200–2000 bajtů.",
    "detection_signature": "Každá vrstva začíná signature 0x01 0x00 0x00 0x00 (4 bajty) bezprostředně před rychlostí.",
    "compiler_notes": "Při generování syntetického .VCF umístit tuto sekci jako poslední část souboru."
  },

  "layer_block_structure": {
    "overview": "Každá aktivní vr...
```

## 📄 `vcf_pair_analysis.txt`

```txt
VCF pair analysis for parser RE
generated from analyze_vcf_pairs.py

========================================================================
PAIR: rectangle 1 vs 2 squares
  rectangle_01.vcf: 157781 bytes (0x26855)
  rectangle_02.vcf: 158318 bytes (0x26A6E)
  delta: 537 bytes (0x219)
  expected delta if +N elements at 575B: N*575
  element_count @ 0x26633: 1 vs 2
  elem sig count: 1 vs 2
  diff regions: 12
    0x00026633-0x00026634 len=1 (0x1)
      f1: 01
      f2: 02
    0x00026675-0x0002667A len=5 (0x5)
      f1: 00 00 40 8f 40
      f2: 80 10 75 bf be
    0x00026688-0x00026689 len=1 (0x1)
      f1: 9f
      f2: 8f
    0x000266C2-0x000266C3 len=1 (0x1)
      f1: 9f
      f2: 8f
    0x000266D2-0x000266D3 len=1 (0x1)
      f1: 9f
      f2: 8f
    0x0002670C-0x0002670D len=1 (0x1)
      f1: 9f
      f2: 8f
    0x00026719-0x0002671E len=5 (0x5)
      f1: 00 00 40 8f 40
      f2: 80 10 75 bf be
    0x00026753-0x00026758 len=5 (0x5)
      f1: 00 00 40 8f 40
      f2: 80 10 75 bf be
    0...
```

## 📄 `vcf_parser_v10.json`

```json
{
  "handoff_id": "VCF_PARSER_V10_FINAL",
  "version": "1.0",
  "created": "2026-05-17T15:30:00+02:00",
  "status": "V9 dokončena, V10 připravena k implementaci",
  "project": "Reverzní inženýrství a finální parser proprietárního CAM formátu .VCF (Shenzhen Ruida Technology / VCutWorks) pro CNC oscilační nůž",
  "objectives": {
    "overall": "Vytvořit parser, který z .VCF souboru extrahuje veškeré technologické parametry a exaktně spočítá strojní čas na základě dekódované geometrie.",
    "current_state": "Parser V9 extrahuje: metadata (jméno DXF, uživatelské tagy, fonty), parametry vrstev (rychlost, typ nástroje, směr řezu, přesahy, V-slot Width Compensation, Tool feeding H1/H2). Predikce času pracuje s empirickým odhadem délky dráhy z počtu instrukcí (instruction_count) a průměrnou rychlostí. Přesnost je orientační, vhodná pro hrubé plánování.",
    "v10_goal": "Dekódovat geometrická data (souřadnice) pro každou vrstvu, spočítat skutečnou délku dráhy (včetně přesahů) a z přesné rychl...
```

