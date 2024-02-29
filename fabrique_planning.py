"""
Fabrication des pages du planning en plusieurs étapes:

* on lit le fichier semaines/planning.txt qui associe à chaque semaine une
date (un lundi) ainsi qu'un ou plusieurs chapitre (info non utilisée, juste là
pour être sûr qu'on s'y retrouve). On fabrique à partir de là la page d'index
de Physique/planning/

* ensuite, on passe en revue toutes les fichiers semaines/Sem??.txt pour
construire les Physique/planning/Sem??.md associés dans lesquels on met les
vidéos sous forme d'une liste de liens et ensuite en vidéos embarquées.

"""

debut_index = """
# Planning de l'année 2023-2024

Vous trouverez sur cette page les liens vers les vidéos à voir pour chaque
semaine de l'année à chaque fois pour le lundi qui commence:

"""

def transforme(date):
    """ Prend une date au format jj-mm-aa et renvoie la chaine jj mois aaaa """
    MOIS = {'01': 'janvier', '02': 'février', '03': 'mars', '04': 'avril',
            '05': 'mai', '06': 'juin', '07': 'juillet', '08': 'août',
            '09': 'septembre', '10': 'octobre', '11': 'novembre', '12': 'décembre'}
    j, m, a = date.split('-')
    return "{} {} 20{}".format(j, MOIS[m], a)

def embedded_video(lien):
    video_inline = lien.replace('https://youtu.be/', 'https://www.youtube.com/embed/')
    return """<div style="text-align:center">
<iframe width="560" height="315" src="{}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
""".format(video_inline)

def heure_min(duree):
    if duree // 60 > 0:
        return "{} h et {} minutes".format(duree//60, duree%60)
    else:
        return "{} minutes".format(duree)

# Lecture des données sur les longueurs des vidéos

DUREE = {}
with open('semaines/longueurs.txt') as f:
    for ligne in f:
        lien, duree = ligne.split(';')
        DUREE[lien] = int(duree)//60 + 1 # On arrondit à la minute supérieure

# Lecture du planning
DATE = {}
CHAPITRES = {}
with open('semaines/planning.txt') as f:
    for ligne in f:
         semaine, date, chapitres = ligne.split(';')
         DATE[semaine] = transforme(date)
         CHAPITRES[semaine] = chapitres.strip()




# Ne reste plus qu'à faire une boucle sur les semaines et écrire les pages associées.

DUREES_TOT = {}
for semaine in DATE.keys():
    duree_totale = 0 # Temps total en minutes
    duree_opt = 0    # Temps des vidéos optionnelles
    txt = """
# Vidéos à voir pour le lundi {}, chapitre {}

Durée totale en vitesse normale: DUREE

## Liste avec liens vers YouTube

""".format(DATE[semaine], CHAPITRES[semaine])
    embedded = """
## Liste avec inclusion des vidéos

"""
    # Cas où il y a plusieurs chapitres
    if CHAPITRES[semaine].count(',') > 0:
        txt = txt.replace('chapitre', 'chapitres')
    generic = "* {} [{}]({}) ({})\n"
    generic_embedded = "* {} {} ({})\n\n {} \n\n"
    with open('semaines/{}.txt'.format(semaine)) as f:
        print("On s'occupe de {}".format(semaine))
        nb_opt = 0
        for ligne in f:
            # Cas des vidéos optionnelles, on donne le nombre
            print(ligne)
            if ligne.startswith('# Optionnel'):
                data = ligne.split()
                if len(data) > 2:
                    nb_opt = int(data[2])
                else: # ou alors tout le reste est concerné
                    nb_opt = 100
            else:
                # Si on n'a pas de caractère optionnel
                if nb_opt > 0:
                    nb_opt -= 1
                    opt = '(optionnel)'
                else:
                    opt = ''
                type, matiere, chapitre, titre, lien = ligne.strip().split(';')
                if 'Exos' in type:
                    txt += '* {}: {}\n'.format(type, titre)
                else:
                    duree = DUREE[lien]
                    duree_totale += duree
                    if opt:
                        duree_opt += duree
                    txt += generic.format(opt, titre, lien, heure_min(duree))
                    embedded += generic_embedded.format(opt, titre, heure_min(duree), embedded_video(lien))


    with open('Physique/planning/{}.md'.format(semaine), 'w') as f:
        dur_tot = heure_min(duree_totale - duree_opt)
        dur_opt = heure_min(duree_opt)
        dur = "{} (plus {} en option)".format(dur_tot, dur_opt)
        DUREES_TOT[semaine] = dur
        f.write(txt.replace('DUREE', dur))
        f.write(embedded)


# La page d'index

txt_index = debut_index

generic = '* Vidéos de la [semaine {}]({}.html) ({}) à avoir vu pour le lundi {}   \n  durée: {}\n'
for k in sorted(DATE.keys()):
     chap = CHAPITRES[k]
     num  = k[-2:] # Les deux derniers sont les chiffres de la semaine
     date = DATE[k]
     if chap == 'CCB':
         txt_index += '* Semaine du concours blanc, révisez bien !\n'
     elif chap == 'Révisions':
         txt_index += '* Exercices de révision à préparer, pas de vidéos\n'
     else:
         txt_index += generic.format(num, k, chap, date, DUREES_TOT[k])

with open('Physique/planning/index.md', 'w') as f:
    f.write(txt_index)
