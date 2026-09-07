from datetime import date, timedelta
import pytest
from httpx import AsyncClient
from tests.factories import booking_payload


@pytest.mark.asyncio
async def test_booking_http_workflow(client: AsyncClient) -> None:
    payload = booking_payload()
    create_response = await client.post("/bookings", json=payload)
    assert create_response.status_code == 201
    booking_id = create_response.json()["id"]

    get_response = await client.get(f"/bookings/{booking_id}")
    list_response = await client.get(
        "/bookings",
        params={"date": payload["booking_date"], "offset": 0, "limit": 1},
    )

    assert create_response.json()["status"] == "active"
    assert get_response.status_code == 200
    assert get_response.json()["id"] == booking_id
    assert list_response.status_code == 200
    assert [booking["id"] for booking in list_response.json()] == [booking_id]


@pytest.mark.asyncio
async def test_booking_http_errors(client: AsyncClient) -> None:
    payload = booking_payload()
    await client.post("/bookings", json=payload)

    missing_response = await client.get("/bookings/999999")
    missing_cancel_response = await client.delete("/bookings/999999")
    conflict_response = await client.post("/bookings", json=payload)

    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Booking not found"}
    assert missing_cancel_response.status_code == 404
    assert missing_cancel_response.json() == {"detail": "Booking not found"}
    assert conflict_response.status_code == 409
    assert conflict_response.json() == {"detail": "Booking slot is already occupied"}


@pytest.mark.asyncio
async def test_booking_http_cancellation_releases_slot(client: AsyncClient) -> None:
    payload = booking_payload()
    create_response = await client.post("/bookings", json=payload)
    booking_id = create_response.json()["id"]

    cancel_response = await client.delete(f"/bookings/{booking_id}")
    repeated_response = await client.delete(f"/bookings/{booking_id}")
    replacement_response = await client.post("/bookings", json=payload)
    list_response = await client.get("/bookings")

    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"
    assert repeated_response.status_code == 200
    assert repeated_response.json()["status"] == "cancelled"
    assert replacement_response.status_code == 201
    assert replacement_response.json()["id"] != booking_id
    assert [booking["status"] for booking in list_response.json()] == [
        "cancelled",
        "active",
    ]


@pytest.mark.asyncio
async def test_api_documentation_is_available(client: AsyncClient) -> None:
    docs_response = await client.get("/docs")
    redoc_response = await client.get("/redoc")
    openapi_response = await client.get("/openapi.json")

    assert docs_response.status_code == 200
    assert redoc_response.status_code == 200
    assert openapi_response.status_code == 200
    assert set(openapi_response.json()["paths"]["/bookings"]) == {"get", "post"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        booking_payload(name="A1"),
        booking_payload(phone="79991234567"),
        booking_payload(booking_date=date.today() - timedelta(days=1)),
        booking_payload(booking_date=date.today() + timedelta(days=91)),
        booking_payload(booking_time="12:30"),
        booking_payload(guests=0),
        booking_payload(guests=13),
        {**booking_payload(), "guests": 4.5},
    ],
)
async def test_invalid_booking_body_returns_422(
    client: AsyncClient,
    payload: dict[str, object],
) -> None:
    response = await client.post("/bookings", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path",
    [
        "/bookings?date=not-a-date",
        "/bookings?offset=-1",
        "/bookings?limit=0",
        "/bookings?limit=101",
        "/bookings/0",
    ],
)
async def test_invalid_query_or_path_returns_422(
    client: AsyncClient,
    path: str,
) -> None:
    response = await client.get(path)

    assert response.status_code == 422
    assert "detail" in response.json()
