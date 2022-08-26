from uuid import UUID

from fastapi import APIRouter, Body, Depends, Response, status

from ..dependencies import get_current_user
from ..internal.repository import Repository, RepositoryProtocol
from .models import Note, NoteRequest, NoteResponse
from .notes_service import NotesService

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[Depends(get_current_user)],
)


def notes_service(
    user: dict = Depends(get_current_user),
    repo: RepositoryProtocol[Note] = Depends(Repository(model=Note)),
) -> NotesService:
    return NotesService(user, repo)


@router.get("/", response_model=list[NoteResponse])
async def get_notes(service: NotesService = Depends(notes_service)) -> list[Note]:
    return await service.get_notes()


@router.get("/{id}", response_model=NoteResponse)
async def get_note(id: UUID, service: NotesService = Depends(notes_service)) -> Note:
    return await service.get_note(id)


@router.post("/", status_code=201)
async def create_note(
    response: Response,
    note: NoteRequest = Body(...),
    notes_service: NotesService = Depends(notes_service),
) -> Note:
    new_note: Note = await notes_service.add_note(note)
    response.headers.append("location", f"/notes/{new_note.uuid}")
    return new_note


@router.patch("/{id}", response_model=NoteResponse)
async def update_note(
    id: UUID,
    note: NoteRequest = Body(...),
    service: NotesService = Depends(notes_service),
) -> Note:
    return await service.update_note(id, note)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: UUID, service: NotesService = Depends(notes_service)) -> bool:
    return await service.delete_note(id)
