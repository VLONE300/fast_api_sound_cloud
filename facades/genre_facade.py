import models
import schemas
from facades.base_facade import BaseFacade


class GenreFacade(BaseFacade):
    async def create_genre(self, genre_data: schemas.GenreCreate) -> models.Genre:
        db_genre = models.Genre(name=genre_data.name)
        self.db.add(db_genre)
        await self.db.commit()
        await self.db.refresh(db_genre)
        return db_genre


genre_facade = GenreFacade()
