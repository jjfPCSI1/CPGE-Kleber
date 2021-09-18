import pafy
import sys
import time
url = "https://youtube.com/playlist?list=PLEABsk5Xlyk4i5Y5lKBJ-hh6BhRHeV31B"
details = pafy.get_playlist(url)
playlist = pafy.get_playlist2(url)
# below three statements print the tilte,author and number of videos
print(details['title'])
print(details['author'])
print(len(playlist))
