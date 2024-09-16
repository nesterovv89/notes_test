from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


async def create_note(
        new_note: NoteCreate,
        session: AsyncSession,
) -> Note:
    new_note_data = new_note.dict()
    db_note = Note(**new_note_data)

    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note

async def get_note_id_by_title(note_title: str, session: AsyncSession) -> Optional[int]:

    db_note_id = await session.execute(
        select(Note.id).where(
            Note.title == note_title
        )
    )
    db_note_id = db_note_id.scalars().first()
    return db_note_id


async def get_note_by_id(
        note_id: int,
        session: AsyncSession,
) -> Optional[Note]:
    db_note = await session.get(Note, note_id)
    return db_note


async def read_all_notes_from_db(
        session: AsyncSession,
) -> list[Note]:
    db_notes = await session.execute(select(Note))
    notes = db_notes.scalars().all()
    formatted_notes = []
    for note in notes:
        note.create_date = note.create_date.isoformat()
        note.update_date = note.update_date.isoformat()
        formatted_notes.append(note)
    return formatted_notes


async def update_note(
        db_note: Note,
        note_in: NoteUpdate,
        session: AsyncSession,
) -> Note:
    obj_data = jsonable_encoder(db_note)
    update_data = note_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_note, field, update_data[field])
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note


async def delete_note(
        db_note: Note,
        session: AsyncSession,
) -> Note:
    await session.delete(db_note)
    await session.commit()
    return db_note