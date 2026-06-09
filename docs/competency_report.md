# Competency Report — Outpost2026 Portfolio Analysis

**Generated:** 2026-06-09
**Subject:** Ondřej Soušek (outpost2026)
**Scope:** 7 GitHub repositories, 6 months of development (leden–červen 2026)

---

## 1. Portfolio Overview

### 1.1 Repo Taxonomy

| Repo | Purpose | Maturity | Size | Tech Stack | Branches |
|------|---------|----------|------|------------|----------|
| **vcut-parser** | VCF binární parser pro Ruida/VCutWorks CNC | Production | 124 files | Python, Flask, Docker, GCP | 1 |
| **CNC_2_LLM** | DXF → ML pipeline, CNC automation, ERP integrace | Active dev | 401 files | Python, JSON, CSV, GCP | 5 |
| **cad2llm** | SketchUp → deterministic JSON pro LLM | MVP | 6 files | Python, JSON | 1 |
| **Kazuistiky-LLM-sprint** | Learning methodology, 45-day GCP sprint | Documentation | 10 files | Python, Markdown, GCP | 3 |
| **Outpost-security-perimeter** | IoT perimeter security (ESP32/8266) | Prototype | 2 files | ESP32, Arduino, IoT | 2 |
| **RAG-indexer** | Unstructured data → vector DB preprocessing | MVP | 3 files | Python, RAG | 1 |
| **outpost2026** | Profile / whitepaper | Static | 1 file | Markdown | 1 |

### 1.2 Portfolio Gravity

```
                    CNC/VCF PARSING (CORE IP)
                    ┌──────────────────────┐
                    │   vcut-parser (v20)  │ ← Unikátní, žádný konkurent
                    │   CNC_2_LLM (v2.4)   │ ← DXF→ML pipeline
                    └──────────┬───────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
     CAD→LLM Bridge     Learning Pipeline     Infrastructure
     ┌──────────┐     ┌────────────────┐    ┌────────────────┐
     │ cad2llm  │     │ Kazuistiky-    │    │ Outpost-       │
     │ (SketchUp│     │ LLM-sprint     │    │ security-      │
     │  →JSON)  │     │ (metodologie)  │    │ perimeter (IoT)│
     └──────────┘     │ RAG-indexer    │    └────────────────┘
                      └────────────────┘
```

---

## 2. Technical Competency Matrix

### 2.1 Skills by Domain

| Domain | Skills | Evidence | Proficiency |
|--------|--------|----------|-------------|
| **Reverse Engineering** | Binární analýza, hex diff, IEEE 754 dekódování, magické signatury | vcut-parser: hex_diff.py, vcf_pair_analysis.txt, 6-fázový RE proces | Expert |
| **Binary Format Parsing** | C++ struct serializace, little-endian, Windows-1250 | vcut-parser: VCF_COMPILER_KNOWLEDGE_BASE, layer mapping | Expert |
| **Python Development** | Flask API, CLI tools, data pipelines | ~50+ .py files across all repos | Advanced |
| **GCP / Cloud** | Cloud Run, Docker, deployment scripts, CI | vcut-parser: deploy/, GCP_Deploy/; Kazuistiky: GCP branch | Advanced |
| **Machine Learning Pipeline** | Feature extraction, SNR optimalizace, vektorizace | CNC_2_LLM: feature branches, ml_vector.csv | Intermediate |
| **IoT / Embedded** | ESP32/8266, PIR, Doppler radar, weight sensor | Outpost-security-perimeter | Intermediate |
| **Web App Development** | Flask, REST API, JSON config | vcut-parser: app.py, app_config.json | Intermediate |
| **RAG / Vector DB** | Semantická klasifikace, chunking, embedding | RAG-indexer; CNC_2_LLM: semantic_embedding branch | Intermediate |
| **Testing** | Pytest, determinism tests, golden master tests | CNC_2_LLM: tests/ (test_determinism.py, test_golden_master.py) | Advanced |
| **Documentation** | Methodologie, handoff JSONy, epistemické playbooky | 30+ .md, 20+ .json dokumentačních souborů | Expert |
| **ERP Integration** | Odoo, Google Sheets API Apps Script | CNC_2_LLM: B2B analýzy; vcut-parser: .gs scripts | Intermediate |
| **DevOps** | Docker, .gcloudignore, deployment automation | vcut-parser: deploy.ps1, Dockerfile | Intermediate |

### 2.2 Technology Stack Heatmap

```
Python          ████████████████████████████████ 100% (dominant)
JSON            ████████████████████████████      90%
Markdown        ████████████████████████████      90%
Docker          ████████████                      40%
GCP             ████████████                      40%
Flask           █████████                         30%
Google Apps Sc. ██████                            20%
ESP32/Arduino   ████                              10%
GitHub Actions  ██                                 5% (not yet used)
```

### 2.3 Development Velocity

| Metrik | Hodnota |
|--------|---------|
| Total files across portfolio | ~560 |
| Total lines of code (estimated) | ~40,000+ |
| Python scripts | ~50+ |
| JSON artifacts | ~40+ |
| Documentation files | ~60+ |
| Branches (active feature work) | 7 (CNC_2_LLM) |
| Timeframe | ~6 months (leden–červen 2026) |
| Velocity | ~6,500 lines/month, ~90 files/month |
| Learning curve | From 0 Python → production GCP deploy in 45 days |

---

## 3. Diff Analysis — Portfolio Evolution

### 3.1 Chronological Development

```
leden 2026    Tacit knowledge acquisition (CNC dílna, stínování)
únor 2026     Synthetic ground truth (testovací VCF, hex analýza)
březen 2026   GitHub účet založen, RAG-indexer, Kazuistiky start
duben 2026    Parser v1–v9, hex_diff, párová analýza
květen 2026   Parser v10–v18.3, layer mapping, edge completion
červen 2026   GCP deploy v1.6–v1.7, CNC_2_LLM pipeline, mirror
```

### 3.2 Cross-Repo Thematic Analysis

| Téma | Dotčené repy | Síla vazby |
|------|-------------|-----------|
| **CNC Manufacturing Data** | vcut-parser, CNC_2_LLM | 🔗🔗🔗 (core) |
| **LLM Integration** | cad2llm, Kazuistiky, CNC_2_LLM | 🔗🔗 (supporting) |
| **Deterministic Data Pipelines** | cad2llm, CNC_2_LLM, RAG-indexer | 🔗🔗🔗 (core) |
| **Self-Learning Methodology** | Kazuistiky, outpost2026 | 🔗🔗 (meta) |
| **IoT / Off-Grid** | Outpost-security-perimeter | 🔗 (peripheral) |
| **Cloud Deployment** | vcut-parser, Kazuistiky | 🔗🔗 (supporting) |

### 3.3 Skill Evolution Trajectory

```
                    Reverse Engineering
                    ████████████████████ →
                    Python Development
                    ████████████████████ →
                    Documentation / Knowledge Mgt
                    ████████████████████ →
                    GCP / Cloud
                    ████████████████░░░ →
                    ML / Data Pipeline
                    ██████████░░░░░░░░░ →
                    Testing / QA
                    ██████████████░░░░░ →
                    IoT / Embedded
                    ████░░░░░░░░░░░░░░░ →
                    Web App (Flask)
                    ██████████████░░░░░ →
                    DevOps / Docker
                    ██████████░░░░░░░░░ →
                    
                    leden   únor   březen  duben  květen  červen
```

---

## 4. Market Positioning

### 4.1 Competitive Landscape — VCF Parser

| Aspekt | outpost2026 (vcut-parser) | LightBurn | MeerK40t | kkaempf/ruida |
|--------|--------------------------|-----------|----------|---------------|
| **Formát** | .VCF (VCutWorks) | .rd (Ruida) | .rd (Ruida) | .rd (Ruida) |
| **Typ** | Standalone parser | Full aplikace | Full aplikace | Decoder tool |
| **Licence** | Proprietary | Commercial ($200) | MIT | MIT |
| **API** | Flask REST API | None | None | None |
| **ERP Ready** | ✅ JSON výstup | ❌ | ❌ | ❌ |
| **ML Pipeline** | ✅ ML vektory | ❌ | ❌ | ❌ |
| **GCP Deploy** | ✅ | ❌ | ❌ | ❌ |
| **Layer Mapping** | ✅ Bit-shift | ✅ | Limited | ❌ |
| **Edge Completion** | ✅ | ❌ | ❌ | ❌ |
| **Physical Models** | ✅ (vakuum, posun) | ❌ | ❌ | ❌ |
| **Stars** | 0 (new) | ~10,000+ | 397 | 43 |

### 4.2 Unique Value Proposition

```
┌─────────────────────────────────────────────────────────────────┐
│              outpost2026 UNIQUE ADVANTAGES                      │
├─────────────────────────────────────────────────────────────────┤
│  1. Jediný známý standalone parser pro .VCF formát             │
│  2. První RE dokumentace formátu (handoff V16)                 │
│  3. Edge Completion Engine (žádný konkurent)                   │
│  4. Fyzikální modely (vakuový přítlak, posun)                 │
│  5. ERP-ready JSON výstup (Odoo, Sheets integrace)             │
│  6. ML pipeline vektory (SNR, trimming, embedding)             │
│  7. GCP Cloud-native (Docker, Flask, Cloud Run)                │
│  8. Knowledge Base engine (technologická pravidla)             │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Market Gap Analysis

| Gap on market | outpost2026 solution | Revenue potential |
|---------------|---------------------|-------------------|
| No standalone .VCF parser | vcut-parser (v20) | Medium (licensing) |
| No CAM-to-ERP bridge | CNC_2_LLM pipeline | High (SaaS) |
| No ML-ready manufacturing data | DXF→ML vectors | Medium (data product) |
| No deterministic CAD→LLM bridge | cad2llm | Low (enabler) |
| No Ruida API ecosystem | Flask API + KB engine | High (API SaaS) |

### 4.4 Total Addressable Market (TAM)

| Segment | Size | outpost2026 relevance |
|---------|------|----------------------|
| CNC laser shops (Ruida) | ~500,000+ machines | **Primary** — VCF parser need |
| LightBurn users | ~100,000+ paid | Secondary — plugin/integration |
| ERP/MRP users in manufacturing | ~50,000+ companies | Tertiary — data pipeline |
| CAM software market | $3–5B globally | Niche entry point |

---

## 5. B2B Pivot Readiness Assessment

### 5.1 Strengths

- **Unique IP**: VCF parser nemá konkurenci — first-mover advantage
- **Production-ready**: Docker + GCP deploy (v1.7)
- **Documentation**: Kompletní RE dokumentace, handoffy, knowledge base
- **Testing**: Test suite (determinism, golden master, smoke tests)
- **Domain expertise**: CNC provoz, CAM parametry, materiály (PET felt 12/24 mm)

### 5.2 Gaps

- **No GitHub Actions / CI/CD**: Automatizace build/test pipeline chybí
- **No license**: Všechny repy bez licence (kromě cad2llm MIT, security Apache)
- **No pricing model**: Není definovaná cenová struktura pro produkt
- **No user base**: 0 stars, 0 forks, 0 followers
- **No legal entity**: s.r.o. není založeno
- **No marketing**: README existuje, ale chybí landing page, dokumentace API

### 5.3 Recommended B2B Positioning

```
Positioning Statement:
"VCF-to-ERP data pipeline pro laserové CNC dílny — 
extrahujte výrobní data z CAM souborů automaticky, 
bez manuálního přepisování do ERP."

Target segments (priority):
1. ⭐ SMB laserové dílny s Ruida/VCutWorks (CZ/SK/DE)
2. ⭐ Výrobci nábytku a signage (PET felt, akryl, dřevo)
3.  ⭐ Integrátoři ERP (Odoo, SAP B1) hledající CAM konektor

Pricing model (recommended):
- SaaS: €50–200/měsíc (dle objemu souborů)
- On-premise: €1,000–5,000 licence (jednorázově)
- API: €0.10–0.50/parsovaný soubor
```

---

## 6. Competency Scorecard

| Dimenze | Skóre (1–10) | Komentář |
|---------|-------------|----------|
| **Technical Depth** | 9/10 | Reverzní inženýrství na úrovni C++ struct serializace |
| **Portfolio Coherence** | 7/10 | Silné CNC jádro, IoT a RAG jsou odbočky |
| **Code Quality** | 7/10 | Testy existují, chybí CI/CD, linting, type hints |
| **Documentation** | 9/10 | Výjimečná — handoffy, metodologie, epistemické playbooky |
| **DevOps Maturity** | 5/10 | Docker je, CI/CD chybí, monitoring chybí |
| **Product Readiness** | 4/10 | Technicky hotovo, productově ne (UI, UX, onboarding) |
| **Market Position** | 8/10 | Unikátní pozice, žádný známý konkurent |
| **Business Readiness** | 2/10 | Chybí entita, licence, pricing, marketing |
| **Learning Velocity** | 10/10 | 0 → GCP production za 45 dní (Kazuistiky) |
| **System Thinking** | 9/10 | CNC → parser → ML → ERP → GCP — celý stack |

**Overall Competency Score: 7.0/10** — Technicky silný, business slabý.

---

## 7. Strategic Recommendations

### Immediate (30 dní)
1. ✅ Založit s.r.o. — oddělit osobní majetek od IP
2. ✅ Přidat licenci (MIT / Apache 2.0) ke všem repům
3. ✅ Nastavit GitHub Actions (CI: pytest na každý push)
4. ✅ Definovat pricing model pro SaaS + on-premise
5. ✅ Vytvořit landing page (GitHub Pages nebo simple site)

### Short-term (90 dní)
1. 🔄 CNC_2_LLM: sloučit feature branch do main
2. 🔄 vcut-parser: publikovat API dokumentaci (Swagger/OpenAPI)
3. 🔄 Vytvořit demo video / interaktivní demo
4. 🔄 Oslovit 10 laserových dílen v CZ/SK jako beta testery
5. 🔄 Vytvořit Odoo module pro přímou integraci

### Long-term (180+ dní)
1. 🎯 Scale: z CLI nástroje na SaaS platformu
2. 🎯 Expand: podpora dalších CAM formátů (LaserGRBL, LightBurn .lbrn2)
3. 🎯 ML: prediktivní model pro optimalizaci nesting a toolpath
4. 🎯 Community: open-source core + commercial extensions

---

*Report generated from GitHub API mirror (7 repos, 401+ tree entries analyzed).*
*Market data from web research + competitive analysis.*
