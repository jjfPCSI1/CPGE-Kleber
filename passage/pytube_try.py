import pafy
from pytube import Playlist

p = Playlist('https://youtube.com/playlist?list=PLEABsk5Xlyk4i5Y5lKBJ-hh6BhRHeV31B')

for video in p[:3]:
    print(video)
