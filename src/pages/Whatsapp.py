import configparser
import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# leyendo configuracion
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

tiempo_espera_pagina = config['DEFAULT']['tiempo_espera_pagina']
PERFIL_FIREFOX = webdriver.FirefoxProfile("perfiles/firefox")

# mis variables
ELEMENTO_FOTO = "/html/body/div[1]/div/div/div[3]/header/div[1]/div/img"
ELEMENTO_INPUT_FOTO = '//INPUT[@type="file"]'
ELEMENTO_BOTON_MENOS = '//button[@data-testid="crop-tool-zoom-out"]'
ELEMENTO_BOTON_ENVIAR_FOTO = '//span[@data-testid="checkmark-large"]'
driver = None

def open_page():
    driver_local = webdriver.Firefox(firefox_profile=PERFIL_FIREFOX)

    # entramos en la web
    url = "https://web.whatsapp.com"
    driver_local.get(url)
    assert "WhatsApp" in driver_local.title

    # dormimos un poco para que cargue la web
    driver_local.implicitly_wait(tiempo_espera_pagina)
    return driver_local

def main(foto):
    global driver
    if not os.path.exists('personajes/'+foto):
        print('No existe el archivo')
        return


    try:
        driver = open_page()

        # buscamos el elemento para subir la foto
        wait = WebDriverWait(driver, 20)
        wait.until(ec.visibility_of_element_located((By.XPATH, ELEMENTO_FOTO)))
        driver.find_element(By.XPATH, ELEMENTO_FOTO).click()

        # subir file
        print("Vamos a poner la foto de perfil")
        driver.find_element(By.XPATH,
                            ELEMENTO_INPUT_FOTO).send_keys(os.getcwd() + '\\personajes\\' + foto)
        time.sleep(2)

        # clicker boton de menos varias veces
        print("El zoom siempre lo quiero al maximo ♥‿♥")
        for i in range(0, 10):
            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, ELEMENTO_BOTON_MENOS))).click()
            time.sleep(0.2)

        driver.find_element(By.XPATH, ELEMENTO_BOTON_ENVIAR_FOTO).click()
    except NoSuchElementException:
        print("No se ha encontrado el elemento")
        return

    finally:
        driver.quit()
        print("Se ha cerrado el navegador")


