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
  
  // Pokud složka existuje, bezpečně načteme její data
  const folderUrl = mainFolder.getUrl();
  const files = mainFolder.getFiles();
  
  const fileList = [];
  let parsedJsonData = [];
  
  // 3. NAČTENÍ SOUBORŮ DO PAMĚTI (Fáze sběru dat)
  while (files.hasNext()) {
    const file = files.next();
    const name = file.getName();
    
    if (name.toLowerCase().endsWith('.vcf')) {
      fileList.push({ name: name, lastUpdated: file.getLastUpdated() });
    } else if (name.toLowerCase().endsWith('.json')) {
      try {
        parsedJsonData = JSON.parse(file.getBlob().getDataAsString());
      } catch (e) {
        Logger.log("Chyba při čtení JSONu: " + e.message);
      }
    }
  }
  
  // 4. ZPRACOVÁNÍ DAT TABULKY (Zápis)
  const data = sheet.getDataRange().getValues();
  
  // Striktní definice indexů sloupců (A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7)
  const zakazkaCol = 0; // Sloupec A (Číslo objednávky)
  const statusCol = 5;  // Sloupec F (6. sloupec v tabulce) -> Stav VCF
  const linkCol = 6;    // Sloupec G (7. sloupec v tabulce) -> Odkaz do složky pro CNC operátora
  const timeCol = 7;    // Sloupec H (8. sloupec v tabulce) -> Predikovaný čas řezu
  
  // Smyčka přes řádky (vynecháváme první řádek s hlavičkou)
  for (let i = 1; i < data.length; i++) {
    const orderId = String(data[i][zakazkaCol]).trim();
    if (!orderId || orderId === "") continue; 
    
    // Vyhledáme soubory patřící k této zakázce
    let matchedFiles = fileList.filter(f => f.name.includes(orderId));
    
    let statusCell = sheet.getRange(i + 1, statusCol + 1);
    let linkCell = sheet.getRange(i + 1, linkCol + 1);
    let timeCell = sheet.getRange(i + 1, timeCol + 1);
    
    if (matchedFiles.length === 0) {
      // Pokud soubory na disku chybí, zapíšeme varování
      statusCell.setValue("❌ Soubor chybí").setBackground("#f4cccc");
      linkCell.setValue("-").setBackground(null);
      timeCell.setValue("-").setBackground(null);
    } else {
      // Soubory nalezeny -> zapíšeme stav, vyrobíme odkaz na složku a vytáhneme čas
      statusCell.setValue(`✅ ${matchedFiles.length}× nalezeno`).setBackground("#d9ead3");
      
      // Sloupec G (7. sloupec): Odkaz přímo na pracovní složku na GDrive
      linkCell.setValue(`=HYPERLINK("${folderUrl}"; "📂 Otevřít složku ${orderId}")`).setBackground("#d9ead3");
      
      // Sloupec H (8. sloupec): Párování času z agregovaného JSONu
      matchedFiles.sort((a, b) => b.lastUpdated - a.lastUpdated);
      const latestFileName = matchedFiles[0].name;
      const jsonRecord = parsedJsonData.find(item => item.filename === latestFileName);
      
      if (jsonRecord && jsonRecord.erp_time_prediction) {
        timeCell.setValue(jsonRecord.erp_time_prediction.predicted_time_formatted).setBackground("#cfe2f3");
      } else {
        timeCell.setValue("⚠️ Neanalyzováno").setBackground("#fff2cc");
      }
    }
  }
  
  SpreadsheetApp.getUi().alert("🚀 Moodpasta Výroba: Data byla úspěšně aktualizována bez chyb.");
}