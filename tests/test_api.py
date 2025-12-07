import pytest
from httpx import AsyncClient
from app.main import app
import fakeredis.aioredis as fakeredis_module

@pytest.fixture
async def fake_redis(monkeypatch):
    """
    Создаём fake redis и подменяем в модуле redis_client глобальную переменную.
    """
    fake = fakeredis_module.FakeRedis(decode_responses=True)
    import app.redis_client as redis_module
    redis_module.redis_client = fake
    yield fake
    await fake.close()

@pytest.mark.asyncio
async def test_create_get_update_delete(fake_redis):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"phone": "+7 (999) 111-22-33", "address": "ул. Тестовая, д. 1"}
        r = await ac.post("/phones", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["phone"] == "+79991112233"
        assert data["address"] == "ул. Тестовая, д. 1"

        r2 = await ac.post("/phones", json=payload)
        assert r2.status_code == 409

        r3 = await ac.get("/phones/+7%20999%20111-22-33")
        assert r3.status_code == 200
        got = r3.json()
        assert got["phone"] == "+79991112233"
        assert got["address"] == "ул. Тестовая, д. 1"

        r4 = await ac.put("/phones/+79991112233", json={"address": "Новая ул., 2"})
        assert r4.status_code == 200
        up = r4.json()
        assert up["address"] == "Новая ул., 2"

        r5 = await ac.delete("/phones/+79991112233")
        assert r5.status_code == 204

        r6 = await ac.get("/phones/+79991112233")
        assert r6.status_code == 404
