from __future__ import annotations

from pathlib import Path
import pandas as pd


# Versuch, Ihr Logging zu laden – falls das Skript standalone läuft,
# fangen wir das ab, damit kein Importfehler entsteht.
try:
    from ..utils.logging_setup import logger
except ImportError:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


class DataReader:
    """Klasse zum Einlesen und Schreiben von Excel-Dateien."""

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        logger.info(f"Initialisiere DataReader mit Datei: {self.input_file}")

    def read_excel(self, sheet_name: str | int = 0, header: int = 0, usecols=None, skiprows=None, nrows=None) -> pd.DataFrame:
        """Liest ein bestimmtes Tabellenblatt und optional einen Bereich aus der Excel-Datei ein."""
        if not self.input_file.exists():
            raise FileNotFoundError(
                f"Die Datei {self.input_file} wurde nicht gefunden."
            )

        logger.info(f"Lese Blatt '{sheet_name}' aus Datei: {self.input_file.name}")

        # Parameter usecols, skiprows und nrows an pd.read_excel übergeben
        df = pd.read_excel(
            self.input_file, 
            sheet_name=sheet_name, 
            header=header, 
            usecols=usecols, 
            skiprows=skiprows, 
            nrows=nrows
        )
        return df

    def write_excel(
        self,
        df: pd.DataFrame,
        output_file: str | Path,
        sheet_name: str = "Auswertung",
    ):
        """Schreibt einen DataFrame in eine neue Excel-Datei."""
        output_path = Path(output_file)
        logger.info(
            f"Schreibe Daten in Datei: {output_path.name} (Blatt: {sheet_name})"
        )
        df.to_excel(output_path, sheet_name=sheet_name, index=False)


# --- Hauptprogramm ---
if __name__ == "__main__":
    # 1. Pfade automatisch relativ zum Skript-Ordner definieren
    script_dir = Path(__file__).resolve().parent
    input_file = script_dir / "Ter Apel_FAC Summary.xlsx"
    output_file = script_dir / "Ter Apel_FAC Summary_neu.xlsx"

    # 2. Reader-Instanz erzeugen
    reader = DataReader(input_file)

    # 3. Gewünschtes Tabellenblatt einlesen
    # Hinweis: Bei Ihrer "Summary"-Struktur in der Ter Apel Datei fängt der Header evtl.
    # erst in einer bestimmten Zeile an (z.B. header=2 oder header=3).
    # Hier standardmäßig Sheet 'Summary' geladen:
    df = reader.read_excel(sheet_name="Summary")

    # --- Optional: Daten bearbeiten / berechnen ---
    # Beispiel (falls die Spaltennamen exakt so vorliegen):
    # if 'Pout' in df.columns and 'Psim' in df.columns:
    #     df['Abweichung_%'] = (df['Pout'] / df['Psim']) * 100

    # 4. In neue Excel-Datei ausgeben
    reader.write_excel(df, output_file, sheet_name="Auswertung")

    print(f"Erfolgreich abgeschlossen! Neue Datei: {output_file}")