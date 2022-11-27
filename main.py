import random
import sys

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import urllib.request


# headers
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

# buscamos la victima
personajes = [
    64851,
    210
]
personaje = random.choice(personajes)
personaje = random.randint(1, 64851)

url = "https://anilist.co/character/{0}/".format(personaje)

# entramos en la web
driver = webdriver.Firefox()
driver.get(url)
assert "AniList" in driver.title

# dormimos un poco para que cargue la web
driver.implicitly_wait(1)

try:
    # buscamos la imagen
    img = driver.find_element(By.CLASS_NAME, "image")
    nombre_personaje = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/h1")

    # obtenemos la url de la imagen
    src = img.get_attribute("src")
    img_filename = "{0}.jpg".format(nombre_personaje.text)
    print(src)

    # obtenemos el nombre del personaje

    # descargamos la imagen
    request_ = urllib.request.Request(src, None, headers)  # The assembled request
    response = urllib.request.urlopen(request_)  # store the response

    # create a new file and write the image
    f = open('personajes/'+img_filename, 'wb')
    f.write(response.read())
    f.close()

except NoSuchElementException:
    print("No se ha encontrado la imagen")


driver.close()

