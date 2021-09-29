import pafy

resultat = ''

with open('total.txt') as f:
    with open('longueurs.txt', 'a') as g:
        for line in f:
            if not(line.startswith('#')):
                 url = line.strip().split(';')[-1]
                 print('On regarde {}'.format(url))
                 video = pafy.new(url)
                 print("Il s'agit de {} ({})".format(video.title, video.length))
                 resultat = "{};{}\n".format(url, video.length)
            g.write(resultat)

