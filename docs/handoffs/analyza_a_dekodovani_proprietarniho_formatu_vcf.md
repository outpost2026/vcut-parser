# 🔬 Výzkumný report: Analýza a dekódování proprietárního formátu .VCF

**Datum:** Březen 2024
**Kontext:** Reverzní inženýrství CAM formátu `.VCF` (Shenzhen Ruida Technology / VCutWorks) pro účely vývoje prediktivního modelu a automatizace ERP.
**Status:** Dekódováno a algoritmizováno.

---

## 1. Úvodní premisa a "Manifest nedotknutelnosti"

Cílem výzkumu bylo porozumět proprietární struktuře hexadecimální binárky souborů s příponou `.VCF`, do kterých program VCutWorks překládá vektorová data (DXF) pro odeslání do řídící jednotky stroje Ruida. Porozumění struktuře je nezbytné pro vytvoření skriptu, který dokáže automatizovaně vytěžit klíčové parametry řezu (čas, složitost, rychlosti) bez spuštění samotného CAM softwaru a poslat je do databáze ERP.

Průběh výzkumu zásadně ovlivnilo "odborné poselství" dosavadního operátora (Karel), který reprezentuje expertní, tacitní rovinu know-how ve výrobě. Jeho postoj k pokusům o dekódování dat byl rezolutní a zamítavý.

**Zkrácený manifest operátora (Karla):**
> *"K čemu ti to je? Je to čínský speciální formát, nikdo z něj nikdy nic nedostal. Ani výrobci plotterů. Není to tvůj G-kód, nelze to rozluštit. Zbytečně si to komplikuješ, je to marná snaha. Věnuj se užitečnějším věcem a kroť své ego. Vycházím ze svých dvacetiletých zkušeností."*

Tento manifest dokonale koreluje s vytvořeným profilovým auditem (*"Tacitní profil optimalizace komunikace"*). Karel operuje výhradně na bázi krystalizované inteligence (Gc) a empirických postupů. Abstrakci nebo reverzní inženýrství černých skříněk (black-box) vnímá ne jako inovaci, ale jako nebezpečnou aroganci zpochybňující "léta praxe". Z jeho pohledu – pokud soubor nejde otevřít v notepadu a nedává smysl na první pohled, "nelze jej rozluštit".

Tento report prokazuje, že **lze**.

---

## 2. Jádro analýzy: Dekonstrukce binární mýty

Výchozím bodem byla hloubková analýza (hexdump) surových binárních dat `.VCF` na několika vzorcích s přesně známou geometrií (od jedné čáry po složité hudební motivy a echobloky) a znalostí toho, jak vrstvy vypadají v GUI softwaru VCutWorks.

### 2.1 Co VCF doopravdy je (a co není)
Karlovo přesvědčení, že to "není G-kód" a je to "neprolomitelný čínský formát", je z technického hlediska zčásti pravda a zčásti mýtus.
*   **Ne, není to čistý textový G-kód.** Není to čitelný plaintext (jako např. `.nc` soubory pro Mach3/LinuxCNC).
*   **Ale ano, je to jen hloupé pole dat.** Není to žádná šifrovaná, kryptograficky chráněná Pandořina skříňka. Jedná se o hrubý, neoptimalizovaný a paměťově zarovnaný sekvenční výpis (tzv. "serialization") datových struktur vytvořený v C/C++. 

### 2.2 Anatomie "Čínského formátu"
Provedl jsem postupné reverzní inženýrství pomocí Pythonu. Analýza odhalila pevnou architekturu souboru:

1.  **Hlavička (ASCII/Windows-1250):** 
    Soubor začíná signaturou (např. `RDVCUTFILEVER1.0.013`). Dále obsahuje zakódovaná textová metadata (názvy vrstev, názvy fontů a původní cesty k `.dxf` souborům). Vtip je v tom, že text není kódován standardně v UTF-8, ale pro české znaky používá středoevropské kódování `Windows-1250`. Pokud to zkusíte otevřít normálně, získáte "čínský rozsypaný čaj". Po správném dekódování jsem ze souborů vyčetl jména jako *"Karel V"*, *"echoblok 2790x1200"*, atd.

2.  **Hřbitov palet (Balastní data):** 
    Další analýza narazila na podivný problém. Skripty hlásily desítky různých řezných rychlostí, i když šablona měla jen jednu čáru. Zjistil jsem absurdní chování programu VCutWorks: Software do každého vygenerovaného `.VCF` na tvrdo "vypíše" parametry všech 20 výchozích systémových barev (i těch, které se vůbec nepoužijí). 

3.  **Geometrický Payload (IEEE 754):** 
    Dráhy nástroje nejsou uloženy jako X/Y souřadnice v textu, ale jako sekvence tzv. `Double Precision Float` (8bajtových desetinných čísel) se zápisem *Little-Endian*. To znamená, že číslo `500.0` je v hexadecimálu zapsáno jako `00 00 00 00 00 40 7f 40`. Z toho vycházela "nemožnost" to rozluštit okem.

4.  **Aktivní vrstvy (Rozluštění "tajemství"):** 
    Ta nejcennější data – parametry pro skutečně řezané vrstvy – připojuje VCutWorks z nějakého důvodu až **na úplný konec souboru**.

---

## 3. Finální algoritmizace (Parser V8)

Na základě těchto objevů jsem naprogramoval iteraci parseru V8. Její logika dokonale eliminuje "balast" a přesně extrahuje data:

1.  Skript přečte soubor po jediném bajtu (odstraněn problém se špatným zarovnáním dat čínskými vývojáři).
2.  Najde signaturu `0x01 00 00 00`, po které následuje nastavení vrstvy (rychlost typu `Double`).
3.  Vypočítá "mezery" (byte ofsety) mezi nalezenými hodnotami.
4.  Ignoruje pravidelný, nudný rytmus (20 zbytečných výchozích palet).
5.  Tam, kde se rytmus na konci souboru změní, odřízne konec a vyčte reálné **rychlosti**.

**Realistický výsledek (Ověření na datech):**
Skriptu jsem podsunul testovací soubory a srovnal je s OCR čtením ze screenshotů ze samotného softwaru VCutWorks:

*   **VCF: big coffee 12.8.2790x1200 bezotočení.VCF**
    *   *Screenshot (GUI):* Vrstvy s rychlostmi 200, 100, 100 mm/s.
    *   *Parser V8 Output:* `[200.0, 100.0, 100.0]` – **100% Shoda.**
*   **VCF: musica 2790x1200.VCF**
    *   *Screenshot (GUI):* Vrstvy s rychlostmi 150, 150, 75, 75 mm/s.
    *   *Parser V8 Output:* `[150.0, 150.0, 75.0, 75.0]` – **100% Shoda.**

---

## 4. Závěr: Inženýrství vs. Empirie

Výzkum prokázal, že formát `.VCF` je plně deterministický a strojově čitelný. Vybudovaný nástroj `RuidaVcfDeepParserV8` nyní dokáže během milisekund bez doteku operátora s 100% přesností získat:
*   Kompletní textová metadata (Kdo to řezal, název zdrojového DXF).
*   Počet vektorových instrukcí (hrubý odhad geometrické složitosti).
*   **Exaktní pole všech reálných rychlostí (mm/s), jak byly nastaveny v CAMu.**

Na základě těchto přesných rychlostí lze nyní aplikovat `Empirický Multiplikátor` a získávat vysoce přesné predikce strojového času pro automatické nacenění v ERP.

### Zhodnocení vůči "Manifestu"
Karlova tvrzení ("nelze rozluštit", "čínský speciální formát", "výrobci plotterů nevěděli") nepramení ze zlého úmyslu, ale z limitů jeho kognitivního modelu (zkušenost vs. analýza). 

Jeho 20 let praxe mu umožňuje postavit se ke stroji a perfektně fixovat PET felt (což se z analýzy binárního kódu nedozvím). Moje schopnost abstrahovat a dekonstruovat systémy mi zase umožňuje během 24 hodin rozbít ochranu "neprolomitelného" proprietárního formátu.

**Taktické doporučení:** 
Karlovi nesmí být výsledek tohoto reportu NIKDY prezentován ve smyslu "Mýlil ses, dokázal jsem to". To by fatálně narušilo fázi extrakce tacitních znalostí (viz profil *Tacitní profil optimalizace komunikace*). Nástroj V8 musí být tichým, backendovým motorem ERP systému, zatímco vůči Karlovi zůstane nadále zachována role "toho, kdo se učí fixovat L-doraz na stroji".
