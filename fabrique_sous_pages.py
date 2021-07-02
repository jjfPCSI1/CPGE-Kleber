import csv

ASSOC_TYPES = {'DiaN': 'Démo in a Nutshell', 
               'Essentiel': "L'essentiel du cours", 
               'Cours': 'Vidéos de cours', 
               'Expériences': 'Expériences amusantes', 
               'TD': 'Exercices de TD', 
               'Savoir-faire': 'Savoir-faire', 
               'Pardèf': 'Par définition',
               'TP': 'Savoir-faire de TP'}

def lecture_chap(fichier):
    DICO = {}
    ordre = []
    with open(fichier, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            numero = row['Numéro']
            titre = row['Titre']
            lien = row['Lien']
            bloc = row['Bloc']
            ordre= float(row['Ordre'])
            DICO[numero] = {'Titre': titre, 'Lien': lien, 'Bloc': bloc, 'Ordre': ordre}
        return DICO

def lecture_donnees(fichier):
    types = set()
    matieres = set()
    videos = []
    with open(fichier, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            types.add(row['Type'])
            matieres.add(row['Matière'])
            videos.append(row)
        return videos, matieres, types

CHAP_PHYS = lecture_chap('chapitres_physique.csv')

CHAP = {'Physique': CHAP_PHYS}

DONNEES_VIDEOS, MATIERES, TYPES = lecture_donnees('donnees_videos.csv')

# Création des différents répertoires
import os
for matiere in MATIERES:
    if not os.path.exists(matiere):
         os.mkdir(matiere)
         print('Création du répertoire {}/'.format(matiere))
    

def partie_page(titre, donnees):
    """
    Fabrique la sous-partie d'une page de chapitre, on doit donner:
    * le titre associé (Cours, TD, DiaN, etc)
    * la liste des vidéos associées
    """
    s = '## {}\n\n'.format(titre)
    for v in donnees:
         s += '* [{}]({})\n'.format(v['Titre'], v['Lien'])
    return s + "\n"

def fabrique_page_chapitre(chapitre, matiere='Physique'):
    chap = CHAP[matiere][chapitre]
    fichier = '{}/{}.md'.format(matiere, chapitre)
    # Les vidéos associées à ce chapitre
    videos = [v for v in DONNEES_VIDEOS if v['Chapitre'] == chapitre and v['Matière'] == matiere]
    with open(fichier, 'w') as f:
        # On commence par le titre
        f.write('# {}\n\n'.format(chap['Titre']))
        f.write('La playliste principale peut se trouver à [ce lien]({}).\n\n'.format(chap['Lien']))
        f.write("Dans le détail, voici ce qu'on peut trouver de ce chapitre.\n\n")
        for type in ASSOC_TYPES:
            vids = [v for v in videos if v['Type'] == type]
            if len(vids) > 0:
                 f.write(partie_page(ASSOC_TYPES[type], vids))

# Exécution proprement dite
for matiere in CHAP:
    for chap in CHAP[matiere]:
        fabrique_page_chapitre(chap, matiere)


# On fabrique aussi les pages principales de chaque matière en complétant le 
# fichier .txt déjà présent avec la liste des chapitres disponibles

for matiere in CHAP:
    mat = matiere.lower()
    s = ''
    with open('{}.txt'.format(mat)) as f:
         for r in f:
             s += r
    generic = '* [{}]({}/{}.html) \n'
    with open('{}.md'.format(mat), 'w') as f:
        try:
             chapitres = CHAP[matiere]
             chaps = list(chapitres.keys())
             print(chaps)
             chaps.sort(key=lambda c: chapitres[c]['Ordre'])
             bloc = None
             for c in chaps:
                 if not(bloc) or bloc != chapitres[c]['Bloc']: 
                    bloc = chapitres[c]['Bloc']
                    s += '### Bloc {}\n\n'.format(bloc)
                 print(c)
                 s+= generic.format(chapitres[c]['Titre'], matiere, c)
             s += '\n\n'
        except : 
            raise 
        f.write(s)
