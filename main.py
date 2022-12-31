# importar pages Anilist.py

import src.pages.Anilist as Anilist
import src.pages.Whatsapp as Whatsapp

foto_to_perfil = Anilist.main()
Whatsapp.main(foto_to_perfil)
