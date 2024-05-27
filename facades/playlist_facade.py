import models
import schemas
from facades.base_facade import BaseFacade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

class PlaylistFacade(BaseFacade):
    async def create_playlist(self, user_id: int, playlist_data: schemas.PlaylistCreate) -> models.Playlist:
        db_playlist = models.Playlist(name=playlist_data.name, user_id=user_id)
        self.db.add(db_playlist)
        await self.db.commit()
        await self.db.refresh(db_playlist)
        return db_playlist

    async def add_song_to_playlist(self, playlist_song_data: schemas.PlaylistSongCreate) -> models.PlaylistSong:
        # Проверка на существование плейлиста
        playlist = await self.db.get(models.Playlist, playlist_song_data.playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")

        # Проверка на существование песни
        song = await self.db.get(models.Song, playlist_song_data.song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")

        # Проверка на наличие уже существующей записи
        existing_entry = await self.db.execute(
            select(models.PlaylistSong).filter_by(
                playlist_id=playlist_song_data.playlist_id,
                song_id=playlist_song_data.song_id
            )
        )
        if existing_entry.scalars().first():
            raise HTTPException(status_code=400, detail="Song already in playlist")

        playlist_song = models.PlaylistSong(
            playlist_id=playlist_song_data.playlist_id,
            song_id=playlist_song_data.song_id
        )
        self.db.add(playlist_song)
        await self.db.commit()
        await self.db.refresh(playlist_song)
        return playlist_song

    async def get_playlist_songs(self, user_id: int, playlist_id: int) -> schemas.PlaylistWithSongs:
        playlist = await self.db.execute(
            select(models.Playlist)
            .options(
                selectinload(models.Playlist.songs).selectinload(models.PlaylistSong.song)
            )
            .filter_by(id=playlist_id, user_id=user_id)
        )
        playlist = playlist.scalars().first()
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")

        # Создаем данные для песен вручную
        songs_data = [schemas.Song.from_orm(playlist_song.song).dict() for playlist_song in playlist.songs]

        # Создаем данные для плейлиста вручную
        playlist_data = {
            "id": playlist.id,
            "user_id": playlist.user_id,
            "name": playlist.name,
            "songs": songs_data
        }

        return schemas.PlaylistWithSongs(**playlist_data)

    async def get_user_playlists(self, user_id: int) -> list[schemas.Playlist]:
        playlists = await self.db.execute(
            select(models.Playlist).filter_by(user_id=user_id)
        )
        playlists = playlists.scalars().all()
        return [schemas.Playlist.from_orm(playlist) for playlist in playlists]


# Создание глобального объекта фасада
playlist_facade = PlaylistFacade()