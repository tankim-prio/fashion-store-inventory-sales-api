from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str | None = Field(default=None, max_length=20)


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str
    phone: str | None = Field(default=None, max_length=20)


class UserUpdate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    role: str
    is_active: bool
    phone: str | None = Field(default=None, max_length=20)


class UserProfileUpdate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    phone: str | None = Field(default=None, max_length=20)

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None):
        if value is None:
            return value

        value = value.strip()
        return value or None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    role: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
