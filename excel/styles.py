from openpyxl.styles import PatternFill

class ExcelStyles:
    def get_fill(color):
        return PatternFill(
            fill_type="solid",
            start_color=color,
            end_color=color
        )


    LIGHT_BLUE_FILL = get_fill("D9EAF7")
    LIGHT_YELLOW_FILL = get_fill("FFF2CC")
