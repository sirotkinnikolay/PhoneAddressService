from pydantic import BaseModel, Field

class PhoneCreate(BaseModel):
    phone: str = Field(
        ...,
        example="+79991234567",
        description="Номер телефона в международном формате"
    )
    address: str = Field(
        ...,
        example="ул. Ленина, д. 1, кв. 1",
        description="Полный адрес"
    )

class AddressUpdate(BaseModel):
    address: str

class PhoneOut(BaseModel):
    phone: str = Field(
        ...,
        example="+79161234567",
        description="Номер телефона в международном формате"
    )
    address: str = Field(
        ...,
        example="ул. Ленина, д. 10, кв. 1",
        description="Полный адрес"
    )
