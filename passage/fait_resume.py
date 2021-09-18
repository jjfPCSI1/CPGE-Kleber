
def lecture(fichier):
    """
    Renvoie le nombre de vidéos, le nombre de vues et le nombre moyen de vues par vidéo
    """
    vues_tot = 0
    nb = 0
    mini = 10**5
    maxi = 0
    with open(fichier) as f:
         for line in f:
              lien, duree, titre, vues = line.strip().split(';')
              vues = int(vues)
              vues_tot += vues
              nb += 1
              if vues > maxi: maxi = vues
              if vues < mini: mini = vues
    return nb, vues_tot, vues_tot // nb, mini, maxi

VUES_TOT = 0
NB_TOT = 0


for playlist in ['organisation', 'langues', 'maths', 'physique', 'chimie', 'informatique']:
    n, v, vpv, m, M = lecture(playlist + '.txt')
    s = "Concernant la playlist {}\n".format(playlist)
    s+= "Un total de {} vues pour {} vidéos, soit {} vues par vidéo en moyenne\n".format(v, n, vpv)
    s+= "avec un minimum de {} vues et un maximum de {} vues.\n".format(m, M)
    s+= 70 * "=" + "\n"
    print(s)
    VUES_TOT += v
    NB_TOT += n


print('Au total, {} vidéos totalisent {} vues soit {} vues par vidéo'.format(NB_TOT, VUES_TOT, VUES_TOT // NB_TOT))
