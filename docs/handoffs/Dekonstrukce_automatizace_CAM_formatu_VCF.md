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
  - **Tool feeding:** Počet, Start height (H1), End height (H2).
  - **V-Slot specifika:** Směr (Left/Right/Both), V-slot width compensation, Starting/Ending extensions.

## 3. Aktuální stav (Roadmapa V10)
Momentálně disponujeme parserem, který z binárních souborů `.VCF` čte veškeré technologické parametry potřebné pro nastavení stroje. 

**Pro příští iteraci (V10) je připraven pivotní workflow:**
- **Cíl:** Exaktní výpočet času namísto empirických odhadů.
- **Implementační strategie:**
  - Diferenciální analýza souborů s různým počtem vrstev ukázala, že geometrická data jsou uložena v prvních 50 kB souboru, separována podle barevných příznaků vrstev.
  - V10 bude muset implementovat **"Opcode Geometry Decoder"**, který projde tuto geometrickou část, přiřadí souřadnice konkrétním barevným kódům (vrstvám) a vypočítá skutečnou délku dráhy (Euklidovská vzdálenost mezi body) pro každou vrstvu.

Projekt je nyní technicky připraven pro finální implementaci geometrického dekodéru, který uzavře cyklus automatizace ERP.
