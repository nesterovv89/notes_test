from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.note import create_note, get_note_id_by_title, read_all_notes_from_db, update_note, get_note_by_id, delete_note
from app.schemas.note import NoteCreate, NoteDB, NoteUpdate
from app.models.note import Note


router = APIRouter(prefix='/notes', tags=['Notes'])


@router.post('/', response_model=NoteDB, response_model_exclude_none=True)
async def create_new_note(
        note: NoteCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_title_duplicate(note.title, session)
    new_note = await create_note(note, session)
    return new_note


@router.get(
    '/',
    response_model=list[NoteDB],
    response_model_exclude_none=True,
)
async def get_all_notes(
        session: AsyncSession = Depends(get_async_session),
):
    all_notes = await read_all_notes_from_db(session)
    return all_notes


@router.patch(
    '/{note_id}',
    response_model=NoteDB,
    response_model_exclude_none=True,
)
async def partially_update_note(
        note_id: int,
        obj_in: NoteUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    note = await check_note_exists(
        note_id, session
    )

    if obj_in.title is not None:
        await check_title_duplicate(obj_in.title, session)

    note = await update_note(
        note, obj_in, session
    )
    return note


@router.delete(
    '/{note_id}',
    response_model=NoteDB,
    response_model_exclude_none=True,
)
async def remove_note(
        note_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    note = await check_note_exists(
        note_id, session
    )
    note = await delete_note(
        note, session
    )
    return note
    

async def check_title_duplicate(
        note_title: str,
        session: AsyncSession,
) -> None:
    note_id = await get_note_id_by_title(note_title, session)
    if note_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Заметка с таким заголовком существует',
        )


async def check_note_exists(
        note_id: int,
        session: AsyncSession,
) -> Note:
    note = await get_note_by_id(
        note_id, session
    )
    if note is None:
        raise HTTPException(
            status_code=404,
            detail='Заметка не найдена'
        )
    return note 