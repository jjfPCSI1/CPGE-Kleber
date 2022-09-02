"""
Récupère les informations sur les vidéos (titre, lien et longueur)
à partir de l'adresse de la playlist dans laquelle se trouvent ces vidéos
"""

import pafy

from pytube import Playlist


PLAYLISTS = {}
with open('playlists.txt') as f:
    for ligne in f:
        denomination, lien = ligne.strip().split(';')
        if denomination[0] == '#': continue
        PLAYLISTS[denomination] = lien

for denomination in PLAYLISTS:
    print("On s'occupe de {}".format(denomination))
    lien = PLAYLISTS[denomination]
    print(lien)
    with open('{}.txt'.format(denomination), 'w') as f:
        p = Playlist(lien)
        for lien in p:
            video = pafy.new(lien)
            titre = video.title
            nb_vues = video.viewcount
            print('On récupère la vidéo: {}'.format(titre))
            print('Temps en s:',video.length,'Nombre de vues:',nb_vues)
            f.write("{};{};{};{}\n".format(lien, video.length, titre, nb_vues))
