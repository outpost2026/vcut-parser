// =========================================================================
// KONFIGURACE (Zde musíte vložit SKUTEČNÉ ID SLOŽKY, nikoliv tabulky!)
// =========================================================================
const GDRIVE_FOLDER_ID = "1AHA4YgvUQM7QQsE4fvxnWKlNqYl3Xac7"; 

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('⚙️ Moodpasta Výroba')
    .addItem('🔍 Aktualizovat složky a časy CNC', 'syncCncData')
    .addToUi();
}

function syncCncData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("dev_sandbox");
  
  if (!sheet) {
    SpreadsheetApp.getUi().alert("Chyba: List 'dev_sandbox' nebyl v tabulce nalezen!");
    return;
  }
  
  // 1. OBRANNÝ KROK: Kontrola, zda uživatel nezadal omylem ID tabulky namísto složky
  if (GDRIVE_FOLDER_ID === ss.getId() || GDRIVE_FOLDER_ID.includes("docs.google.com")) {
    SpreadsheetApp.getUi().alert("❌ KRITICKÁ CHYBA:\nV proměnné GDRIVE_FOLDER_ID máte vloženo ID nebo URL samotné tabulky.\n\nMusíte do ní vložit ID složky z Google Drive (otevřete složku 'Timestamps_zakazky' v prohlížeči a zkopírujte kód na konci URL za /folders/).");
    return;
  }
  
  // 2. OBRANNÝ KROK: Bezpečné otevření složky přes Try-Catch (prevence pádu celého skriptu)
  let mainFolder;
  try {
    mainFolder = DriveApp.getFolderById(GDRIVE_FOLDER_ID);
  } catch (error) {
    SpreadsheetApp.getUi().alert("❌ CHYBA GOOGLE DRIVE:\n\nSkript nedokázal najít nebo otevřít složku pod zadaným ID. Tabulka nebyla upravena.\n\nDetaily chyby: " + error.message);
    return;
  }
  
  const data = sheet.getDataRange().getValues();
  
  // Striktní definice indexů sloupců (A=0, F=5, G=6, H=7, I=8, J=9, K=10, L=11)
  const zakazkaCol = 0;       // Sloupec A (Číslo objednávky)
  const statusCol = 5;        // Sloupec F (6. sloupec v tabulce) -> Stav VCF
  const linkCol = 6;          // Sloupec G (7. sloupec v tabulce) -> Odkaz do složky pro CNC operátora
  const timeCol = 7;          // Sloupec H (8. sloupec v tabulce) -> Predikovaný čas řezu
  const noteCol = 8;          // Sloupec I (9. sloupec v tabulce) -> Technologická poznámka (Vector 3)
  const activeLayersCol = 9;  // Sloupec J (10. sloupec) -> Počet aktivních vrstev (v3)
  const vCutBothLengthCol = 10; // Sloupec K (11. sloupec) -> Celková délka řezu V-cut oboustranně (v3)
  const vibreLengthCol = 11;  // Sloupec L (12. sloupec) -> Celková délka aktivního oscilačního nože (v3)

  let updatedCount = 0;
  let foldersFoundCount = 0;
  let totalPredictedSeconds = 0; // Pro dispečerskou agregaci kapacitního plánování (Vector 4)
  
  // Smyčka přes řádky (vynecháváme první řádek s hlavičkou)
  for (let i = 1; i < data.length; i++) {
    const orderId = String(data[i][zakazkaCol]).trim();
    if (!orderId || orderId === "" || orderId.toLowerCase() === "objednávka" || orderId.toLowerCase() === "číslo objednávky") continue; 
    
    let statusCell = sheet.getRange(i + 1, statusCol + 1);
    let linkCell = sheet.getRange(i + 1, linkCol + 1);
    let timeCell = sheet.getRange(i + 1, timeCol + 1);
    let noteCell = sheet.getRange(i + 1, noteCol + 1);
    let activeLayersCell = sheet.getRange(i + 1, activeLayersCol + 1);
    let vCutBothLengthCell = sheet.getRange(i + 1, vCutBothLengthCol + 1);
    let vibreLengthCell = sheet.getRange(i + 1, vibreLengthCol + 1);
    
    // Formátování čísla zakázky pro složky cislovane_adresare (např. "1" -> "0001")
    let paddedOrderId = orderId;
    if (/^\d+$/.test(orderId)) {
      paddedOrderId = ("0000" + orderId).slice(-4);
    }
    
    // VEKTOR 1: Rychlé vyhledávání podle složky (decoupled folder search) namísto procházení všech souborů
    let folderQuery = "title contains '" + paddedOrderId + "' and trashed = false";
    let folders;
    try {
      folders = DriveApp.searchFolders(folderQuery);
    } catch (e) {
      Logger.log("Chyba při vyhledávání složky pro zakázku " + paddedOrderId + ": " + e.message);
      statusCell.setValue("⚠️ Chyba hledání").setBackground("#f4cccc");
      continue;
    }
    
    let targetFolder = null;
    while (folders.hasNext()) {
      let folder = folders.next();
      targetFolder = folder;
      break;
    }
    
    if (!targetFolder) {
      statusCell.setValue("❌ Složka chybí").setBackground("#f4cccc");
      linkCell.setValue("-").setBackground(null);
      timeCell.setValue("-").setBackground(null);
      noteCell.setValue("-").setBackground(null);
      activeLayersCell.setValue("-").setBackground(null);
      vCutBothLengthCell.setValue("-").setBackground(null);
      vibreLengthCell.setValue("-").setBackground(null);
      continue;
    }
    
    foldersFoundCount++;
    const folderUrl = targetFolder.getUrl();
    
    // Sloupec G (7. sloupec): Odkaz přímo na pracovní složku na GDrive pro operátora
    linkCell.setValue(`=HYPERLINK("${folderUrl}"; "📂 Otevřít složku ${paddedOrderId}")`).setBackground("#d9ead3");
    
    // VEKTOR 2: Architektura distribuovaných reportů (Načtení sidecar JSONů v17.4)
    const files = targetFolder.getFiles();
    const reportsByVcf = {};
    let reportsCount = 0;
    
    while (files.hasNext()) {
      const file = files.next();
      const name = file.getName();
      
      if (name.toLowerCase().endsWith("_report.json")) {
        try {
          let nameNoExt = name.substring(0, name.toLowerCase().lastIndexOf("_report.json"));
          let lastUnderscore = nameNoExt.lastIndexOf("_");
          
          if (lastUnderscore !== -1) {
            let timestamp = nameNoExt.substring(lastUnderscore + 1); // "YYYYMMDD_HHMMSS"
            let vcfKey = nameNoExt.substring(0, lastUnderscore); // "[folder_name]_[vcf_base_name]"
            
            if (!reportsByVcf[vcfKey] || timestamp > reportsByVcf[vcfKey].timestamp) {
              reportsByVcf[vcfKey] = {
                file: file,
                timestamp: timestamp
              };
            }
          }
        } catch (e) {
          Logger.log("Chyba parsování názvu reportu " + name + ": " + e.message);
        }
      }
    }
    
    if (Object.keys(reportsByVcf).length === 0) {
      statusCell.setValue("⚠️ Chybí report").setBackground("#fff2cc");
      timeCell.setValue("⚠️ Neanalyzováno").setBackground("#fff2cc");
      noteCell.setValue("-").setBackground(null);
      activeLayersCell.setValue("-").setBackground(null);
      vCutBothLengthCell.setValue("-").setBackground(null);
      vibreLengthCell.setValue("-").setBackground(null);
      continue;
    }
    
    // Agregace všech unikátních nejnovějších reportů v daném adresáři (řeší Vektor 4)
    let totalSeconds = 0;
    let totalLength = 0.0;
    const combinedWarnings = [];
    const combinedTechNotes = [];
    let failSafeFlag = false;
    
    // Nové agregované metriky (v3):
    let activeLayersCount = 0;
    let totalVCutBothSideLength = 0;
    let totalVibrateCutterLength = 0;
    
    for (let vcfKey in reportsByVcf) {
      reportsCount++;
      const file = reportsByVcf[vcfKey].file;
      try {
        const content = file.getBlob().getDataAsString();
        const report = JSON.parse(content);
        
        if (report && report.erp_time_prediction) {
          totalSeconds += (report.erp_time_prediction.predicted_time_seconds || 0);
          totalLength += (report.erp_time_prediction.total_path_length_mm || 0.0);
        }
        if (report.fail_safe_flag) {
          failSafeFlag = true;
        }
        if (report.warnings) {
          report.warnings.forEach(w => {
            if (combinedWarnings.indexOf(w) === -1) combinedWarnings.push(w);
          });
        }
        if (report.tech_notes) {
          report.tech_notes.forEach(tn => {
            if (combinedTechNotes.indexOf(tn) === -1) combinedTechNotes.push(tn);
          });
        }
        
        // Hloubková extrakce fyzikálních vrstev z kompletního JSONu (v3):
        if (report.layers) {
          report.layers.forEach(layer => {
            if (layer.is_output_yes) {
              activeLayersCount++;
              
              if (layer.cutter_type === "V-slot" && layer.direction === "Cut both side") {
                totalVCutBothSideLength += (layer.total_cut_length_mm || 0);
              } else if (layer.cutter_type === "Vibrate cutter" || layer.cutter_type === "Vibrate cut") {
                totalVibrateCutterLength += (layer.total_cut_length_mm || 0);
              }
            }
          });
        }
      } catch (e) {
        Logger.log("Chyba čtení JSONu " + file.getName() + " v " + paddedOrderId + ": " + e.message);
      }
    }
    
    // VEKTOR 5: Fail-Safe mechanismus (detekce neznámé verze VCF)
    if (failSafeFlag) {
      statusCell.setValue("⚠️ Verze VCF nepodporována").setBackground("#f4cccc");
      timeCell.setValue("⚠️ Neanalyzováno").setBackground("#f4cccc");
      noteCell.setValue("⚠️ Detekována nová verze VCF – vyžadován zásah vývojáře").setBackground("#fff2cc");
      activeLayersCell.setValue("-").setBackground(null);
      vCutBothLengthCell.setValue("-").setBackground(null);
      vibreLengthCell.setValue("-").setBackground(null);
      continue;
    }
    
    // Úspěšná synchronizace
    statusCell.setValue("✅ OK").setBackground("#d9ead3");
    
    // Sloupec H (8. sloupec): Nastavení predikovaného času řezu (zformátovaný agregovaný čas)
    timeCell.setValue(formatGasTime(totalSeconds)).setBackground("#cfe2f3");
    
    // Připočtení sekund pro celkový sumář plánování směn (Vektor 4)
    totalPredictedSeconds += totalSeconds;
    
    // VEKTOR 3: Propisování technologických varování (Flagy pro operátory) do sloupce I (9. sloupec)
    if (combinedTechNotes.length > 0) {
      const techNotesStr = combinedTechNotes.join(", ");
      noteCell.setValue(techNotesStr).setBackground("#fff2cc"); // Žluté zvýraznění anomálie
    } else {
      noteCell.setValue("Bez poznámek").setBackground(null);
    }
    
    // NOVÉ SLOUPCE (v3): Zápis hloubkových technologických metrik pro plánování kapacity a opotřebení
    activeLayersCell.setValue(activeLayersCount).setBackground("#cfe2f3");
    vCutBothLengthCell.setValue(Math.round(totalVCutBothSideLength * 10) / 10).setBackground("#cfe2f3");
    vibreLengthCell.setValue(Math.round(totalVibrateCutterLength * 10) / 10).setBackground("#cfe2f3");
    
    updatedCount++;
  }
  
  // VEKTOR 4: Dashboard kapacitního plánování - výpočet celkového strojního času pro dispečera
  const hours = Math.floor(totalPredictedSeconds / 3600);
  const minutes = Math.floor((totalPredictedSeconds % 3600) / 60);
  const seconds = totalPredictedSeconds % 60;
  
  let capacitySummary = "";
  if (hours > 0) {
    capacitySummary = hours + " h " + minutes + " min " + seconds + " s";
  } else {
    capacitySummary = minutes + " min " + seconds + " s";
  }
  
  // Zobrazení přehledného oznámení dispečerovi
  const alertMsg = `🚀 Moodpasta Výroba (v3): Data byla úspěšně aktualizována.\n\n` +
                   `📂 Nalezeno zakázkových složek: ${foldersFoundCount}\n` +
                   `📊 Úspěšně synchronizováno zakázek: ${updatedCount}\n\n` +
                   `⏱️ CELKOVÝ STROJNÍ ČAS NAČTENÝCH ZAKÁZEK (Kapacitní plánování): ${capacitySummary}\n` +
                   `(Tento čas představuje čistou dobu řezu plotru na základě kinematického modelu a slouží jako podklad pro plánování směny.)`;
                   
  SpreadsheetApp.getUi().alert(alertMsg);
}

// Pomocná funkce pro formátování času v Apps Scriptu
function formatGasTime(seconds) {
  if (seconds <= 0) return "0 s";
  if (seconds < 60) return seconds + " s";
  let minutes = Math.floor(seconds / 60);
  let secs = seconds % 60;
  if (minutes < 60) {
    return minutes + " min " + secs + " s";
  }
  let hours = Math.floor(minutes / 60);
  let mins = minutes % 60;
  return hours + " h " + mins + " min " + secs + " s";
}
