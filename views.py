import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException, APIRouter
from async_db import get_db
from facades.favorite_song_facade import favorite_song_facade
from users import get_current_user
from facades.file_facade import FILE_MANAGER
from facades.song_facade import song_facade
from facades.genre_facade import genre_facade

router = APIRouter(
    prefix="/api",
    tags=["API"],
)


@router.post('/favorites/', response_model=schemas.FavoriteSong)
async def add_favorite_song(
        song_data: schemas.FavoriteSongCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    favorite_song = await favorite_song_facade.add_favorite_song(song_id=song_data.song_id, user_id=current_user.id)

    return favorite_song


@router.get('/favorites/', response_model=list[schemas.Song])
async def get_user_favorite(
        current_user: models.User = Depends(get_current_user),
):
    favorite_songs = await favorite_song_facade.get_user_favorites(user_id=current_user.id)
    return favorite_songs


@router.get('/songs/genre/{genre_id}/', response_model=list[schemas.Song])
async def get_song_by_genre(
        genre_id: int,
        current_user: models.User = Depends(get_current_user),
):
    songs = await song_facade.get_songs_by_genre(genre_id=genre_id)
    return songs
