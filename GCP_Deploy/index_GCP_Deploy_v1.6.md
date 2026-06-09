---
title: Master_Context_GCP_Deploy_v1.6
source_url: local_tree://C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Data_moodpasta\Vcf_vyvoj\GCP_Deploy_v1.6
scraped_at: 2026-06-05T18:06:52.695077
topic: code_context_map
data_type: markdown
---

# Zdrojový strom: GCP_Deploy_v1.6

```text
├── src
│   ├── demo_data
│   │   ├── 1ks.VCF
│   │   ├── fluenz_l.VCF
│   │   └── vyrobni_data_pernerka_service_for_office_dark_knight_12mm.VCF
│   ├── Knowledge_base
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── models.py
│   │   └── rules.json
│   ├── app.py
│   └── vcf_parser_v20.py
├── context_indexer_v3.py
├── deploy.ps1
├── Dockerfile
├── index_GCP_Deploy_v1.6.md
├── KNOWLEDGE_BASE_DEPLOY_v1.6.md
└── requirements.txt

```

---

## 📄 `.dockerignore`

```
*.md
diff.txt
__pycache__/
*.pyc
.git/
readme_dev_v1.5.md
B2B_MEETING_BRIEF_v1.5.md

```

## 📄 `.gcloudignore`

```
*.md
diff.txt
__pycache__/
*.pyc
.git/
readme_dev_v1.5.md
B2B_MEETING_BRIEF_v1.5.md
.gcloudignore
.gitignore

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

## 📄 `deploy.ps1`

```ps1
# Moodpasta VCF Parser — Deploy Script v1.6
# ============================================
# TOTO JE PRVNI DEPLOY PRODUKTOVEHO SOFTWARU AUTORA V ZIVOTE.
# Spustit z PowerShellu jako Administrator.
#
# Predpoklady pred spustenim:
#   1. gcloud CLI nainstalovano + prihlaseno (gcloud auth login)
#   2. Docker Desktop nainstalovano a bezi
#   3. Projekt project-4ac30110-41b1-4783-a5d aktivni
#
# Region: europe-west1 (Belgie) — NEPOUZIVAT europe-west3!

$ErrorActionPreference = "Stop"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  MOODPASTA VCF PARSER — GCP CLOUD RUN DEPLOY" -ForegroundColor Cyan
Write-Host "  Verze: v1.6-demo | Datum: 2026-06-05" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$PROJECT_ID = "project-4ac30110-41b1-4783-a5d"
$PROJECT_NUMBER = "537446704644"
$REGION = "europe-west1"
$SERVICE_NAME = "vcf-parser-demo"
$IMAGE_NAME = "europe-west1-docker.pkg.dev/$PROJECT_ID/moodp...
```

## 📄 `Dockerfile`

```
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY vcf_parser_v20.py .
COPY Knowledge_base/ Knowledge_base/
COPY demo_data/ demo_data/

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

```

## 📄 `index_GCP_Deploy_v1.6.md`

```md
[Prázdný nebo nečitelný obsah]
```

## 📄 `KNOWLEDGE_BASE_DEPLOY_v1.6.md`

```md
# Moodpasta VCF Parser — GCP Deploy Knowledge Base
# ===================================================
# Autor: Ondrej Sousek
# Datum: 2026-06-05
# Udalost: PRVNI DEPLOY VYVINUTEHO SOFTWARU V ZIVOTE
#
# Epistemicky kontext pro budouciho autora:
# Toto je prvni nasazeni softwaru, ktery autor samostatne vyvinul,
# na verejnou cloudovou platformu za ucelem prezentace B2B zakaznikovi.
# Kazdy krok je popsan vcetne "proc" — nejen "jak".

## ARCHITEKTURA DEPLOYE

### Co se deje pri gcloud builds submit:
1. gcloud zabali zdrojovy kod (respektuje .gcloudignore)
2. Nahraje ho do Cloud Storage (docasny bucket)
3. Cloud Build spusti Docker build podle Dockerfile
4. Vysledny image pushne do Artifact Registry
5. Docasny bucket se smaze

### Co se deje pri gcloud run deploy:
1. Cloud Run vytahne image z Artifact Registry
2. Vytvori novou "revizi" (immutabilni verze sluzby)
3. Spusti kontejner s nastavenymi parametry (memory, CPU, min/max instances)
4. Priradi HTTPS URL ve formatu: {service}-{proje...
```

## 📄 `requirements.txt`

```txt
streamlit==1.38.0
matplotlib==3.8.0
pandas==2.2.0

```

## 📄 `src\app.py`

```py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vcf_parser_v20 import RuidaVcfEngineV20
import os

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Moodpasta Parser Demo")
    pwd = st.text_input("Přístupové heslo", type="password")
    if st.button("Přistoupit"):
        if pwd == "moodpasta-demo-2026":
            st.session_state.authenticated = True
            st.rerun...
```

## 📄 `src\vcf_parser_v20.py`

```py
class RuidaVcfEngineV20:
```

## 📄 `src\Knowledge_base\engine.py`

```py
class KnowledgeBaseEngine:
```

## 📄 `src\Knowledge_base\models.py`

```py
class RuleClass:
class ValidationStatus:
class Severity:
class ThicknessConfidence:
class EpistemicMetadata:
class H2Rule:
class SequenceRule:
class FixationRule:
class ValidationResult:
```

## 📄 `src\Knowledge_base\rules.json`

```json
{
  "h2_rules": [
    {
      "metadata": {
        "rule_id": "RULE_H2_VIBRATE_12MM",
        "description": "Výška hrotu vibračního nože pro 12mm PET felt.",
        "source": "Osobní znalostní báze_ PET_felty_moodpasta_V2.md",
        "confidence": 0.95,
        "validation_status": "accepted",
        "rule_class": "CLASS_B"
      },
      "cutter_type_id": 1,
      "material_thickness_mm": 12.0,
      "ideal_h2_range": [-0.3, -0.1],
      "critical_h2_threshold": 0.1
    },
    {
      "metadata": {
        "rule_id": "RULE_H2_VIBRATE_24MM",
        "description": "Výška hrotu vibračního nože pro 24mm PET felt.",
        "source": "CNC operátor - Wynnwood",
        "confidence": 0.90,
        "validation_status": "accepted",
        "rule_class": "CLASS_B"
      },
      "cutter_type_id": 1,
      "material_thickness_mm": 24.0,
      "ideal_h2_range": [-0.5, -0.2],
      "critical_h2_threshold": 0.1
    }
  ],
  "sequence_rules": [
    {
      "metadata": {
        "rule_id": "RUL...
```

## 📄 `src\Knowledge_base\__init__.py`

```py
from .models import (
    RuleClass,
    ValidationStatus,
    Severity,
    ThicknessConfidence,
    EpistemicMetadata,
    H2Rule,
    SequenceRule,
    FixationRule,
    ValidationResult
)
from .engine import KnowledgeBaseEngine
...
```

