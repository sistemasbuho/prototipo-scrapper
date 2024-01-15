import openpyxl
from io import BytesIO

workbook = openpyxl.Workbook()
sheet = workbook.active



def generador_excel(lista_scraper: list):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    columnas = list(lista_scraper[0].keys())
    for col_idx, columna in enumerate(columnas, start=1):
        sheet.cell(row=1, column=col_idx, value=columna)

    for row_idx, objeto in enumerate(lista_scraper, start=2):
        for col_idx, columna in enumerate(columnas, start=1):
            sheet.cell(row=row_idx, column=col_idx, value=objeto[columna])

    return workbook

def descargar_excel(workbook):
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer