# 🔬 V13.1 Report: Grouping Mode Fix

Tato verze opravuje klíčový neduh VCutWorks: pokud uživatel v GUI sloučí elementy (Group), CAM je nepřevede na Polygon, ale zahodí jejich signatury a sbalí je jako zřetězené čisté čáry. Parser se nyní adaptoval na tento kompresní formát a umí iterovat skrze sloučené geometrie (V-slot dráhy).

## 📄 manchester_vse_01.VCF
- **Predikce času:** 7 min 17 s (na základě dráhy: **126726.11 mm**)
- **Počet uložených elementů/instrukcí:** 111
### Ukázka elementů (prvních 15):
  - Geometrie: Line [@ 0x268f6], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26940], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26940_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x2698a], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26a31], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26a7b], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26a7b_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26ac5], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26b6c], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26bb6], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26bb6_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c00], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - *... a dalších 96 elementů.*
### Vrstvy (Fyzikální parametry vč. V-Slot detailů z V9):
  - **Vrstva 1:** Rychlost 400 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace celku): 126726.11 mm
    - Tool feeding (Počet: 1, H1: 3.0 mm, H2: 7.0 mm)
    - Směr řezu (Direction): Cut both side
    - Starting Extension: 10.0 mm
    - Ending Extension: 10.0 mm
    - V-slot Width Comp: 0.0 mm
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace celku): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

## 📄 manchester_vse_03.VCF
- **Predikce času:** 7 min 17 s (na základě dráhy: **126726.11 mm**)
- **Počet uložených elementů/instrukcí:** 114
### Ukázka elementů (prvních 15):
  - Geometrie: Line [@ 0x26911], Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x2695b], Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x269a5], Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26a39], Délka dráhy: 0.0 mm
  - Geometrie: Line [@ 0x26ade], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26b28], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26b28_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26b72], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26c19], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c63], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26c63_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26cad], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26d54], Délka dráhy: 2790.0 mm
  - *... a dalších 99 elementů.*
### Vrstvy (Fyzikální parametry vč. V-Slot detailů z V9):
  - **Vrstva 1:** Rychlost 400 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace celku): 126726.11 mm
    - Tool feeding (Počet: 1, H1: 3.0 mm, H2: 7.0 mm)
    - Směr řezu (Direction): Cut both side
    - Starting Extension: 10.0 mm
    - Ending Extension: 10.0 mm
    - V-slot Width Comp: 0.0 mm
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace celku): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

## 📄 manchester_vse_02.VCF
- **Predikce času:** 14 min 19 s (na základě dráhy: **253452.21 mm**)
- **Počet uložených elementů/instrukcí:** 222
### Ukázka elementů (prvních 15):
  - Geometrie: Line [@ 0x268f6], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26940], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26940_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x2698a], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26a31], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26a7b], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26a7b_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26ac5], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - Geometrie: Line [@ 0x26b6c], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26bb6], Délka dráhy: 90.14 mm
✨ Geometrie: Reconstructed Edge [@ 0x26bb6_recon], Délka dráhy: 2790.0 mm
  - Geometrie: Line [@ 0x26c00], Délka dráhy: 0.0 mm
✨ Geometrie: Reconstructed Edge [@ End_of_Group_recon], Délka dráhy: 90.14 mm
  - *... a dalších 207 elementů.*
### Vrstvy (Fyzikální parametry vč. V-Slot detailů z V9):
  - **Vrstva 1:** Rychlost 400 mm/s | Nástroj: V-slot
    - Délka dráhy vrstvy (zatím fixní agregace celku): 253452.21 mm
    - Tool feeding (Počet: 1, H1: 3.0 mm, H2: 7.0 mm)
    - Směr řezu (Direction): Cut both side
    - Starting Extension: 10.0 mm
    - Ending Extension: 10.0 mm
    - V-slot Width Comp: 0.0 mm
  - **Vrstva 2:** Rychlost 200 mm/s | Nástroj: Vibrate cutter
    - Délka dráhy vrstvy (zatím fixní agregace celku): 0.0 mm
    - Tool feeding (Počet: 1, H1: 0.0 mm, H2: -0.5 mm)

