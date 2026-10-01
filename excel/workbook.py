import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
from datetime import datetime, timedelta
from ..excel.styles import ExcelStyles

# =================================================================================================
# Anlegen WORKBOOK und der Seiten
# =================================================================================================
def create_excel_report():
    wb = Workbook()
    ws_base = wb.active
    ws_base.title = "Data_Basis"
    ws_open_points = wb.create_sheet("Open Points")
    ws_checklists = wb.create_sheet("Checklists")
    ws_data_basis = wb.create_sheet("Data Basis")
    wb.remove(ws_base)

    w_s = (ws_data_basis, ws_open_points, ws_checklists)

    # =================================================================================================
    # Seitenaufbau für 1. Seite
    # =================================================================================================
    headers = [
            "Site",
            "Description",
            "Model",
            "Visible_ID",
            "Status",
            "Typ",
            "Created",
            "Updated",
            "Life"
        ]

    today = datetime.today()

    for week in range(15, -1, -1):
        week_date = today - timedelta(days=week * 7)
        monday = week_date - timedelta(days=week_date.weekday())
        # headers.append( f"CW{week:02d}\n{week_date.strftime('%d.%m.%Y')}" )
        headers.append(f"CW {week_date.isocalendar()[1]}\n{monday.strftime('%d.%m.%Y')}")

    ws_data_basis.append(headers)


    for col in range(1, 27):
        ws_data_basis.cell( row=1, column=col 
        ).alignment = Alignment(
            wrap_text=True,
            textRotation=90,
            horizontal="center",
            vertical="center"
        )
        ws_data_basis.cell(row=1, column=col).font = Font(bold=True)



    ws_data_basis.column_dimensions["A"].width = 20
    ws_data_basis.column_dimensions["B"].width = 30
    ws_data_basis.column_dimensions["C"].width = 12
    ws_data_basis.column_dimensions["D"].width = 8
    ws_data_basis.column_dimensions["E"].width = 15
    ws_data_basis.column_dimensions["F"].width = 15
    ws_data_basis.column_dimensions["G"].width = 20
    ws_data_basis.column_dimensions["H"].width = 20
    for col in range(9, 26):
        ws_data_basis.column_dimensions[ get_column_letter(col) ].width = 5

    # =================================================================================================
    # Seitenaufbau für 2. Seite
    # =================================================================================================
    ws_open_points.append(["OPEN POINTS"])
    ws_open_points.append(["The diagram shows all OPEN POINTS in status TO_DO, PLANNED, IN_PROGRESS or RESOLVED"])
    ws_open_points.append(["The detailed infomation are available in the Data Basis sheet"])
    ws_open_points.append([""])
    ws_open_points.cell(row=5, column=1).value = "Monday of Calenderweek"
    ws_open_points.cell(row=5, column=2).value = "Calenderweek / Site"
    ws_open_points.row_dimensions[5].height = 80

    for week in range(15, -1, -1):
        week_date = today - timedelta(days=week * 7)
        ws_open_points.append([
            week_date.strftime("%d.%m.%Y"),
            f"CW {week_date.isocalendar()[1]}"
        ])

    ws_open_points.column_dimensions["A"].width = 14
    ws_open_points.cell(row=1, column=1).fill = ExcelStyles.LIGHT_BLUE_FILL
    ws_open_points.cell(row=21, column=1).fill = ExcelStyles.LIGHT_BLUE_FILL

    # =================================================================================================
    # Seitenaufbau für 3. Seite
    # =================================================================================================
    ws_checklists.append(["CHECKLISTS"])
    ws_checklists.append(["The diagram shows all CHECKLISTS in status TO_DO, PLANNED, IN_PROGRESS or RESOLVED"])
    ws_checklists.append(["The detailed infomation are available in the Data Basis sheet"])
    ws_checklists.append([""])
    ws_checklists.cell(row=5, column=1).value = "Monday of Calenderweek"
    ws_checklists.cell(row=5, column=2).value = "Calenderweek / Site"
    ws_checklists.row_dimensions[5].height = 80

    for week in range(15, -1, -1):
        week_date = today - timedelta(days=week * 7)
        ws_checklists.append([
            week_date.strftime("%d.%m.%Y"),
            f"CW {week_date.isocalendar()[1]}"
        ])

    ws_checklists.column_dimensions["A"].width = 14
    ws_checklists.cell(row=1, column=1).fill = ExcelStyles.LIGHT_YELLOW_FILL
    ws_checklists.cell(row=21, column=1).fill = ExcelStyles.LIGHT_YELLOW_FILL

    return wb, w_s