# Moodpasta VCF Parser — GCP_Deploy_v1.7
# ======================================
# Autor: Ondrej Sousek
# Datum: 2026-06-06
# Verze: v1.7

## ZMENY PROTI v1.6

### 1. Kalibracni protokol (BUS FACTOR > 1)
- NOVY SOUBOR: src/machine_profile.json
  - Definuje mereni 3 fyzikalnich konstant stroje:
    a) kinematicky rychlostni strop (pohyb 1000 mm bez zateze)
    b) uhlova brzda portalu (cas prujezdu pravo uhle zatacky)
    c) materialove tlumeni (korekcni faktory pro ruzne materialy)
  - Kazda konstanta ma atribut validation_status (empirical/calibrated/hypothesis)
  - Parser jiz NEOBSAHUJE hardcoded casove konstanty
  - Vsech 7 kinematickych parametru se nacita z machine_profile.json pri startu
  - Vypocita se epistemicky index duvery = empirical_pocet / celkem_pocet

### 2. Extrakce konfigurace z app.py
- NOVY SOUBOR: src/app_config.json
  - Extrahovane hodnoty:
    * machine_minute_cost_czk = 18.50 (cena strojni minuty)
    * material_cost_per_m2_czk = 420.00 (cena materialu/m2)
    * default_margin_percent = 45 (vychozi marze)
    * demo_password = "moodpasta-demo-2026"
    * panel_formats (6 definic formatu)
    * gcp konfigurace
  - app.py jiz neobsahuje HARDCODED ceny

### 3. Epistemicka d*uveryhodnost (KPI)
- NOVY KPI sloupec v dashboardu: Epistemicky index (0-100 %)
  - Zelena >= 40 % (D*uveryhodnost)
  - Zluta >= 20 % (C*astecna)
  - Cervena < 20 % (N*izka)
  - Data v parsed_data["epistemic_confidence_index"]

### 4. Dalsi zmeny
- models.py: EpistemicValidationStatus enum + MachineProfile/AppConfig dataclasses
- vcf_parser_v20.py: _load_machine_profile(), _get_epistemic_index() metody
- Dockerfile: COPY machine_profile.json + app_config.json
- deploy.ps1: bump v1.6 -> v1.7, validace novych JSONu

## PRACOVNOST ITERACE
~4 h (navrh + implementace)

## OVERENI
Test na 3 demo VCF souborech: identicky vystup jako v1.6 (stejne casy, delky, pocty elementu)
+ novy sloupec epistemickeho indexu v dashboardu

## DALSI ITERACE (v1.8)
- Shapely TopoSanitizer (geometricka sanace, Vektor B)
- --strict flag pro zamitani hypotez
- Validacni statusy u rychlosti (validation_status flags)
