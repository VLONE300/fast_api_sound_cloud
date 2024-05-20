from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import admin

import users
import views
from async_db import get_db
from facades.artist_facade import artist_facade
from facades.album_facade import album_facade
from facades.genre_facade import genre_facade
from facades.song_facade import song_facade
from facades.favorite_song_facade import favorite_song_facade


def set_db_for_facade(db):
    artist_facade.set_db(db)
    album_facade.set_db(db)
    genre_facade.set_db(db)
    song_facade.set_db(db)
    favorite_song_facade.set_db(db)


OAUTH2_SCHEME = OAuth2PasswordBearer('users/login/')

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    async for db in get_db():
        set_db_for_facade(db)
        break


app.include_router(admin.router)
app.include_router(users.router)
app.include_router(views.router)


@app.get("/")
async def index():
    return {'message': 'Hello World'}
