# from __future__ import annotations
from pathlib import Path
from openpyxl import Workbook
import openpyxl
from datetime import datetime




from ..utils.logging_setup import logger
from ..api. basicdata import DataReader


class Pipeline:

    # =================================================================================================
    # Einlesen und Schreiben der Excel-Datei mit DataReader (aus basicdata.py)
    # =================================================================================================
    def process_summary(self):
        logger.info("Starte Excel-Verarbeitung mit DataReader...")
        
        # 1. Pfade relativ zum Skript-Ordner definieren
        script_dir = Path(__file__).resolve().parent.parent
        input_file = script_dir / "Ter Apel_FAC Summary.xlsx"

        from datetime import datetime

        # Aktuelles Datum und Uhrzeit holen
        jetzt = datetime.now()
        geformt = jetzt.strftime("%Y_%m_%d %H_%M_%S")
        output_file = script_dir / f"Ter Apel_FAC_Result_{geformt}.xlsx"

        # 2. Reader-Instanz erzeugen
        reader = DataReader(input_file)

        # 3. Tabellenblatt einlesen
        # Hier wird bestimmt, welche Daten aus dem Excel-File gelesen werden
        # def read_excel(self, sheet_name: str | int = 0, header: int = 0, usecols=None, skiprows=None, nrows=None)
        df = reader.read_excel(sheet_name="Summary", usecols="A:E", skiprows=1, nrows=29)

        # (Optional: Hier können Berechnungen / Transformationen am DataFrame 'df' stattfinden)

        # 4. In neue Excel-Datei ausgeben
        reader.write_excel(df, output_file, sheet_name="Auswertung")

        logger.info("Excel-Verarbeitung erfolgreich abgeschlossen -> Neue Datei: %s", output_file)



           
    # =================================================================================================
    # Ausführen der Pipeline basierend auf dem gewählten Modus
    # =================================================================================================
    def run(self, mode):
        logger.info("=====X START LOWCARBON PIPELINE X=====")
        if mode == "N":
            logger.info("Modus 'N' ausgewählt: Neue EXCEL-Datei erstellen.")
            # Abrufen der SITES aus SITEMARK und Erstellen der EXCEL-Datei zur Koordination
            self.process_summary()
        else:
            logger.error("Ungültige Auswahl.")
        logger.info("===== PIPELINE ABGESCHLOSSEN =====")



