# HANDOFF — Session 2026-06-11
## Bug: Element Cut Sequence Detection in VCF Parser v20

---

## 1. Problém

Parser nedokázal určit pořadí, v jakém jsou elementy odesílány k řezu na CNC. 
Veškeré výstupy (JSON, MD, dashboard) byly založeny na lineárním čtení pořadí vrstev, 
nikoliv na skutečném pořadí elementů.

## 2. Hex Diff Analysis

Dva identické VCF soubory se 3 koncentrickými obdélníky, pouze změněné pořadí řezu:

| Soubor | Pořadí | Očekávání |
|--------|--------|-----------|
| `inward_cut` | vnější → střední → vnitřní | ✅ OK |
| `outward_cut` | vnitřní → střední → vnější | ❌ CHYBA |

**Nález:** VCF binárka ukládá elementy v pořadí řezu (file order = cut order). 
Při změně pořadí v LightBurnu je VCF přepsán s elementy v novém pořadí — 
potvrzeno hex diffem (14 regionů rozdílů = přeuspořádané souřadnice elementů).

## 3. Implementované změny

### `src/vcf_parser_v20.py` (core fix)

- **Každý element** dostává pole `cut_order` (index v souboru = pořadí řezu)
- **Element-level sequence validation**: pro každou vrstvu spočítá bbox plochy elementů 
  a ověří, zda monotónně klesají (vnější → vnitřní = správně)
- **Warning**: `"⚠️ Kritická chyba sekvence elementů ve vrstvě X (cutter): Elementy jsou řazeny od vnitřního k vnějšímu (zvyšující se plocha)! Hrozí poškození materiálu."`
- **KB nesting suppression**: `SEQUENCE_NESTING_ERROR` z Knowledge Base engine jsou potlačeny, 
  pokud je element-level sekvence již potvrzena jako správná (žádné violations)
- **Nové struktury v `operation_sequence`**:
  - `element_sequence[]` — sekvence všech elementů v pořadí řezu
  - `element_sequence_violations[]` — popis porušení sekvence

### `src/app.py` (dashboard)

- **LLM prompt** obsahuje sekci `Element Cut Order` s výpisem sekvence
- **Kontrola před řezem** (CNC role): specifická hláška pro element-level sekvenci
- **Layer Card expander**: nová tabulka "Sekvence řezu elementů"
- **Falešně pozitivní varování** potlačena

## 4. Test Results (CURRENT CODE — commit c7acc75)

| Soubor | `seq_correct` | Violations | Warnings |
|--------|:---:|:---:|---|
| `inward_cut` (vnější→vnitřní) | ✅ True | 0 | žádné o sekvenci |
| `outward_cut` (vnitřní→vnější) | ❌ False | 1 | chyba sekvence + nesting backup |
| `demo/Ofset_3x.VCF` (prohozené) | ❌ False | 1 | chyba sekvence + nesting backup |

Demo soubor `Ofset_3x.VCF` má dlouhodobě neodhalenou chybu: 
big(6825) → smallest(5225) → medium(6025) — nesprávné pořadí.

## 5. Known Remaining Issues

### 5.1 Nesting detection (parent_id / children_ids) — PRE-EXISTING

Koncentrické elementy se stejným centroidem způsobí inverzi parent/child vztahů.
Všechny elementy mají centroid (618.64, 1201.18), který leží uvnitř bboxu všech 
ostatních elementů. Výsledek: outer element dostane `parent_id` = inner element.

**Kód:** `vcf_parser_v20.py` řádky 847-871 (`_is_point_inside_element`)

**Dopad:** `SEQUENCE_NESTING_ERROR` varování z KB engine je nespolehlivé pro 
koncentrické elementy. Momentálně potlačeno podmínkou `operation_sequence_info.get("element_sequence_violations")`.

**Možné řešení:** Nesting detekce by měla používat bbox containment (bbox A ⊆ bbox B), 
nikoliv centroid containment.

### 5.2 Streamlit modul caching

Streamlit cachuje importované moduly. Pokud Streamlit server nebyl restartován 
po nasazení nového kódu, stará verze parseru je stále v paměti.

**Řešení:** Restartovat Streamlit server (`Ctrl+C` → `streamlit run src/app.py`)

### 5.3 Jedna vrstva, jeden cutter type

Sekvenční detekce funguje pouze pokud je ve vrstvě více elementů se stejným cutter type.
Pro reálné soubory s více vrstvami (V-slot + Vibrate cutter) je potřeba otestovat 
layer-level i element-level detekci dohromady.

### 5.4 H2=12.0 mm warning (pre-existing, unrelated)

Oba testovací soubory mají H2=12.0 mm pro 12mm materiál = nulový průřez. 
Toto je samostatný warning z KB engine, nesouvisí s pořadím řezu.

## 6. Architecture

```
VCF binary → vcf_parser_v20.py → parsed_data dict
                                    ↓
              operation_sequence {
                layer_order: [0],
                sequence_is_correct: bool,
                element_sequence: [{cut_order, element_id, layer_index, ...}],
                element_sequence_violations: [{layer_index, layer_cutter, 
                                               element_order, bbox_areas}]
              }
                                    ↓
              app.py → dashboard display (st.success/st.error)
              app.py → LLM prompt string embedding
```

## 7. Files Changed

| File | Lines | Changes |
|------|-------|---------|
| `src/vcf_parser_v20.py` | +59, -2 | Element seq detection + nesting suppression |
| `src/app.py` | +35, -2 | Dashboard display of element sequence |

## 8. Test Data Added

| File | Purpose |
|------|---------|
| `data/Bugs/Ofset_3x_inward_cut.VCF` | Correct order (outer→inner) |
| `data/Bugs/Ofset_3x_outward_cut.VCF` | Wrong order (inner→outer) |
| `data/Bugs/Ofset_3x_inward_cut_v20.json` | Expected output for inward |
| `data/Bugs/Ofset_3x_outward_cut_v20.json` | Expected output for outward |
| `data/Bugs/hex_diff_report.md` | Hex diff analysis between inward/outward |
