from __future__ import annotations
import json
from openpyxl import Workbook
import openpyxl
from datetime import datetime
from ..api.client import SitemarkAPI
from ..api.sites import list_sites
from ..utils.logging_setup import logger
from ..api.punchlists import list_punchlist_items, count_weeks, count_status
from ..excel.workbook import create_excel_report
from ..excel.diagramm import DiagrammMaker
from ..excel.styles import ExcelStyles

from ..excel.macro import make_macro

class Pipeline:
    def __init__(self):
        self.api = SitemarkAPI()
        self.sites = []


    # =================================================================================================
    # Einlesen der SITES aus SITEMARK
    # =================================================================================================
    def fetch_sites(self):
        logger.info("Lade Sites aus Sitemark ...")
        sites = list_sites(self.api)
        # SUPPORT: if SELECTED_SITES is not defined in the global scope,
        # fall back to selecting all sites.
        selected_names = globals().get("SELECTED_SITES")
        if selected_names is None:
            self.sites = sites
        else:
            self.sites = [site for site in sites if site.get("name") in selected_names]
        logger.info("%s Sites ausgewählt.", len(self.sites))
        for site in self.sites:
            logger.info("Site ID=%s | Site Name=%s", site.get("id"), site.get("name"))

    # =================================================================================================
    # Ausgaben der SITES in EXCEL zur Koordination
    # wird aufgerufen, wenn der Modus "N" gewählt wurde, um die Sites in eine Excel-Datei zu exportieren.
    # =================================================================================================
    def export_sites(self):
        logger.info("Erzeuge Site-Auswahldatei ...")
        sites = list_sites(self.api)
        wb = Workbook()
        ws = wb.active
        ws.title = "Sites"
        ws.append(["Aktiv", "Site ID", "Site Name"])
        for site in sites:
            ws.append(["", site["id"], site["name"]])
        ws.column_dimensions["A"].width = 7
        ws.column_dimensions["B"].width = 15
        ws.column_dimensions["C"].width = 50
        wb.save("sites.xlsx")
        logger.info("%s Sites nach sites.xlsx geschrieben.", len(sites))

    # =================================================================================================
    # Einlesen der SITES aus EXCEL mit Markierungen zur Koordination
    # wird aufgerufen, wenn der Modus "M" gewählt wurde
    # =================================================================================================
    def load_selected_sites(self):
        wb = openpyxl.load_workbook("sites.xlsx")
        ws = wb["Sites"]
        self.sites = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            aktiv, site_id, site_name = row
            if str(aktiv).strip().upper() == "X":
                self.sites.append({
                    "id": site_id,
                    "name": site_name
                })
        logger.info(f"Sites markiert:                                       _______{len(self.sites):>10}")

    # =================================================================================================
    # Ausgabe in Excel mit Punchlist-Items für die markierten Sites
    # =================================================================================================
    def fetch_punchlists(self):
        wb, w_s = create_excel_report()

        all_items = []
        for index, site in enumerate(self.sites):
            items = list_punchlist_items(self.api, site["id"], site["name"])
            status_count = count_status(items)
            open_points = count_weeks(items, "Open Point")
            checklisten = count_weeks(items, "Checkliste")
            if False:
                logger.info("=" * 80)
                logger.info(f"{" " * 100}Site / markiert:{site["name"]:>20}  /  {len(items):>10}")

                logger.info(
                    "Open Points  : %s",
                    " | ".join(str(v) for v in open_points.values())
                )
                logger.info(
                    "Checklisten : %s",
                    " | ".join(str(v) for v in checklisten.values())
                )
                total_status = sum(status_count.values())
                logger.info(
                    "Statusübersicht : %s | Total : %s",
                    " | ".join(f"{k}: {v}" for k, v in status_count.items()), total_status
                )
            else:
                logger.info(f"{" " * 30}Site / markiert:{site["name"]:>20}  /  {len(items):>10}")

            count_runs = 0
            for item in items:
                count_runs += 1
                if count_runs % 10 == 0:
                    print(f"--> {count_runs}", end="\r", flush=True)
                w_s[0].append([
                    item.get("site_name"),
                    item.get("description"),
                    item.get("dataset_id"),
                    item.get("properties_VISIBLE_ID"),
                    item.get("properties_STATUS"),
                    item.get("typ"),
                    item.get("created_at"),
                    item.get("updated_at"),
                    item.get("status_icon"),
                ]
                + [item.get(f"{week:02d}_Woche") for week in range(15, -1, -1)]
                )


                # =================================================================================================
                # Seitenaufbau für 1. Seite
                # =================================================================================================
                row_nr = w_s[0].max_row
                w_s[0].cell(row=row_nr, column=6).number_format = "dd.mm.yyyy hh:mm"
                w_s[0].cell(row=row_nr, column=7).number_format = "dd.mm.yyyy hh:mm"


                # Nur die gerade eingefügte Zeile bearbeiten
                row = list(w_s[0].iter_rows( min_row=row_nr, max_row=row_nr ))[0]

                status_icon = row[8].value
                typ = row[5].value

                # Einfärben der Zellen in den Wochen-Spalten (10 bis 26) basierend auf dem Status-Icon und Typ
                for col in range(10, 27):
                    cell = row[col - 1]
                    if cell.value == "X" and status_icon == "►":
                        if typ == "Open Point":
                            cell.fill = ExcelStyles.LIGHT_BLUE_FILL
                        elif typ == "Checkliste":
                            cell.fill = ExcelStyles.LIGHT_YELLOW_FILL

            print(f"\033[2K\r", end="", flush=True)

            # TODO 260801 Name der Seiten setzen
            # =================================================================================================
            # Seitenaufbau für 2. Seite
            # =================================================================================================
            col_op = index + 3; row = 5
            w_s[1].cell(row=row, column=col_op, value=site["name"])
            # Wochenwerte darunter schreiben
            for offset_op, week in enumerate(range(15, -1, -1), start=1):
                w_s[1].cell( row=row + offset_op, column=col_op, value=open_points.get(f"{week:02d}_Woche", 0) )

            # =================================================================================================
            # Seitenaufbau für 3. Seite
            # =================================================================================================
            col_cl = index + 3; row = 5
            w_s[2].cell(row=row, column=col_cl, value=site["name"])
            # Wochenwerte darunter schreiben
            for offset_cl, week in enumerate(range(15, -1, -1), start=1):
                w_s[2].cell( row=row + offset_cl, column=col_cl, value=checklisten.get(f"{week:02d}_Woche", 0) )






            all_items.extend(items)
        DiagrammMaker().add_area_chart(ws=w_s[1], title="Open Points", x_title="Week", y_title="Count")
        DiagrammMaker().add_area_chart(ws=w_s[2], title="Checklists", x_title="Week", y_title="Count")
        # add_area_chart(ws=w_s[2], title="Checklists", x_title="Week", y_title="Count")
        # TODO 260801 Name setzen
        wb.save("sitemark_report.xlsx")

        logger.info("=" * 80)
        logger.info("Alle Sites verarbeitet.")
        logger.info("Gesamteinträge: %s", len(all_items))     
                
    # =================================================================================================
    # Ausführen der Pipeline basierend auf dem gewählten Modus
    # =================================================================================================
    def run(self, mode):
        logger.info("=====X START SITEMARK PIPELINE X=====")
        if mode == "N":
            # Abrufen der SITES aus SITEMARK und Erstellen der EXCEL-Datei zur Koordination
            self.export_sites()
        elif mode == "M":
            # Aufbau der EXCEL-Datei mit den Sites, die in der vorherigen Ausführung markiert wurden
            create_excel_report()
            # Laden der markierten Sites aus der EXCEL-Datei
            self.load_selected_sites()
            # Abrufen der Punchlist-Items für die markierten Sites und Erstellen des Berichts
            self.fetch_punchlists()
            # Erstellen des Makros in der EXCEL-Datei zur Anpassung der Diagramme
            make_macro()


        else:
            logger.error("Ungültige Auswahl.")
        logger.info("===== PIPELINE ABGESCHLOSSEN =====")