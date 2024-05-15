from sync_db import Base
from sqlalchemy import (Column, Integer, String,
                        TIMESTAMP, text, ForeignKey, Boolean)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    playlists = relationship('Playlist', back_populates='user')
    favorite_songs = relationship('FavoriteSong', back_populates='user')


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    albums = relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)

    artist = relationship('Artist', back_populates='albums')
    songs = relationship('Song', back_populates='album')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

    songs = relationship('SongGenreAssociation', back_populates='genre')


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    text = Column(String, nullable=True)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)

    album = relationship('Album', back_populates='songs')
    genres = relationship('SongGenreAssociation', back_populates='song')
    liked_by_users = relationship('FavoriteSong', back_populates='song')


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='playlists')
    songs = relationship('PlaylistSong', back_populates='playlist')


class SongGenreAssociation(Base):
    """
    m2m table songs to genres
    """

    __tablename__ = 'song_genre_association'

    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True, nullable=False)

    song = relationship('Song', back_populates='genres')
    genre = relationship('Genre', back_populates='songs')


class FavoriteSong(Base):
    """
    m2m table songs to users
    """
    __tablename__ = 'favorite_songs'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True, nullable=False)

    user = relationship('User', back_populates='favorite_songs')
    song = relationship('Song', back_populates='liked_by_users')


class PlaylistSong(Base):
    """
    m2m table songs to playlist
    """
    __tablename__ = 'playlist_songs'
    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True, nullable=False)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True, nullable=False)

    playlist = relationship('Playlist', back_populates='songs')
    song = relationship('Song')