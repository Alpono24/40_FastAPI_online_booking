from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    user_email: EmailStr
    phone_number: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserInDB(UserBase):
    hashed_password: str
    created_at: datetime

