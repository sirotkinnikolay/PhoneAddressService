import os
import logging
from fastapi import FastAPI, HTTPException, status, Path
from fastapi.responses import JSONResponse
from . import schemas
from .redis_client import init_redis_pool, close_redis_pool, get_redis
from .utils import normalize_phone

logger = logging.getLogger("phone-address-api")
logging.basicConfig(level=logging.INFO)

PHONE_REGEX = r"^\+7[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$"

app = FastAPI(title="Phone-Address service", version="1.0")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@app.on_event("startup")
async def startup():
    await init_redis_pool(REDIS_URL)

@app.on_event("shutdown")
async def shutdown():
    await close_redis_pool()


@app.get("/phones/{phone}", response_model=schemas.PhoneOut)
async def get_address(
    phone: str = Path(
        ...,
        pattern=PHONE_REGEX,
        description="Номер телефона в формате +7XXXXXXXXXX или +7(XXX)XXXXXXX"
    )
) -> dict[str, str]:
    """
    Получение адреса по номеру телефона.
    """
    key = normalize_phone(phone)
    rc = get_redis()
    if rc is None:
        raise HTTPException(status_code=503, detail="Redis client not initialized")
    value = await rc.get(key)
    if value is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found")
    return {"phone": key, "address": value}

@app.post("/phones", status_code=status.HTTP_201_CREATED)
async def create_mapping(item: schemas.PhoneCreate) -> JSONResponse:
    """
    Создание новой записи (номер телефона, адрес).
    """
    key = normalize_phone(item.phone)
    rc = get_redis()
    if rc is None:
        raise HTTPException(status_code=503, detail="Redis client not initialized")
    existed = await rc.exists(key)
    if existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone already exists")
    await rc.set(key, item.address)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"phone": key, "address": item.address})

@app.put("/phones/{phone}", response_model=schemas.PhoneOut)
async def update_mapping(
    phone: str = Path(
        ...,
        pattern=PHONE_REGEX,
        description="Номер телефона в формате +7XXXXXXXXXX или +7(XXX)XXXXXXX"
    ),
    payload: schemas.AddressUpdate = ...
) -> dict[str, str]:
    """
    Обновление адреса.
    """
    key = normalize_phone(phone)
    rc = get_redis()
    if rc is None:
        raise HTTPException(status_code=503, detail="Redis client not initialized")
    existed = await rc.exists(key)
    if not existed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found")
    await rc.set(key, payload.address)
    return {"phone": key, "address": payload.address}

@app.delete("/phones/{phone}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mapping(
    phone: str = Path(
        ...,
        pattern=PHONE_REGEX,
        description="Номер телефона в формате +7XXXXXXXXXX или +7(XXX)XXXXXXX"
    )
) -> JSONResponse:
    """
    Удаление записи.
    """
    key = normalize_phone(phone)
    rc = get_redis()
    if rc is None:
        raise HTTPException(status_code=503, detail="Redis client not initialized")
    deleted = await rc.delete(key)
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

