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
$IMAGE_NAME = "europe-west1-docker.pkg.dev/$PROJECT_ID/moodpasta/vcf-parser:v1.6-demo"
$REPO_NAME = "moodpasta"
$SA = "537446704644-compute@developer.gserviceaccount.com"

# === KROK 0: Overeni predpokladu ===
Write-Host "`n[0/5] Overuji predpoklady..." -ForegroundColor Yellow

$gcloudCheck = gcloud auth list --format="value(account)" 2>$null
if (-not $gcloudCheck) {
    Write-Host "CHYBA: gcloud neni prihlaseno. Spust: gcloud auth login" -ForegroundColor Red
    exit 1
}
Write-Host "  gcloud prihlasen jako: $gcloudCheck" -ForegroundColor Green

gcloud config set project $PROJECT_ID --quiet 2>$null
Write-Host "  Projekt nastaven: $PROJECT_ID" -ForegroundColor Green

$dockerCheck = docker --version 2>$null
if (-not $dockerCheck) {
    Write-Host "CHYBA: Docker neni dostupny. Spust Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "  Docker: $dockerCheck" -ForegroundColor Green

# === KROK 1: Vytvoreni Artifact Registry repo (pokud neexistuje) ===
Write-Host "`n[1/5] Overuji Artifact Registry..." -ForegroundColor Yellow

$repoExists = gcloud artifacts repositories describe $REPO_NAME --location=$REGION --project=$PROJECT_ID 2>$null
if (-not $repoExists) {
    Write-Host "  Vytvarim repository '$REPO_NAME' v $REGION..." -ForegroundColor Yellow
    gcloud artifacts repositories create $REPO_NAME `
        --repository-format=docker `
        --location=$REGION `
        --project=$PROJECT_ID `
        --description="Moodpasta Parser container images" `
        --quiet
    Write-Host "  Repository vytvoreno." -ForegroundColor Green
} else {
    Write-Host "  Repository '$REPO_NAME' jiz existuje." -ForegroundColor Green
}

# === KROK 2: Pull source build do src/ adresare ===
Write-Host "`n[2/5] Overuji zdrojove soubory..." -ForegroundColor Yellow

$srcPath = "$PSScriptRoot\src"
if (-not (Test-Path "$srcPath\app.py")) {
    Write-Host "CHYBA: $srcPath\app.py neexistuje. Spust skript ve slozce GCP_Deploy_v1.6" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "$srcPath\vcf_parser_v20.py")) {
    Write-Host "CHYBA: vcf_parser_v20.py chybi" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "$srcPath\demo_data")) {
    Write-Host "CHYBA: demo_data/ chybi" -ForegroundColor Red
    exit 1
}
Write-Host "  app.py, vcf_parser_v20.py, Knowledge_base/, demo_data/ — OK" -ForegroundColor Green

# === KROK 3: Build Docker image ===
Write-Host "`n[3/5] Buildim Docker image..." -ForegroundColor Yellow
Write-Host "  Image: $IMAGE_NAME" -ForegroundColor Gray

docker build -t $IMAGE_NAME -f Dockerfile $srcPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "CHYBA: Docker build selhal." -ForegroundColor Red
    exit 1
}
Write-Host "  Image postaveno." -ForegroundColor Green

# === KROK 4: Push do Artifact Registry ===
Write-Host "`n[4/5] Pushuji do Artifact Registry..." -ForegroundColor Yellow

docker push $IMAGE_NAME

if ($LASTEXITCODE -ne 0) {
    Write-Host "CHYBA: Docker push selhal. Over gcloud auth configure-docker $REGION-docker.pkg.dev" -ForegroundColor Red
    Write-Host "  Spust: gcloud auth configure-docker europe-west1-docker.pkg.dev" -ForegroundColor Yellow
    exit 1
}
Write-Host "  Image pushnuto." -ForegroundColor Green

# === KROK 5: Deploy na Cloud Run ===
Write-Host "`n[5/5] Deployuji na Cloud Run..." -ForegroundColor Yellow

gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --min-instances 0 `
    --max-instances 1 `
    --service-account $SA `
    --project $PROJECT_ID `
    --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "CHYBA: Cloud Run deploy selhal." -ForegroundColor Red
    exit 1
}

# === VYSLEDNE URL ===
$url = "https://$SERVICE_NAME-$PROJECT_NUMBER.$REGION.run.app"
Write-Host "`n============================================" -ForegroundColor Green
Write-Host "  DEPLOY DOKONCEN!" -ForegroundColor Green
Write-Host "  URL:  $url" -ForegroundColor Cyan
Write-Host "  Heslo: moodpasta-demo-2026" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Green
Write-Host "`nPro overeni: gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'" -ForegroundColor Gray
Write-Host "Pro smazani:  gcloud run services delete $SERVICE_NAME --region $REGION --quiet" -ForegroundColor Gray
