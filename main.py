# importar pages Anilist.py

import src.pages.Anilist as Anilist
import src.pages.Whatsapp as Whatsapp

foto_to_perfil = Anilist.main()

print("Vamos a poner a este personaje como foto de perfil de Whatsapp " + foto_to_perfil)

Whatsapp.main(foto_to_perfil)
