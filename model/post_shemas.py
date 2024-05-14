from typing import List, Optional
from bson import ObjectId
from fastapi import Query
from pydantic import BaseModel, Field, validator
from datetime import datetime

# Schemas de Publicaciones
class NewPost(BaseModel):
    title: Optional[str] = Field(alias="title")
    description: Optional[str] = Field(alias="description")
    tags: Optional[list] = Field(alias="tags")
    genres: str = Field(alias="genres")
    moods: Optional[list] = Field(alias="moods")
    instruments: Optional[list] = Field(alias="instruments")
    bpm: Optional[int] = Field(alias="bpm")
    key: Optional[str] = Field(alias="key")

class Post(NewPost):
    user_id: str = Field(alias="user_id")
    publication_date: datetime = Field(alias="publication_date")
    #beat_info: MusicBase._id = Field(alias="beat_info")

class PostInDB(Post):
    id: Optional[str] = Field(default=None, alias='_id')

    @validator('id', pre=True, always=True)
    def convert_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

class PostShowed(PostInDB):
    likes: int = 0
    dislikes: int = 0
    saves: int = 0
    creator_username: Optional[str] = Field(default=None, alias="creator_username")
    isLiked: Optional[bool] = Field(default=False, alias="isLiked")
    isSaved: Optional[bool] = Field(default=False, alias="isSaved")
    
class SearchPost(BaseModel):
    genre: Optional[str] = None
    bpm: Optional[int] = None
    mood: Optional[str] = None
    instruments: Optional[List[str]] =None
    key: Optional[str] = None
    tags: Optional[List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None

class Tag(BaseModel):
    name: str = Field(alias="name")
    description: str = Field(alias="description")

class Genre(BaseModel):
    name: str = Field(alias="name")
    description: str = Field(alias="description")

class Mood(BaseModel):
    name: str = Field(alias="name")
    description: str = Field(alias="description")

class Instrument(BaseModel):
    name: str = Field(alias="name")
    description: str = Field(alias="description")