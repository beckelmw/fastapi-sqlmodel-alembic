import uuid as uuid_pkg

from sqlmodel import Field, Relationship, SQLModel

from ..internal.models import TimestampModel, User, UUIDModel


class NoteBase(SQLModel):
    note: str


class Note(NoteBase, UUIDModel, TimestampModel, table=True):
    __tablename__ = "notes"
    user_id: uuid_pkg.UUID = Field(default=None, foreign_key="users.uuid")
    user: User = Relationship(back_populates="users")


class NoteRequest(NoteBase):
    pass


class NoteResponse(SQLModel):
    uuid: uuid_pkg.UUID
    note: str
