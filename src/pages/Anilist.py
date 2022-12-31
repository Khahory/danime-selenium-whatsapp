import os
import random
import urllib.request
import configparser
from PIL import Image

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

load_dotenv('.env')

# leyendo configuracion
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
tiempo_espera_pagina = config['DEFAULT']['tiempo_espera_pagina']
img_filename = None

def buscar_personaje():
    # variables
    imagen_default = "character/large/default"
    is_404 = True
    driver = webdriver.Firefox()

    # headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    while is_404:
        # buscamos la victima
        personaje_code = random.randint(1, 128038)

        print("Buscando personaje con ID: " + str(personaje_code))

        # entramos en la web
        url = "https://anilist.co/character/{0}/".format(personaje_code)
        driver.get(url)
        assert "AniList" in driver.title

        # dormimos un poco para que cargue la web
        driver.implicitly_wait(tiempo_espera_pagina)

        # nos logueamos
        login_to_page(driver)

        try:
            # global
            global img_filename

            # comprobamos si es NSFW
            if validar_personaje_nsfw(driver, url):
                print("Es NSFW ¯\_(ツ)_/¯ busquemos otro...")
                continue

            # si navegamos a otra pagina perdemos lo que teniamos en la variable driver.find_element
            # buscamos la imagen
            img = driver.find_element(By.CLASS_NAME, "image")
            nombre_personaje = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/h1")

            # obtenemos la url de la imagen
            src = img.get_attribute("src")

            # validamos que no tenga imagen default
            if imagen_default in src:
                print("No tiene imagen, buscando otra...")
                continue

            # obtenemos el nombre del personaje
            img_filename = "{0}.jpg".format(nombre_personaje.text)
            print(src)

            # descargamos la imagen
            request_ = urllib.request.Request(src, None, headers)  # The assembled request
            response = urllib.request.urlopen(request_)  # store the response

            # create a new file and write the image
            f = open('personajes/' + img_filename, 'wb')
            f.write(response.read())
            f.close()

            # validamos las dimensiones de la imagen
            if not validar_dimensiones_img(img_filename):
                continue

            is_404 = False

        except NoSuchElementException:
            print("No se ha encontrado la imagen")

    driver.close()

def validar_dimensiones_img(img):
    # get image
    filepath = "personajes/" + img
    img = Image.open(filepath)

    # get width and height
    width = img.width
    height = img.height

    # display width and height
    print("The height of the image is: ", height)
    print("The width of the image is: ", width)
    img.close()

    if width < 192 or height < 192:
        print("La imagen es muy pequeña, la eliminamos")
        os.remove(filepath)
        return False

    return True


def validar_personaje_nsfw(driver_web, url):
    print("Personaje NSFW ? o_O")

    # variables
    driver = driver_web

    try:
        driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div/div[1]/div/div[1]/a").click()
        is_NSFW = driver.find_element(By.CLASS_NAME, "adult-label").text
        if is_NSFW == "ADULT":
            return True

    except NoSuchElementException:
        # entramos en la web
        driver.get(url)
        driver.implicitly_wait(tiempo_espera_pagina)
        return False

def login_to_page(driver):
    # nos logueamos y buscamos nuestras cookies
    # time.sleep(30)
    # print(driver.get_cookies())

    print('Verificando si ya estamos logueados...')
    cookies = driver.get_cookies()
    try:
        if cookies[1]:
            print('OK!')

    except IndexError:
        print('Agregando cookies...')
        driver.add_cookie({
            'name': os.getenv('NAME'),
            'value': os.getenv('VALUE'),
            'path': os.getenv('COOKIE_PATH'),
            'domain': os.getenv('DOMAIN'),
            'secure': bool(os.getenv('SECURE')),
            'httpOnly': bool(os.getenv('HTTPONLY')),
            'expiry': int(os.getenv('EXPIRY')),
            'sameSite': os.getenv('SAMESITE')
        })
        driver.refresh()
        driver.implicitly_wait(tiempo_espera_pagina)

def main():
    buscar_personaje()
    return img_filename

if __name__ == "__main__":
    main()
