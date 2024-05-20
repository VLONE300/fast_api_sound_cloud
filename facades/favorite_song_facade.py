import models
import schemas
from facades.base_facade import BaseFacade
from fastapi import HTTPException, status, FastAPI
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class FavoriteSongFacade(BaseFacade):
    async def add_favorite_song(self, song_id, user_id: int) -> schemas.FavoriteSong:
        song = await self.db.get(models.Song, song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        existing_favorite = await self.db.execute(
            select(models.FavoriteSong).filter_by(user_id=user_id, song_id=song_id)
        )
        if existing_favorite.scalars().first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Song is already in favorited")
        favorite_song = models.FavoriteSong(user_id=user_id, song_id=song_id)
        self.db.add(favorite_song)
        await self.db.commit()
        await self.db.refresh(favorite_song)

        return schemas.FavoriteSong.from_orm(favorite_song)

    async def get_user_favorites(self, user_id: int) -> list[schemas.Song]:
        favorite_songs = await self.db.execute(
            select(models.FavoriteSong).filter_by(user_id=user_id).options(selectinload(models.FavoriteSong.song))
        )

        favorite_songs = favorite_songs.scalars().all()
        return [schemas.Song.from_orm(favorite_song.song) for favorite_song in favorite_songs]


favorite_song_facade = FavoriteSongFacade()
