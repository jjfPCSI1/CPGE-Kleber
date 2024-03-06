from fabrique_sous_pages import *

CHAP_PHYS = lecture_chap('chapitres_physique.csv')

import glob

liste_chapitres = CHAP_PHYS.keys()

# Trier les chapitres en fonction de la clé "ordre"
chapitres_tries = sorted(CHAP_PHYS.items(), key=lambda x: x[1]["Ordre"])

s = """
# Liste des chapitres de physique

NB: les notes de cours et TD sont fournies «as is». Si vous détectez un problème, n'hésitez pas à le signaler.

NB2: pour voir les animations incluses dans les pdf, pensez à les ouvrir avec Acrobat Reader et cliquer sur la flèche de lecture sous l'animation.

NB3: les TD ne sont pas (et de loin) tous corrigés, mais je ne désespère pas de les compléter au fil des années. Si vous voulez une correction d'un exercice en particulier, n'hésitez pas à la demander via les commentaires sur la chaîne et si j'ai le temps, il est possible que je puisse le faire, par exemple sous forme d'un short.

"""

old_bloc = ''
# Afficher la liste des chapitres triés
for chapitre, details in chapitres_tries:
    bloc = details['Bloc']
    if old_bloc != bloc:
        old_bloc = bloc
        s += '\n\n## {}\n\n'.format(bloc)
    C = chapitre
    if 'S' in chapitre and len(chapitre) < 3:
        C = chapitre[0] + '0' + chapitre[1]
    pdf = ''
    tde = ''
    tdc = ''
    liste = glob.glob('Physique/pdf/{}*.pdf'.format(C))
    if len(liste) > 0: pdf = liste[0].replace('Physique/','')
    liste = glob.glob('Physique/pdf/td{}*enonce.pdf'.format(C))
    if len(liste) > 0: tde = liste[0].replace('Physique/','')
    liste = glob.glob('Physique/pdf/td{}*corrige.pdf'.format(C))
    if len(liste) > 0: tdc = liste[0].replace('Physique/','')
    print(f"Chapitre: {chapitre}, Ordre: {details['Ordre']}", pdf)
    s += '* {}, {}: [Vidéos]({}.html)'.format(chapitre, details['Titre'], chapitre)
    if pdf != '': s+= ', [notes de cours]({})'.format(pdf)
    if tde != '': s+= ', [énoncés]({})'.format(tde)
    if tdc != '': s+= ' et [corrigés (partiels)]({})'.format(tdc)
    if tde != '': s+= ' des TD'
    s += '\n'

with open('Physique/pdf.md', 'w') as f:
    f.write(s)
