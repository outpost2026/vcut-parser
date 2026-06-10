# DESIGN V20 — B2B Visual & Topographical Playbook

**Verze:** 2.0 (Červen 2026)  
**Repo:** `vcf_integrace`  
**Branch:** `features/dashboard_principles`  
**Cíl:** Sjednotit Streamlit dashboard s vizuální identitou SYSTEQ (systeq.cz) pro B2B dema, postaveno na principech kognitivní psychologie (Hickův zákon, Millerův zákon, Gestalt, Fitts, Preattentivní zpracování).  
**Stav:** Implementováno v `src/app.py` (HUD+MFD architektura).

---

## Přehled změn (CO)

### Výchozí verze (1.0, branche `feature/design`)

| # | Změna | Soubor | Řádky |
|---|-------|--------|-------|
| 1 | **SYSTEQ header bar** — logo SYS/TEQ + API ONLINE + nav odkazy | `app.py` | 88–148 |
| 2 | **Headline text** — "Moodpasta Manufacturing Intelligence" → "CAM Automation Platform" | `app.py` | 151–153 |
| 3 | **System metrics** — 4-sloupcový kompaktní grid (33+ VCF, 100%, 86%, 0%) | `app.py` | 156–179 |
| 4 | **KPI sub-labels** — zvětšeny (12px), zesvětleny (#9CA3AF) | `app.py` | CSS `.kpi-sub` |
| 5 | **Footer** — SYSTEQ © 2026 + kontakt + engine verze + motto | `app.py` | 726–734 |
| 6 | **Login page title** — "Moodpasta Parser Demo" → "SYSTEQ // CAM Automation Platform" | `app.py` | 12 |
| 7 | **Page title** — změněn na "SYSTEQ // CAM Automation Platform | v20 B2B" | `app.py` | 23 |
| 8 | **Akcentová barva tlačítek** — #10B981 → #0d9488 (teal) | `app.py` | CSS `.stButton` |

### HUD+MFD architektura (2.0, branche `features/dashboard_principles`)

| # | Změna | Princip | Efekt |
|---|-------|---------|-------|
| 9 | **Hero blok** — cut time dominantní (48px) + 6 compact statů | Miller (10→1 chunk), Preattentive (velikost) | Okamžitá orientace <200 ms |
| 10 | **2D viz na Level 0** — universalní (všechny role), bez scroll | Gestalt proximity (data + viz v jednom viewportu) | Operátor nepropadává informace |
| 11 | **Rizika podmíněná** — skryta při risk_score = 0 | Normalizace deviace (Challenger) | Warning zůstane warningem |
| 12 | **Tier 2 KPI → expander** — default closed | Miller (5→0 chunků na Level 0) | Čistý HUD, detail na vyžádání |
| 13 | **Layer Card → expander** — default closed | Miller (dataframe není Level 0) | Pouze když potřeba |
| 14 | **Metadata → expander** — default closed | Miller (hash/magic jsou Level 2) | Pouze pro debugging |
| 15 | **Download a až za MFD** — po všech datech | Fitts (akce až po rozhodnutí), Gestalt proximity | Eliminace false proximity |
| 16 | **Status badge** — OK/WARNING/CRITICAL (barevný pill) | Preattentive (barva), TMI (hierarchie alarmů) | Okamžitá detekce rizika |
| 17 | **HUD/MFD separator** — gradient line | Gestalt proximity (vizuální oddělení úrovní) | Jasná hierarchie |

---

## Detailní dokumentace (CO + PROČ + KDE + JAK)

### 1. SYSTEQ Header Bar

**CO:** Sticky header s logem, API statusem a navigačními odkazy.  
**PROČ:** Streamlit app musí vizuálně patřit k SYSTEQ brandu — při B2B demu klient vidí konzistentní identitu napříč webem (systeq.cz) i dashboardem. Header řeší objektivizaci IP: "není to skript, je to platforma".  
**KDE:** `app.py` — hned za `<style>` blokem, jako první element po set_page_config.  
**JAK:** Vložen jako `st.markdown()` s HTML/CSS. Struktura:

```html
<div class="systeq-header">
  <div class="sh-logo">
    <span class="sh-logo-sys">SYS</span>      <!-- #0d9488 (teal) -->
    <span class="sh-logo-teq">TEQ</span>      <!-- #D35400 (orange) -->
    <span class="sh-logo-tag">CAM Automation</span>
  </div>
  <nav class="sh-nav">
    <div class="sh-pill"><div class="sh-dot"></div>API ONLINE</div>  <!-- zelená tečka + blink animace -->
    <a class="sh-link">GitHub</a>
    <a class="sh-link">LinkedIn</a>
    <a class="sh-link">+420 735 045 256</a>
  </nav>
</div>
```

**CSS třídy (vše inline v `<style>`):**

| Třída | Účel | Klíčové vlastnosti |
|-------|------|--------------------|
| `.systeq-header` | Hlavní kontejner | `display: flex; justify-content: space-between; position: sticky; top: 0; backdrop-filter: blur(10px); z-index: 200` |
| `.sh-logo-sys` | "SYS" část loga | `color: #0d9488; font-weight: 700` |
| `.sh-logo-teq` | "TEQ" část loga | `color: #D35400; font-weight: 700` |
| `.sh-logo-tag` | "CAM Automation" tag | `font-size: .65rem; color: #64748b; border-left: 1px solid rgba(...)` |
| `.sh-pill` | Status pill | `border: 1px solid rgba(...); padding: .25rem .65rem` |
| `.sh-dot` | Zelená tečka | `width: 6px; height: 6px; background: #22c55e; animation: blink 2.2s` |
| `.sh-link` | Nav odkazy | `font-size: .75rem; color: #64748b; transition: color .2s` |
| `@keyframes blink` | Blikání tečky | `0%,100%{opacity:1} 50%{opacity:.3}` |

**Poznámka:** Header se zobrazí až po autentizaci — login page používá jen textový titulek.

---

### 2. Headline Text

**CO:** Nahrazen hero text.  
**PROČ:** Původní "Moodpasta Manufacturing Intelligence" byl příliš specifický pro jednoho klienta. Nový text je univerzální B2B value proposition: "CAM Automation Platform — Deterministický parser proprietárních CNC formátů."  
**KDE:** `app.py` řádky 151–153.  
**JAK:**

```python
st.markdown("<h1 style='text-align: center; ...'>CAM Automation Platform</h1>", ...)
st.markdown("<p style='text-align: center; color: #64748b; ...'>Deterministický parser proprietárních CNC formátů.<br>VCF → DXF → strukturovaná CSV &amp; JSON data pro ERP/AI integraci</p>", ...)
```

---

### 3. System Metrics

**CO:** 4-sloupcový kompaktní grid s výkonnostními parametry engine.  
**PROČ:** Přebíráno z HTML verze (systeq.cz) — ukazuje klientovi okamžitou důvěryhodnost (33+ souborů, 100% RPA, 86% přesnost, 0% halucinací).  
**KDE:** `app.py` řádky 156–179 (vloženo za headline, před role selectbox).  
**JAK:** Čistý HTML grid s CSS třídami:

```html
<div class="metrics-mini">
  <div class="m-item">
    <div class="m-val">33<span>+</span></div>
    <div class="m-label">VCF souborů<br>parsováno</div>
  </div>
  <!-- ... 3 další sloupce -->
</div>
```

**CSS:**

| Třída | Vlastnosti |
|-------|------------|
| `.metrics-mini` | `display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; border: 1px solid rgba(255,255,255,.055); margin-bottom: 1.5rem` |
| `.m-item` | `background: #0e1320; padding: 1rem 1.2rem` |
| `.m-val` | `font-size: 1.4rem; font-weight: 700` |
| `.m-val span` | `color: #0d9488` (teal accent) |
| `.m-label` | `font-size: .65rem; color: #64748b` |
| `.m-note` | `font-size: .6rem; color: #2e3d52` |

**Poznámka:** Data jsou statická (pevně zakódovaná) — jedná se o marketingový prvek, ne o live metriky.

---

### 4. KPI Sub-labels (čitelnost)

**CO:** Zvětšeny a zesvětleny popisky pod KPI hodnotami.  
**PROČ:** Dle user feedbacku byly původní popisky "příliš malé, příliš tmavý odstín".  
**KDE:** CSS třída `.kpi-sub` v `<style>` bloku.  
**JAK:**

```css
/* PŮVODNÍ */
.kpi-sub { font-size: 11px; color: #6B7280; margin-top: 2px; }

/* NOVĚ */
.kpi-sub { font-size: 12px; color: #9CA3AF; margin-top: 2px; }
```

Změní se pouze hodnoty `font-size` (11→12px) a `color` (#6B7280→#9CA3AF). Třída je použita ve všech KPI kartách (Tier 1 i Tier 2).

---

### 5. Footer

**CO:** Zápatí dashboardu s brandem, kontaktem a technickými informacemi.  
**PROČ:** Dokončuje vizuální rámec — header + content + footer. Obsahuje email a telefon pro B2B kontakt.  
**KDE:** `app.py` řádky 580–590 — vloženo až po download sekci (před `except` blok).  
**JAK:**

```html
<div class="systeq-footer">
  <div class="sf-logo"><span class="sf-sys">SYS</span><span class="sf-teq">TEQ</span> © 2026</div>
  <div class="sf-contact">
    <a href="mailto:sousek@systeq.cz">sousek@systeq.cz</a> ·
    <a href="tel:+420735045256">+420 735 045 256</a>
  </div>
  <div class="sf-meta">Engine v20 deterministic · outpost2026</div>
  <div class="sf-motto">Hledám funkční řešení v balastu.</div>
</div>
```

**CSS:**

| Třída | Vlastnosti |
|-------|------------|
| `.systeq-footer` | `display: flex; justify-content: space-between; flex-wrap: wrap; border-top: 1px solid rgba(...); padding: 1.2rem 0; margin-top: 2.5rem` |
| `.sf-logo` | `font-size: .82rem; color: #64748b` |
| `.sf-sys / .sf-teq` | Stejné barvy jako v headeru (#0d9488 / #D35400) |
| `.sf-contact` | `font-size: .65rem; color: #2e3d52` |
| `.sf-contact a` | `color: #64748b; text-decoration: none; :hover → #0d9488` |
| `.sf-meta` | `font-size: .65rem; color: #2e3d52` |
| `.sf-motto` | `font-size: .68rem; color: #2e3d52; font-style: italic` |

---

### 6. HUD+MFD architektura (HUD Level 0 + MFD expandery)

**CO:** Kompletní restrukturalizace layoutu z ploché sekvence 10+ sekcí na hierarchickou HUD+MFD architekturu.  
**PROČ:** Dle `docs/PRINCIPLES_DASHBOARD_DESIGN.md` — analýza ukázala 10 principiálních violací (Miller: overflow 10 chunků; Hick: 20+ alternativ; Gestalt: špatná proximity/similarity; TMI: multiple similar alarms). Nová architektura redukuje Level 0 na 1 hero blok + 1 vizualizace = 2 chunky (Miller OK).  
**KDE:** `app.py` — celý blok od hero po footer.  
**JAK:**

#### 6.1 Hero blok (řádky 397–454)

```
┌──────────────────────────────────────────────────────┐
│  12 min 34 s                    [CRITICAL] [Risk: 0.23]│
│  Cut time prediction · ±2–5 %                        │
│  ─────────────────────────────────────────────────── │
│  95.3 m    1208×2790    5 vstev    142 el.    0.341 m²    Standardní  │
│  Dráha     Rozměry      Vrstvy     Elementy   Plocha    Složitost    │
└──────────────────────────────────────────────────────┘
```

**CSS třídy:**

| Třída | Účel | Klíčové vlastnosti |
|-------|------|--------------------|
| `.hero-block` | Hlavní kontejner | `background: linear-gradient(135deg, #111827, #0F172A); border-radius: 12px; padding: 20px 24px` |
| `.hero-main` | Řádek čas + status | `display: flex; justify-content: space-between; flex-wrap: wrap` |
| `.hero-time` | Dominantní cut time | `font-size: 48px; font-weight: 800; color: #0d9488` |
| `.hero-time-label` | Popiska pod časem | `font-size: 11px; color: #64748b; text-transform: uppercase` |
| `.hero-status-badge` | Status pill | `padding: 6px 14px; border-radius: 20px; font-size: 12px` |
| `.hero-status-badge.ok` | OK stav | `background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3)` |
| `.hero-status-badge.warn` | Warning stav | `background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3)` |
| `.hero-status-badge.critical` | Critical stav | `background: rgba(244,63,94,0.15); color: #F43F5E; border: 1px solid rgba(244,63,94,0.3)` |
| `.hero-stats` | Řádek statistik | `display: flex; gap: 24px; flex-wrap: wrap; border-top: 1px solid rgba(255,255,255,0.06)` |
| `.hero-stat-value` | Hodnota statu | `font-size: 18px; font-weight: 700; color: #e2e8f0` |
| `.hero-stat-label` | Popiska statu | `font-size: 10px; color: #64748b; text-transform: uppercase` |

#### 6.2 2D vizualizace na Level 0 (řádky 456–461)

**JAK:**
```python
if fig_viz:
    st.markdown("#### 2D Digitální model drah")
    st.image(png_bytes, caption=f"{uploaded_file.name} — 1920×1080", use_column_width=True)
```

**PROČ:** 2D viz je nyní universalní (všechny role ji vidí) a je ihned pod hero blokem bez scroll. Role-specifická sekce pro CNC již neobsahuje 2D viz — pouze "Kontrola před řezem".

#### 6.3 Podmíněná rizika (řádky 463–483)

**JAK:**
```python
if risk_score > 0 or criticals or warnings_w:
    st.markdown("### Rizika")
    # ... zobrazit detail rizik
# else: nic — žádná normalizace deviace
```

**PROČ:** Fix normalization of deviance (Challenger case study). Pokud riziko neexistuje, nezobrazuje se sekce "100% OK" — ta by byla vždy přítomna a degraduje celý varovný systém.

#### 6.4 HUD→MFD separator (řádek 488)

```html
<div class="hud-separator"></div>
```

Gradient line: `background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent)` — opticky odděluje Level 0 od Level 1.

#### 6.5 MFD expandery (řádky 490–563)

Tři Streamlit expandery v sekvenci:

1. **TIER 2 — Sekundární parametry** — 5 KPI karet (complexita, tloušťka, risk score, sub-zakázky, panel formát) v původním grid layoutu
2. **Layer Card — CAM nástroje per vrstva** — datový dataframe (přesunut z Level 0)
3. **Metadata & integrita** — parser version, magic, timestamp, MD5 hash

Všechny expandery jsou default `expanded=False` — obsah se načítá až na kliknutí (Miller: Level 0 = 2 chunky).

#### 6.6 Pořadí sekcí (nový layout)

```
1. SYSTEQ header                          (sticky, beze změny)
2. Headline + Role selector + Uploader    (beze změny)
3. HERO BLOCK (cut time + stats + status) ← NOVĚ: 1 chunk místo 10
4. 2D vizualizace                          ← NOVĚ: Level 0 pro všechny role
5. Rizika (pouze pokud > 0)               ← ZMĚNA: podmíněné zobrazení
── HUD/MFD separator ──
6. TIER 2 KPI (expander)                  ← NOVĚ: přesunuto z Level 0
7. Layer Card (expander)                  ← NOVĚ: přesunuto z Level 0
8. Metadata (expander)                    ← NOVĚ: přesunuto z Level 0
9. Role-specific sekce                    ← ZMĚNA: CNC bez 2D viz
10. LLM Prompt (expander)                 ← beze změny
11. Download artifacts                    ← NOVĚ: přesunuto za všechna data
12. System metrics                        ← beze změny
13. Footer                                ← beze změny
```

---

## Kontaktní údaje (email/telefon)

Všechny soubory napříč repozitáři byly opraveny:

| Soubor | Stará hodnota | Nová hodnota |
|--------|---------------|--------------|
| `src/index.html` (3×) | `+420 735 052 56` | `+420 735 045 256` |
| `src/index.html` (1×) | `ondra.sousek@gmail.com` | `sousek@systeq.cz` |
| `GROUND_TRUTH.md` | `ondra.sousek@gmail.com, +420 735 052 56` | `sousek@systeq.cz, +420 735 045 256` |
| `docs/handoffs/handoff_beta0.2-1.0.txt` (2×) | `ondra.sousek@gmail.com` | `sousek@systeq.cz` |

---

## Barevná paleta SYSTEQ (pro oba repozitáře)

| Role | Hex | Použití |
|------|-----|---------|
| Pozadí app | `#0a0e14` | `.stApp` |
| Pozadí karet | `#111827` | `.kpi-card` |
| Pozadí panel | `#0e1320` | `.m-item` |
| Akcent (teal) | `#0d9488` | Logo SYS, tlačítka, highlighty |
| Akcent (orange) | `#D35400` | Logo TEQ |
| Text primární | `#e2e8f0` | Nadpisy, hlavní text |
| Text muted | `#64748b` | Popisky, sekundární text |
| Text dim | `#2e3d52` | Poznámky, metada |
| Zelená (OK) | `#22c55e` | Statusy, tečka API |
| Tier 1 | `#10B981` | Primární KPI border |
| Tier 2 | `#F59E0B` | Sekundární KPI border |

---

## Architektura změn (KDE přesně)

### `src/app.py` — struktura souboru po změnách:

```
Řádky    Obsah
─────────────────────────────────────────────────────
1–6      Importy (beze změny)
8–20     Autentizace (login title změněn)
22–26    set_page_config (title změněn)
28–86    CSS <style> blok (PŘIDÁNY: header, metrics, footer třídy)
88–148   SYSTEQ header (NOVÝ)
151–153  Headline (ZMĚNĚN)
156–179  System metrics (NOVÝ)
181      Role selectbox (beze změny)
183      File uploader (beze změny)
185–590  Hlavní parsing logika a KPI (sub-labels opraveny v CSS)
580–590  Footer (NOVÝ — v else větev za download sekcí)
590–     Výjimky, empty state (beze změny)
```

---

## Provádění vizuálních korekcí (JAK pro dev)

### Chci změnit barvu loga:
Hledej v `<style>` bloku třídy `.sh-logo-sys` a `.sh-logo-teq`. Změň `color`.

### Chci přidat/ubrat navigační odkaz v headeru:
Hledej `<nav class="sh-nav">` — přidej/uber `<a class="sh-link">...</a>` blok. SVG ikony jsou inline.

### Chci změnit metriky (33+, 100%, ...):
Hledej `<div class="metrics-mini">` — každý `<div class="m-item">` je jeden sloupec. Můžeš přidat/ubrat.

### Chci upravit footer:
Hledej `<div class="systeq-footer">` — struktura je: logo | kontakt | meta | motto.

### Chci změnit email nebo telefon:
- Footer: hledej `sousek@systeq.cz` nebo `+420 735 045 256` v `app.py`
- HTML: `src/index.html` — hledej `sousek@systeq.cz` nebo `+420 735 045 256`

### Chci změnit KPI sub-label velikost/barvu:
Hledej v `<style>` bloku `.kpi-sub` — změň `font-size` a `color`.

### Chci změnit akcentní barvu (teal/orange):
Hledej CSS proměnné (nejsou použity — barvy jsou inline). Každou změnu proveď na všech místech, kde se barva vyskytuje. Doporučuji převést na CSS proměnné při větším redesignu.
