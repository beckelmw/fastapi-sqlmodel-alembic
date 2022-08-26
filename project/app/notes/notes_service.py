from dataclasses import dataclass
from uuid import UUID

from ..internal.exceptions import ServiceException
from ..internal.repository import RepositoryProtocol
from .models import Note, NoteRequest


@dataclass()
class NotFoundException(ServiceException):
    message: str = "Not found"
    code: int = 404


class NotesService:
    def __init__(
        self,
        user: dict,
        repository: RepositoryProtocol[Note],
    ):
        self.repo = repository
        self.user_id = user["user_id"]

    async def get_notes(self) -> list[Note]:
        return await self.repo.find(Note.user_id == self.user_id)

    async def get_note(self, id: UUID) -> Note:
        note = await self.repo.findOne(Note.uuid == id and Note.user_id == self.user_id)
        if not note:
            raise NotFoundException()
        return note

    async def delete_note(self, id: UUID) -> bool:
        note = await self.get_note(id)
        return await self.repo.delete(note)

    async def add_note(self, note: NoteRequest) -> Note:
        return await self.repo.add(Note(**note.dict(), user_id=self.user_id))

    async def update_note(self, id: UUID, data: NoteRequest) -> Note:
        note: Note = await self.get_note(id)
        updated_note = await self.repo.update(note, Note.from_orm(data))

        if not updated_note:
            raise NotFoundException()

        return updated_note
