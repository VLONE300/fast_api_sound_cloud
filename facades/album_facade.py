import models
import schemas
from facades.base_facade import BaseFacade


class AlbumFacade(BaseFacade):
    async def create_album(self, album_data: schemas.AlbumCreate) -> models.Album:
        db_album = models.Album(title=album_data.title, description=album_data.description,
                                artist_id=album_data.artist_id)
        self.db.add(db_album)
        await self.db.commit()
        await self.db.refresh(db_album)
        return db_album


album_facade = AlbumFacade()
