from uuid import uuid4

import pytest

from app.notes.models import Note
from app.notes.notes_service import NotesService, NotFoundException


async def test_get_note_returns_note():
    note_id = uuid4()
    user_id = uuid4()

    class FakeRepo:
        async def findOne(self):
            return Note(note="Note 1", uuid=note_id, user_id=user_id)

    service = NotesService({"user_id": user_id}, FakeRepo)

    result = await service.get_note(note_id)

    assert result.uuid == note_id


async def test_get_note_errors_when_note_not_found():
    user_id = uuid4()
    not_found_id = uuid4()

    class FakeRepo:
        async def findOne(self):
            return None

    service = NotesService({"user_id": user_id}, FakeRepo)

    with pytest.raises(NotFoundException):
        await service.get_note(not_found_id)
