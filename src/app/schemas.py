from pydantic import BaseModel, Field, constr

PHONE_PATTERN = r"^\+7[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$"

class PhoneCreate(BaseModel):
    phone: constr(pattern=PHONE_PATTERN) = Field(
        ...,
        example="+79991234567",
        description="Номер телефона в формате +7XXXXXXXXXX или +7(XXX)XXXXXXX"
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
