import os
import dotenv
import requests
from .limpieza import limpieza

dotenv.load_dotenv()


def txtfly(url):
    
    ### api para pruebas
    # api = "https://verne-desarrollo.buho.media/txtfly/"
    
    api = "https://full-text-rss.p.rapidapi.com/extract.php"
    payload = {
        "url": f"{url}",
        "xss": "1",
        "lang": "3",
        "links": "remove", #Bien
        "content": "text" # text0, text##, text80
        # "parser": "html5php"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
        "X-RapidAPI-Host": "full-text-rss.p.rapidapi.com"
    }
    data = requests.post(api, data=payload, headers=headers)
    data = data
    data_limpia = limpieza(data)

    ### Conf para pruebas
    # data = requests.get(api, data={"url":url})
    # data_limpia = limpieza(data)


    return data_limpia