import threading
# import concurrent.futures
from scraper.txtify import txtfly
from .excel import generador_excel

column_mapping = {
    "id": "id",#
    "Titular": "title",
    "Contenido": "content",
    "Link": "url",
    "Keyword": "Keyword",#
    "Fecha": "date",
    "Ubicación": "Ubicación",
    "Medio": "domain",
}

def scrape_and_append(urls, result_list:list):
    for url in urls:
        result_list.append(txtfly(url))


def scrape_task(urls: list) -> list:
    lista_scraper = []

    cantidad_urls = len(urls)

    # Numero de peticiones por paquete
    if cantidad_urls >= 60:
        num_threads = 8
    elif cantidad_urls >= 50:
        num_threads = 6
    elif cantidad_urls >= 40:
        num_threads = 4
    elif cantidad_urls >= 20:
        num_threads = 2
    else:
        num_threads = 1


    # Dividir las URLs en paquetes para cada hilo
    url_batches = [urls[i:i + num_threads] for i in range(0, len(urls), num_threads)]

    threads = []

    for url_batch in url_batches:
        thread = threading.Thread(target=scrape_and_append, args=(url_batch, lista_scraper))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    return generador_excel(lista_scraper, column_mapping, urls)