import threading
# import concurrent.futures
from scraper.txtify import txtfly
from .excel import generador_excel

def scrape_and_append(urls, result_list:list):
    for url in urls:
        result_list.append(txtfly(url))


def scrape_task(urls: list) -> list:
    print("----Entro----")
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

    print(url_batches)
    for url_batch in url_batches:
        print("Entro al for")
        thread = threading.Thread(target=scrape_and_append, args=(url_batch, lista_scraper))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    print("---sale---")
    return generador_excel(lista_scraper)