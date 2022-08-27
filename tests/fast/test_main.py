import pytest
from httpx import AsyncClient

from app.internal.models import User

users: list[User] = [
    User(
        uuid="855d465d-dd58-4982-947f-6854b942de8b",
        username="test@beckelman.net",
        first_name="Test",
        last_name="User",
    )
]


@pytest.mark.asyncio
async def test_equals(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
