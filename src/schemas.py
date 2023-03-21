from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=15)
    email: EmailStr
    phone: str = Field(min_length=6, max_length=16)
    birthday: date
    additional_info: str = Field(min_length=3, max_length=300)


class ContactResponse(BaseModel):
    id: int
    first_name: str = "Andrew"
    last_name: str = "Lastname"
    email: EmailStr = "andrew.lastname@gmail.com"
    phone: str = "+380958745896"
    birthday: date = date(year=1986, month=2, day=28)
    additional_info: str = "some info"

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserModelPassword(BaseModel):
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
