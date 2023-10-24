from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import openpyxl
import requests
from celery import Celery
import os
import time
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)


# Configuración de Celery
app.config['CELERY_BROKER_URL'] = 'redis://prototipo-scrapper_redis_1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://prototipo-scrapper_redis_1:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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
        "X-RapidAPI-Key": "6fd32a4cc6mshb266cfc4f75cd1dp12d4d1jsnd5bc578c4926",
    }
    data = requests.post(api, data=payload, headers=headers)
    data_limpia = limpieza(data)
    return data_limpia

@celery.task
def scrape_task(urls):
    logger.info("Inicio de la tarea")
    time.sleep(10)
    logger.info("Fin de la tarea")
    # lista_scraper = []
    # for url in urls:
    #     lista_scraper.append(txtfly(url))
    #         # Crear un nuevo archivo Excel con los resultados
    # workbook = openpyxl.Workbook()
    # sheet = workbook.active

    # columnas = list(lista_scraper[0].keys())
    # for col_idx, columna in enumerate(columnas, start=1):
    #     sheet.cell(row=1, column=col_idx, value=columna)

    # for row_idx, objeto in enumerate(lista_scraper, start=2):
    #     for col_idx, columna in enumerate(columnas, start=1):
    #         sheet.cell(row=row_idx, column=col_idx, value=objeto[columna])

    # # Guardar el archivo con los resultados
    # workbook.save("scrapers.xlsx")

    #return redirect(url_for('download', filename='scrapers.xlsx'))


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

        # Lanzar la tarea Celery en segundo plano
        print("ANTES DE ENTRAR A LA TAREA")
        task = scrape_task.apply_async(args=(urls,))

        return "La tarea de scraping se está ejecutando en segundo plano. Puede tomar un tiempo."



@app.route('/download/<filename>')
def download(filename):
    directory = os.getcwd()
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)