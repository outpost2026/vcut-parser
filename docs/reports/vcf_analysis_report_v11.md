# 🔬 V11.1 Report: Korekce mapování elementů a extrakce pole geometrie

Tato iterace řeší problém chybějících geometrií. Parser již nečte pouze 'hlavičkový' polygon, ale sekvenčně iteruje přes celé pole navazujících prvků (čáry tvořící reálnou řeznou dráhu a polygony). Výsledná délka je přesným fyzickým součtem všech skutečných G-code-like instrukcí v souboru.

## 📄 manchester vše.VCF
- **Predikce času:** 1 min 22 s (na základě celkové dráhy 20335.42 mm)
- **Počet uložených elementů/instrukcí:** 58
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26940], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x2698a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26a7b], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26ac5], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26bb6], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26c00], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26cf1], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26d3b], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26e76], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26f67], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 48 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 400 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 20335.42 mm
    - Tool feeding (Počet: 1, H1: 3.0 mm, H2: 7.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

## 📄 diamond_01.VCF
- **Predikce času:** 0 min 35 s (na základě celkové dráhy 3090.14 mm)
- **Počet uložených elementů/instrukcí:** 5
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266b0], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x266fa], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x26744], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x2678e], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x267d8], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 3090.14 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 big coffee 12.8.2790x1200 bezotočení.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 1
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xd8c2], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 4.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)
  - **Vrstva 3:** Rychlost 100 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)

## 📄 PCB.VCF
- **Predikce času:** 1565 min 53 s (na základě celkové dráhy 18787713.24 mm)
- **Počet uložených elementů/instrukcí:** 2038
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x27299], Body/Uzly: 2, Délka dráhy: 2550.0 mm
  - Geometrie: Line [@ 0x272e3], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x2732d], Body/Uzly: 2, Délka dráhy: 2550.0 mm
  - Geometrie: Line [@ 0x27377], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x273c1], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x274b2], Body/Uzly: 2, Délka dráhy: 2550.0 mm
  - Geometrie: Line [@ 0x274fc], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x27546], Body/Uzly: 2, Délka dráhy: 2550.0 mm
  - Geometrie: Line [@ 0x27590], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x275da], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 2028 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 18787713.24 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 8.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)
  - **Vrstva 3:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 9.0 mm)
  - **Vrstva 4:** Rychlost 100 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 9.0 mm)

## 📄 line_01.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 1
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266f8], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 small coffee 2790x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 4
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xdc73], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe024], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe15f], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xfd27], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 3:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

## 📄 geometry_dif_01.VCF
- **Predikce času:** 0 min 37 s (na základě celkové dráhy 6870.14 mm)
- **Počet uložených elementů/instrukcí:** 5
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266b0], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x266fa], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26744], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x2678e], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x267d8], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 6870.14 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 8.0 mm)

## 📄 2560x150 s fazetou 45st hl6.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 3
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xd5a6], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xd6e1], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xd81c], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 500 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 FLUENZ L.VCF
- **Predikce času:** 3 min 6 s (na základě celkové dráhy 13748.27 mm)
- **Počet uložených elementů/instrukcí:** 139
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26289], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x263fb], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x2648f], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x265b7], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x26773], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x267bd], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x2692f], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26979], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x26bc9], Body/Uzly: 2, Délka dráhy: 4.0 mm
  - Geometrie: Line [@ 0x26ca7], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - *... a dalších 129 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 80 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 13748.27 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 bigcoffee 12.8. 2790x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 3:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 12.0 mm, H2: -0.5 mm)

## 📄 Big_coffee_dune_2790_600.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 1
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xe417], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 3:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.45 mm)

## 📄 FLUENZ BOLD M_Varianta A.VCF
- **Predikce času:** 4 min 38 s (na základě celkové dráhy 19795.1 mm)
- **Počet uložených elementů/instrukcí:** 460
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x16c6e], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16cb8], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16d02], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16d4c], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16d96], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x16de0], Body/Uzly: 2, Délka dráhy: 4.47 mm
  - Geometrie: Line [@ 0x16e2a], Body/Uzly: 2, Délka dráhy: 4.47 mm
  - Geometrie: Line [@ 0x16f08], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x16f52], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16f9c], Body/Uzly: 2, Délka dráhy: 4.47 mm
  - *... a dalších 450 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 75 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 19795.1 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 V měřítku.VCF
- **Predikce času:** 11 min 53 s (na základě celkové dráhy 69817.07 mm)
- **Počet uložených elementů/instrukcí:** 95
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x28fbd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x29007], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x29051], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x2909b], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x290e5], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x2912f], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x29179], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x291c3], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x2920d], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x29257], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 85 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 69817.07 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)

## 📄 FLUENZ BOLD S upr.VCF
- **Predikce času:** 3 min 30 s (na základě celkové dráhy 15603.56 mm)
- **Počet uložených elementů/instrukcí:** 323
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x186f8], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x1886a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x188b4], Body/Uzly: 2, Délka dráhy: 4.0 mm
  - Geometrie: Line [@ 0x188fe], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x18948], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x18a26], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x18a70], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x18aba], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x18b04], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x18be2], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - *... a dalších 313 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 80 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 15603.56 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 botanic vše.VCF
- **Predikce času:** 2832 min 4 s (na základě celkové dráhy 16990901.51 mm)
- **Počet uložených elementů/instrukcí:** 2162
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd5], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26e1f], Body/Uzly: 2, Délka dráhy: 975.0 mm
  - Geometrie: Line [@ 0x26e69], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26eb3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26fee], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x27038], Body/Uzly: 2, Délka dráhy: 975.0 mm
  - Geometrie: Line [@ 0x27082], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x270cc], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x27116], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 2152 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 16990901.51 mm
    - Tool feeding (Počet: 16470, H1: -0.0 mm, H2: 8.029891305820163e+283 mm)

## 📄 geometry_dif_02.VCF
- **Predikce času:** 1 min 9 s (na základě celkové dráhy 13740.28 mm)
- **Počet uložených elementů/instrukcí:** 10
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26912], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x2695c], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x269a6], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x269f0], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26a3a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26b2b], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26b75], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26bbf], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c09], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26c53], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 13740.28 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 8.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)

## 📄 FLUENZ BOLD S_Zdroj světla dole.VCF
- **Predikce času:** 3 min 40 s (na základě celkové dráhy 16400.0 mm)
- **Počet uložených elementů/instrukcí:** 45
### Ukázka elementů (prvních 10):
  - Geometrie: Polygon [@ 0x22abc], Body/Uzly: 4, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x25e51], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x25e9b], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x25ee5], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x25f2f], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x25f79], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x25fc3], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x2600d], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x26057], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - Geometrie: Line [@ 0x260a1], Body/Uzly: 2, Délka dráhy: 400.0 mm
  - *... a dalších 35 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 80 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 16400.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 26ks skladba.VCF
- **Predikce času:** 7 min 0 s (na základě celkové dráhy 20278.89 mm)
- **Počet uložených elementů/instrukcí:** 389
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26912], Body/Uzly: 2, Délka dráhy: 2900.0 mm
  - Geometrie: Line [@ 0x2695c], Body/Uzly: 2, Délka dráhy: 1220.0 mm
  - Geometrie: Line [@ 0x269a6], Body/Uzly: 2, Délka dráhy: 2900.0 mm
  - Geometrie: Line [@ 0x269f0], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26a3a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x28dc9], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x28e13], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x28e5d], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x28ea7], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x28ef1], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 379 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 50 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 20278.89 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)

## 📄 FLUENZ M.VCF
- **Predikce času:** 3 min 31 s (na základě celkové dráhy 21626.6 mm)
- **Počet uložených elementů/instrukcí:** 90
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x1f61e], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f668], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f6b2], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f6fc], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f746], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f790], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f7da], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f824], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f86e], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1f8b8], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 80 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 21626.6 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)
  - **Vrstva 2:** Rychlost 70 mm/s | Nástroj: Unknown (131072)
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 vyrobni_data_Pernerka-Service for office_Camel_12mm.VCF
- **Predikce času:** 12837 min 42 s (na základě celkové dráhy 154049425.22 mm)
- **Počet uložených elementů/instrukcí:** 1659
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd5], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26e1f], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26e69], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26eb3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26fee], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x27038], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x27082], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x270cc], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x27116], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 1649 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 154049425.22 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 botanic 2790 x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 400 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 300 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 3:** Rychlost 300 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 2790x1200 s fazetou.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 echoblock_2790_1200_fasets_new_offsets_speed_100.VCF
- **Predikce času:** 1 min 8 s (na základě celkové dráhy 26940.55 mm)
- **Počet uložených elementů/instrukcí:** 20
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26b74], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26bbe], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26c08], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c52], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26c9c], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26d8d], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26dd7], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26e21], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26e6b], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26eb5], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 10 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 500 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 26940.55 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 500 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 vyrobni_data_Pernerka-Service for office_Matcha_12mm.VCF
- **Predikce času:** 78729 min 41 s (na základě celkové dráhy 944753342.7 mm)
- **Počet uložených elementů/instrukcí:** 2610
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd5], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26e1f], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26e69], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26eb3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26fee], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x27038], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x27082], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x270cc], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x27116], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 2600 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 944753342.7 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 line_05.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 6.0 mm)
- **Počet uložených elementů/instrukcí:** 8
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266f8], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x2679f], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x26833], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x268da], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x2696e], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26aa9], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26b50], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x26be4], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 6.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 line_05.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 1
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266f8], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 1ks.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 45 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

## 📄 diamond_02.VCF
- **Predikce času:** 1 min 16 s (na základě celkové dráhy 9271.42 mm)
- **Počet uložených elementů/instrukcí:** 19
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266b0], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x266fa], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x26744], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x2678e], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x267d8], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x268b6], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x2694a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26994], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26a72], Body/Uzly: 2, Délka dráhy: 1.0 mm
  - Geometrie: Line [@ 0x268c9], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - *... a dalších 9 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 9271.42 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 FLUENZ XL.VCF
- **Predikce času:** 4 min 0 s (na základě celkové dráhy 24792.17 mm)
- **Počet uložených elementů/instrukcí:** 204
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x16708], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16752], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1679c], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x167e6], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16830], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1687a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x168c4], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1690e], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16958], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x169a2], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 194 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 24792.17 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)
  - **Vrstva 2:** Rychlost 70 mm/s | Nástroj: Unknown (131072)
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 echoblock_2790_1200_fasets_only.VCF
- **Predikce času:** 1 min 33 s (na základě celkové dráhy 13740.28 mm)
- **Počet uložených elementů/instrukcí:** 10
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26912], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x2695c], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x269a6], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x269f0], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26a3a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26b2b], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26b75], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26bbf], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c09], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26c53], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 13740.28 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 vyrobni_data_Pernerka-Service for office_Dark Knight_12mm.VCF
- **Predikce času:** 107 min 46 s (na základě celkové dráhy 6387435.87 mm)
- **Počet uložených elementů/instrukcí:** 1761
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd5], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26e1f], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26e69], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26eb3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26fee], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x27038], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x27082], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x270cc], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x27116], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 1751 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 990 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 6387435.87 mm
    - Tool feeding (Počet: -268435456, H1: 0.0 mm, H2: 0.0 mm)

## 📄 FLUENZ BOLD M_Varianta A 2ks skladba.VCF
- **Predikce času:** 6 min 27 s (na základě celkové dráhy 27930.65 mm)
- **Počet uložených elementů/instrukcí:** 987
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x16c6e], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16cb8], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16d02], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16d4c], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x16d96], Body/Uzly: 2, Délka dráhy: 2.83 mm
  - Geometrie: Line [@ 0x16de0], Body/Uzly: 2, Délka dráhy: 4.47 mm
  - Geometrie: Line [@ 0x16e2a], Body/Uzly: 2, Délka dráhy: 4.47 mm
  - Geometrie: Line [@ 0x16f08], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16f52], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x16f9c], Body/Uzly: 2, Délka dráhy: 4.0 mm
  - *... a dalších 977 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 75 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 27930.65 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 FLUENZ BOLD S_Zdroj světla nahoře.VCF
- **Predikce času:** 4 min 48 s (na základě celkové dráhy 21893.91 mm)
- **Počet uložených elementů/instrukcí:** 231
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x10415], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Line [@ 0x107d7], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1086b], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x108ff], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x10a71], Body/Uzly: 2, Délka dráhy: 4125.31 mm
  - Geometrie: Line [@ 0x10abb], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x10b05], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x10dfc], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1112a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x11174], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 221 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 80 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 21893.91 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 Fishbone 2790x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)
  - **Vrstva 3:** Rychlost 150 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)

## 📄 data řez.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 12.0 mm, H2: -0.5 mm)

## 📄 FLUENZ BOLD S_ozub kolo na objímku.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 0
### Ukázka elementů (prvních 10):
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Unknown (131072)
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

## 📄 Vzorky_15052026_training.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.48 mm)
- **Počet uložených elementů/instrukcí:** 6
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xd8c2], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xd9fd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe947], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xec07], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xedd6], Body/Uzly: 2, Délka dráhy: 0.48 mm
  - Geometrie: Line [@ 0x1021d], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 300 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.48 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 300 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 3:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 Arbyd_výrobní data_V1 20.5.2025.VCF
- **Predikce času:** 1121 min 14 s (na základě celkové dráhy 6725972.13 mm)
- **Počet uložených elementů/instrukcí:** 1668
### Ukázka elementů (prvních 10):
  - Geometrie: Circle [@ 0x26b2f], Body/Uzly: 31, Délka dráhy: 9.38 mm
  - Geometrie: Circle [@ 0x27516], Body/Uzly: 38, Délka dráhy: 11.06 mm
  - Geometrie: Circle [@ 0x28103], Body/Uzly: 36, Délka dráhy: 14.98 mm
  - Geometrie: Circle [@ 0x28c5c], Body/Uzly: 36, Délka dráhy: 49.12 mm
  - Geometrie: Circle [@ 0x297b5], Body/Uzly: 36, Délka dráhy: 20.7 mm
  - Geometrie: Circle [@ 0x2a30e], Body/Uzly: 39, Délka dráhy: 3.38 mm
  - Geometrie: Circle [@ 0x2bb7c], Body/Uzly: 39, Délka dráhy: 0.05 mm
  - Geometrie: Line [@ 0x2dd29], Body/Uzly: 2, Délka dráhy: 2.0 mm
  - Geometrie: Circle [@ 0x2fb3c], Body/Uzly: 30, Délka dráhy: 3.22 mm
  - Geometrie: Circle [@ 0x30f9e], Body/Uzly: 29, Délka dráhy: 3.11 mm
  - *... a dalších 1658 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 6725972.13 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 26ks skladba_nesting.VCF
- **Predikce času:** 7 min 6 s (na základě celkové dráhy 34258.84 mm)
- **Počet uložených elementů/instrukcí:** 192
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd6], Body/Uzly: 2, Délka dráhy: 2900.0 mm
  - Geometrie: Line [@ 0x26e20], Body/Uzly: 2, Délka dráhy: 1220.0 mm
  - Geometrie: Line [@ 0x26e6a], Body/Uzly: 2, Délka dráhy: 2900.0 mm
  - Geometrie: Line [@ 0x26eb4], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efe], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x294dd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x29ce5], Body/Uzly: 2, Délka dráhy: 24.0 mm
  - Geometrie: Line [@ 0x29d2f], Body/Uzly: 2, Délka dráhy: 12.0 mm
  - Geometrie: Line [@ 0x29d79], Body/Uzly: 2, Délka dráhy: 24.0 mm
  - Geometrie: Line [@ 0x29dc3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - *... a dalších 182 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 34258.84 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)
  - **Vrstva 2:** Rychlost 100 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 3.0 mm)
  - **Vrstva 3:** Rychlost 50 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)

## 📄 vyrobni_data_Pernerka-Service for office_Savanna_12mm.VCF
- **Predikce času:** 6208 min 38 s (na základě celkové dráhy 74500668.0 mm)
- **Počet uložených elementů/instrukcí:** 1736
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd5], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26e1f], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26e69], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26eb3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26fee], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x27038], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x27082], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x270cc], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x27116], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 1726 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 74500668.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 musica 2790x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 5
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xde80], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x122e0], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x13c3f], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x143d6], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x1559e], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)
  - **Vrstva 3:** Rychlost 75 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 4:** Rychlost 75 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)

## 📄 vyrobni_data_Pernerka-Service for office_Terracota_12mm.VCF
- **Predikce času:** 136 min 2 s (na základě celkové dráhy 1629417.05 mm)
- **Počet uložených elementů/instrukcí:** 3428
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26dd5], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26e1f], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26e69], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x26eb3], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26efd], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26fee], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x27038], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x27082], Body/Uzly: 2, Délka dráhy: 2850.0 mm
  - Geometrie: Line [@ 0x270cc], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x27116], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 3418 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 1629417.05 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.3 mm)

## 📄 small fishbone 2790x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 7
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xd8c2], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdb38], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe024], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe190], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xf1d5], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xf857], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xfed9], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)
  - **Vrstva 3:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)

## 📄 stripe sixty 1200x2790.VCF
- **Predikce času:** 1048 min 10 s (na základě celkové dráhy 6287502.42 mm)
- **Počet uložených elementů/instrukcí:** 319
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xd796], Body/Uzly: 2, Délka dráhy: 2792.0 mm
  - Geometrie: Line [@ 0xd7e0], Body/Uzly: 2, Délka dráhy: 1202.0 mm
  - Geometrie: Line [@ 0xd82a], Body/Uzly: 2, Délka dráhy: 2792.0 mm
  - Geometrie: Line [@ 0xd874], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0xd8be], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdb9a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdc8b], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdcd5], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdf38], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdf82], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 309 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 100 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 6287502.42 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 0.0 mm)
  - **Vrstva 2:** Rychlost 100 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 9.0 mm)
  - **Vrstva 3:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 12.0 mm)
  - **Vrstva 4:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -1.0 mm)

## 📄 bigcoffee 12.8. 2790x1200.VCF
- **Predikce času:** 0 min 15 s (na základě celkové dráhy 0.0 mm)
- **Počet uložených elementů/instrukcí:** 1
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xead8], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 200 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 4.0 mm, H2: 9.5 mm)
  - **Vrstva 2:** Rychlost 100 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 9.5 mm)
  - **Vrstva 3:** Rychlost 100 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 FLUENZ S.VCF
- **Predikce času:** 19 min 53 s (na základě celkové dráhy 129602.82 mm)
- **Počet uložených elementů/instrukcí:** 202
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0xde3d], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xde87], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xded1], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdf1b], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdf65], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdfaf], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xdff9], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe043], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe08d], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0xe0d7], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 192 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 129602.82 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)
  - **Vrstva 2:** Rychlost 70 mm/s | Nástroj: Unknown (131072)
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 1, H1: 24.0 mm, H2: -0.5 mm)

## 📄 rectangle_01.vcf
- **Predikce času:** 0 min 35 s (na základě celkové dráhy 3090.14 mm)
- **Počet uložených elementů/instrukcí:** 5
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266b0], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x266fa], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x26744], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x2678e], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x267d8], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 3090.14 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 rectangle_02.vcf
- **Predikce času:** 0 min 56 s (na základě celkové dráhy 6180.28 mm)
- **Počet uložených elementů/instrukcí:** 15
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x266b0], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x266fa], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x26744], Body/Uzly: 2, Délka dráhy: 1000.0 mm
  - Geometrie: Line [@ 0x2678e], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x267d8], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x2686c], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x268b6], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26900], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x2694a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26994], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - *... a dalších 5 elementů.*
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 6180.28 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 echoblock_2790_1200_fasets_only_speed_500.VCF
- **Predikce času:** 0 min 42 s (na základě celkové dráhy 13740.28 mm)
- **Počet uložených elementů/instrukcí:** 10
### Ukázka elementů (prvních 10):
  - Geometrie: Line [@ 0x26912], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x2695c], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x269a6], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x269f0], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26a3a], Body/Uzly: 2, Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26b2b], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26b75], Body/Uzly: 2, Délka dráhy: 1200.0 mm
  - Geometrie: Line [@ 0x26bbf], Body/Uzly: 2, Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c09], Body/Uzly: 2, Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26c53], Body/Uzly: 2, Délka dráhy: 0.0 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 500 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace): 13740.28 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: 6.0 mm)
  - **Vrstva 2:** Rychlost 500 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 0.0 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 circle_02.VCF
- **Predikce času:** 0 min 56 s (na základě celkové dráhy 6283.19 mm)
- **Počet uložených elementů/instrukcí:** 2
### Ukázka elementů (prvních 10):
  - Geometrie: Circle [@ 0x26664], Body/Uzly: 4, Délka dráhy: 3141.59 mm
  - Geometrie: Circle [@ 0x2687d], Body/Uzly: 4, Délka dráhy: 3141.59 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 6283.19 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

## 📄 circle_01.VCF
- **Predikce času:** 0 min 35 s (na základě celkové dráhy 3141.59 mm)
- **Počet uložených elementů/instrukcí:** 1
### Ukázka elementů (prvních 10):
  - Geometrie: Circle [@ 0x26664], Body/Uzly: 4, Délka dráhy: 3141.59 mm
### Vrstvy (Fyzikální parametry):
  - **Vrstva 1:** Rychlost 150 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace): 3141.59 mm
    - Tool feeding (Počet: 0, H1: 0.0 mm, H2: 8.0 mm)

