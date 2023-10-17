from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import openpyxl
import requests
import os

app = Flask(__name__)

def limpieza(response):
    response = response.json()
    del response["effective_url"]
    del response["word_count"]
    del response["og_url"]
    del response["og_image"]
    del response["og_type"]
    del response["twitter_site"]
    del response["twitter_creator"]
    del response["twitter_image"]
    del response["twitter_title"]
    del response["twitter_description"]
    del response["twitter_card"]
    return response

def txtfly(url):
    api = "https://full-text-rss.p.rapidapi.com/extract.php"
    payload = {
        "url": f"{url}",
        "xss": "1",
        "lang": "2",
        "links": "remove",
        "content": "text"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "57b21f0580msha9486981b9f1776p19b5bdjsn45ac803f42e5",
        "X-RapidAPI-Host": "full-text-rss.p.rapidapi.com"
    }
    data = requests.post(api, data=payload, headers=headers)
    data_limpia = limpieza(data)
    return data_limpia

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Guardar el archivo Excel con las URLs en el servidor
        file.save('urls.xlsx')

        # Leer las URLs desde el archivo Excel
        workbook = openpyxl.load_workbook('urls.xlsx')
        sheet = workbook.active
        urls = [cell.value for cell in sheet['A']]

        lista_scraper = []
        for url in urls:
            lista_scraper.append(txtfly(url))

        # Crear un nuevo archivo Excel con los resultados
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        columnas = list(lista_scraper[0].keys())
        for col_idx, columna in enumerate(columnas, start=1):
            sheet.cell(row=1, column=col_idx, value=columna)

        for row_idx, objeto in enumerate(lista_scraper, start=2):
            for col_idx, columna in enumerate(columnas, start=1):
                sheet.cell(row=row_idx, column=col_idx, value=objeto[columna])

        # Guardar el archivo con los resultados
        workbook.save("scrapers.xlsx")

        return redirect(url_for('download', filename='scrapers.xlsx'))

@app.route('/download/<filename>')
def download(filename):
    directory = os.getcwd()  # Obtiene el directorio actual
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
