from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ArtistBase(BaseModel):
    name: str
    description: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: int

    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    title: str
    artist_id: int
    description: str


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int

    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True
