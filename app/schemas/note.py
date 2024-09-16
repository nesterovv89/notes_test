from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


class NoteBase(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    text: Optional[str]


class NoteCreate(NoteBase):
    title: str = Field(..., min_length=1, max_length=50)
    


class NoteUpdate(NoteBase):
    #update_date: datetime = Field(..., example='2023-12-21T12:34:56')
    @validator('title')
    def title_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Заголовок не может быть пуст')
        return value


class NoteDB(NoteCreate):
    id: int
    create_date: datetime
    update_date: Optional[datetime]

    class Config:
        orm_mode = True
