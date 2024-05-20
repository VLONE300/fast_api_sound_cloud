import models
import schemas
from facades.base_facade import BaseFacade


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


song_facade = SongFacade()
