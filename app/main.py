import uvicorn  # type: ignore
from fastapi import Body, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from .auth.auth_service import AuthService
from .auth.models import LoginResponse
from .dependencies import auth_service, get_current_user
from .internal.db import AsyncSession, get_session
from .internal.exceptions import ServiceException
from .internal.models import UserCreate
from .internal.repository import Repository
from .internal.unit_of_work import UnitOfWork
from .notes.models import Note
from .notes.notes_router import router as notes_router

app = FastAPI()


# https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
@app.exception_handler(ServiceException)
async def service_exception_handler(
    request: Request, exc: ServiceException
) -> JSONResponse:
    headers: dict | None = None
    if exc.code == 401:
        headers = {"WWW-Authenticate": "Bearer"}

    return JSONResponse(
        status_code=exc.code, content={"message": exc.message}, headers=headers
    )


@app.get("/ping")
def pong() -> dict:
    return {"ping": "pong!"}


@app.get("/me")
def me(user: dict = Depends(get_current_user)) -> dict:
    return user


def unit_of_work(session: AsyncSession = Depends(get_session)) -> UnitOfWork[Note]:
    return UnitOfWork(session=session, repository=Repository(model=Note)(session))


@app.get("/uow")
async def uow(
    user: dict = Depends(get_current_user),
    uow: UnitOfWork[Note] = Depends(unit_of_work),
) -> list[Note]:
    async with uow:
        notes = await uow.repo.find(Note.user_id == user["user_id"])

    return notes


@app.post("/signup", tags=["user"], status_code=status.HTTP_200_OK)
async def create_user(
    user: UserCreate = Body(...), auth_service: AuthService = Depends(auth_service)
) -> bool:
    return await auth_service.signup(user)


@app.post("/login", tags=["auth"], response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(auth_service),
) -> LoginResponse:
    return await auth_service.login(form_data.username, form_data.password)


app.include_router(notes_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
