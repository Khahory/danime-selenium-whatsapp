import random

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

# buscamos la victima
personajes = [
    64851,
    210,
    # 859430
]
personaje = random.choice(personajes)
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

    # obtenemos la url de la imagen
    src = img.get_attribute("src")
    print(src)

    # descargamos la imagen
except NoSuchElementException:
    print("No se ha encontrado la imagen")


driver.close()

