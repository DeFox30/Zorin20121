from typing import List

class Artist:
    def __init__(self, name: str):
        self.name = name
        self.albums: List['Album'] = []

    def add_album(self, album: 'Album'):
        self.albums.append(album)


class Song:
    def __init__(self, title: str, duration: int, album: 'Album'):
        self.title = title
        self.duration = duration
        self.album = album


class Album:
    def __init__(self, title: str, artist: Artist):
        self.title = title
        self.artist = artist
        self.songs: List[Song] = []
        artist.add_album(self)

    def add_song(self, title: str, duration: int):
        song = Song(title, duration, self)
        self.songs.append(song)


class Playlist:
    def __init__(self, name: str):
        self.name = name
        self.songs: List[Song] = []

    def add_song(self, song: Song):
        self.songs.append(song)
