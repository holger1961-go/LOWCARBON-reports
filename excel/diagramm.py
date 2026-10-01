
from __future__ import annotations
from openpyxl.styles import Alignment, Font
from openpyxl.chart import AreaChart3D, Reference
from openpyxl.chart._3d import View3D
from openpyxl.utils import get_column_letter
from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor
from ..utils.logging_setup import logger
from typing import List, Tuple

class DiagrammMaker:
    def add_area_chart(self, ws: str, title: str, x_title: str, y_title: str, header_row: int = 5):
        """
        Formatieren der Kopfzeile.
        """
        for col in range(1, ws.max_column + 1):
            ws.cell( row=5, column=col 
            ).alignment = Alignment(
                wrap_text=True,
                textRotation=90,
                horizontal="center",
                vertical="center"
            )
            ws.cell(row=5, column=col).font = Font(bold=True)
        """
        Insert an area chart using `header_row` as the row containing column titles.
        Data rows begin at `header_row + 1`.
        """
        # ws = self.wb[ws_name]
        # need at least one header row and one data row with at least two columns of data
        if ws.max_row < header_row + 1 or ws.max_column < 3:
            logger.info('Überspringe Diagramm für %s (zu wenig Daten).', ws.title)
            return
            
        chart = AreaChart3D()
        chart.title = title
        chart.style = 13
        chart.grouping = "standard"
        chart.legend = None

        # Positionierung
        anchor = TwoCellAnchor()
        anchor._from.col = 0 
        anchor._from.row = ws.max_row + 2 
        anchor.to.col = 15 
        anchor.to.row = ws.max_row + 30 
        chart.anchor = anchor

        # Daten-Referenzen
        cats = Reference(ws, min_col=2, min_row=header_row + 1, max_row=ws.max_row)
        data = Reference(ws, min_col=3, min_row=header_row, max_col=ws.max_column, max_row=ws.max_row)
        
        
        if chart.x_axis:
            chart.x_axis.title = x_title
            chart.x_axis.delete = False
            chart.x_axis.tickLblPos = "nextTo"
        else:
            logger.info("Fehler beim x_axis")

        if chart.y_axis:
                chart.y_axis.title = y_title
                chart.y_axis.delete = False
                chart.y_axis.tickLblPos = "nextTo"
        else:
            logger.info("Fehler beim y_axis")

        chart.z_axis.delete = False

        # Daten hinzufügen
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)


        ws.add_chart(chart)