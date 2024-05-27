import os

import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException, APIRouter, Response
from async_db import get_db
from facades.favorite_song_facade import favorite_song_facade
from facades.playlist_facade import playlist_facade
from users import get_current_user
from facades.file_facade import FILE_MANAGER
from facades.song_facade import song_facade

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


@router.post('/playlists/', response_model=schemas.Playlist)
async def create_playlist(
        playlist_data: schemas.PlaylistCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    db_playlist = await playlist_facade.create_playlist(user_id=current_user.id, playlist_data=playlist_data)
    return db_playlist


@router.post('/playlists/songs/', response_model=schemas.PlaylistSong)
async def add_song_to_playlist(
        playlist_song_data: schemas.PlaylistSongCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    db_playlist_song = await playlist_facade.add_song_to_playlist(playlist_song_data=playlist_song_data)
    return db_playlist_song


@router.get('/playlists/{playlist_id}/songs/', response_model=schemas.PlaylistWithSongs)
async def get_playlist_songs(
        playlist_id: int,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    playlist_songs = await playlist_facade.get_playlist_songs(user_id=current_user.id, playlist_id=playlist_id)
    return playlist_songs


@router.get('/playlists/', response_model=list[schemas.Playlist])
async def get_user_playlists(
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_playlists = await playlist_facade.get_user_playlists(user_id=current_user.id)
    return user_playlists


@router.get('songs/{song_id}/')
async def download_song(
        song_id: int,
        current_user: models.User = Depends(get_current_user),
):
    song = await song_facade.get_song(song_id=song_id)
    file_path = song.file_path
    file_content = await FILE_MANAGER.get_file(file_path)

    return Response(content=file_content, media_type='audio/mpeg',
                    headers={'Content-Disposition': f"attachment; filename='{os.path.basename(file_path)}'"
                             })
