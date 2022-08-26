import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_can_create_and_retrieve_note(authorized_client: AsyncClient) -> None:
    response = await authorized_client.post(
        "/notes/",
        json={
            "note": "The first note",
        },
    )

    assert response.status_code == 201
    location_header: str = response.headers.get("location")
    assert location_header.startswith("/notes/")

    response = await authorized_client.get(location_header)
    assert response.status_code == 200
    note = response.json()
    assert note["note"] == "The first note"
    assert note["uuid"]


@pytest.mark.asyncio
async def test_can_retrieve_notes(authorized_client: AsyncClient) -> None:
    await authorized_client.post(
        "/notes/",
        json={
            "note": "The first note",
        },
    )

    await authorized_client.post(
        "/notes/",
        json={
            "note": "The second note",
        },
    )

    response = await authorized_client.get("/notes/")
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 2


@pytest.mark.asyncio
async def test_can_delete_note(authorized_client: AsyncClient) -> None:
    response = await authorized_client.post(
        "/notes/",
        json={
            "note": "The first note",
        },
    )

    location_header: str = response.headers.get("location")

    response = await authorized_client.get("/notes/")
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 1

    response = await authorized_client.get(location_header)
    uuid = response.json()["uuid"]
    response = await authorized_client.delete(f"/notes/{uuid}")

    response = await authorized_client.get("/notes/")
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 0
