from sqlalchemy.future import select

import models
import schemas
from facades.base_facade import BaseFacade
from fastapi import HTTPException, status
from sqlalchemy import func

from facades.file_facade import FILE_MANAGER


class SongFacade(BaseFacade):
    async def create_song(self, song_data: schemas.SongCreate, file_path) -> models.Song:
        db_song = models.Song(
            title=song_data.title,
            album_id=song_data.album_id,
            text=song_data.text,
            file_path=file_path
        )
        self.db.add(db_song)
        await self.db.commit()
        await self.db.refresh(db_song)

        for genre_id in song_data.genres:
            genre = await self.db.get(models.Genre, genre_id)
            if genre:
                song_genre = models.SongGenreAssociation(song_id=db_song.id, genre_id=genre_id)
                self.db.add(song_genre)
        await self.db.commit()
        await self.db.refresh(db_song)

        return db_song

    async def get_songs_by_genre(self, genre_id) -> list[schemas.Song]:
        genre = await self.db.get(models.Genre, genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")

        # songs = await self.db.execute(
        #     select(models.Song).join(models.SongGenreAssociation).filter(
        #         models.SongGenreAssociation.genre_id == genre_id
        #     )
        # )
        # songs = songs.scalars().all()
        # return [schemas.Song.from_orm(song) for song in songs]

        songs = await self.db.execute(
            select(
                models.Song,
                func.count(models.FavoriteSong.user_id).label("favorite_count")
            )
            .join(models.SongGenreAssociation)
            .outerjoin(models.FavoriteSong, models.Song.id == models.FavoriteSong.song_id)
            .filter(models.SongGenreAssociation.genre_id == genre_id)
            .group_by(models.Song.id)
            .order_by(func.count(models.FavoriteSong.user_id).desc())
            .limit(15)
        )
        songs = songs.all()
        return [schemas.Song(
            id=song.id,
            title=song.title,
            text=song.text,
            album_id=song.album_id,
            favorite_count=favorite_count
        ) for song, favorite_count in songs]

    async def get_song(self, song_id: int) -> models.Song:
        song = await self.db.get(models.Song, song_id)
        if not song:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
        return song

    async def delete_song(self, song_id: int) -> None:
        song = await self.db.get(models.Song, song_id)
        if not song:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
        await FILE_MANAGER.delete_file(song.file_path)

        await self.db.execute(
            models.SongGenreAssociation.__table__.delete().where(models.SongGenreAssociation.song_id == song.id)
        )
        await self.db.execute(
            models.FavoriteSong.__table__.delete().where(models.FavoriteSong.song_id == song.id)
        )
        await self.db.execute(
            models.PlaylistSong.__table__.delete().where(models.PlaylistSong.song_id == song.id)
        )

        await self.db.delete(song)
        await self.db.commit()


song_facade = SongFacade()
