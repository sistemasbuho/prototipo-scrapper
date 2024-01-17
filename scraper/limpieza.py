import re

def unir_descripcion_content(response:dict):
    response["content"] = f"{response['og_description']}\n{response['content']}"
    del response["og_description"]
    return response

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
    del response["title"]
    del response["excerpt"]
    del response["date"]
    del response["author"]
    del response["language"]
    del response["og_title"]

    # Esto es para quitar los saltos de línea necesarios
    response["content"] = re.sub(r'[^\w\s]', '', response["content"].replace('\n\n', ' NEW_PARAGRAPH ').replace('\n', ' ')).replace(' NEW_PARAGRAPH ', '\n')
    
    # Eliminar el espacio sin rompimiento (U+00A0)
    response["content"] = response["content"].replace('\u00A0', ' ')
    
    # Une la cuadrilla de la nota con el contenido principal
    response = unir_descripcion_content(response)
    return response