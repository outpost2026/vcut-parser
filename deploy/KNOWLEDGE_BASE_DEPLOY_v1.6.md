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
4. Priradi HTTPS URL ve formatu: {service}-{project_number}.{region}.run.app
5. Stara revize zustava (lze se k ni vratit — rollback)

### Cloud Run URL format:
- Stary format: {service}-{hash}-{region}.a.run.app (napr. jdpi45qekq-ew.a.run.app)
- NOVY format: {service}-{project_number}.{region}.run.app (napr. 537446704644.europe-west1.run.app)
- Nas projekt pouziva NOVY format (videt na miner-orchestrator)

### Proc region europe-west1 (Belgie) a ne europe-west3 (Frankfurt):
- Projekt PrahaScrapersV1 ma VSECHNY sluzby v europe-west1
- Scheduler joby, Cloud Functions, Cloud Run — vse v europe-west1
- Region nelze mixovat — Cloud Run a Scheduler musi byt ve stejnem regionu

## CO SE STANE PO DEPLOYI (PROVOZNI REALITA)

### Cold start:
- min-instances=0 znamena: po obdobi neaktivity (~15 min) se kontejner vypne
- Prvni request po vypnuti trva 5-10s (Streamlit + Python init)
- Dalsi requesty jsou instantni
- PRO DEMO je toto v poradku. Pro produkci by bylo min-instances=1.

### Streamlit na Cloud Run:
- Streamlit pouziva WebSocket pro real-time komunikaci s prohlizecem
- Cloud Run WebSocket podporuje nativne
- Kazdy uzivatel ma vlastni Streamlit session v ramci jedne instance
- Pri max-instances=1 sdili vsichni uzivatele jeden kontejner

### Upload VCF souboru:
- Soubory se zpracovavaji v RAM (ne na disk)
- Cloud Run disk je efemerni — po restartu kontejneru zmizi
- Max velikost HTTP requestu: 32 MB (Cloud Run limit)
- VCF soubory z Moodpasty: typicky 100-500 KB — bez problemu

### Omezeni max-instances=1:
- Pro 3 lidi z Moodpasty — naprosto dostacujici
- Pri vice uzivatelich zvysit na max-instances=3 nebo vice
- KAZDA instance ma vlastni Python proces → vlastni pamet

## BEZPECNOSTNI UVEDOMENI (co dashboard obsahuje)

Dashboard ve stavu v1.6-demo obsahuje tyto citlive udaje Moodpasty:
- Produktove nazvy: Echoblock, Savanna, Capexus
- Vyrobni parametry: H2 rozsahy, fixacni pravidla, sekvencni validace
- Cenovy model: 18.5 Kc/min, 420 Kc/m²
- Referencni firma: Moodpasta, Wynwood s.r.o.

Proto je NASADENA AUTENTIZACE (auth gate v app.py).
Bez hesla se dashboard neotevre.
Heslo je v tele follow-up emailu → znaji ho jen ucastnici schuzky.

PRO PRODUKCNI NASAZENI je nutne prejit na:
- GCP Identity-Aware Proxy (IAP) misto hesla v kodu
- Nebo Cloud Run s --no-allow-unauthenticated + service account key

## JAK SMazat / AKTUALIZOVAT SLUZBU

# Smazat sluzbu (uplne odstraneni):
gcloud run services delete vcf-parser-demo --region europe-west1 --quiet

# Aktualizovat existujici sluzbu (novy image):
gcloud run deploy vcf-parser-demo \
  --image europe-west1-docker.pkg.dev/project-4ac30110-41b1-4783-a5d/moodpasta/vcf-parser:v1.7 \
  --region europe-west1

# Vypsat vsechny revize:
gcloud run revisions list --service vcf-parser-demo --region europe-west1

# Rollback na predchozi revizi:
gcloud run services update-traffic vcf-parser-demo --to-revisions=<REVISION_NAME>=100 --region europe-west1

## KONTROLNI SEZNAM PO DEPLOYI

- [ ] URL funguje: https://vcf-parser-demo-537446704644.europe-west1.run.app
- [ ] Auth gate se zobrazi (vyzaduje heslo)
- [ ] Po zadani hesla "moodpasta-demo-2026" se otevre dashboard
- [ ] 3 demo VCF soubory jsou videt (fluenz_l, pernerka_dark_knight_12mm, 1ks)
- [ ] Upload vlastniho VCF funguje
- [ ] CSV export pro Odoo funguje
- [ ] Odkaz a heslo odeslany v follow-up emailu Františkovi a Jakubovi

## PRIPRAVA NA DALSI VERZI (v1.7+)

Po uspesnem deployi a zpetne vazbe od Moodpasty:
1. Pridat vice demo VCF souboru (na zaklade feedbacku)
2. Zvazit konfiguracni soubor misto hardcoded hodnot (app_config.json)
3. Pridat logovani (Cloud Logging je automaticky pro Cloud Run — stderr/stdout)
4. Nastavit billing alert (pokud uz neni)
