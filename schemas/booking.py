from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import phonenumbers

class BookingBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone_number: str = Field(min_length=1, max_length=50)
    user_email: EmailStr
    service_id: int

    @validator('phone_number')
    def validate_phone_number(cls, value):
        """
        Валидация белорусского номера телефона.
        Поддерживаются форматы: '+375 XX XXX XXXX', '375XX...'.
        """
        try:
            parsed_number = phonenumbers.parse(value, 'BY')

            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Недействительный номер телефона.")

            if phonenumbers.region_code_for_number(parsed_number) != 'BY':
                raise ValueError("Телефонный номер должен быть из Республики Беларусь.")

        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Неверный формат номера телефона.")

        return value



class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    user_email: Optional[EmailStr] = None
    service_id: Optional[int] = None



class BookingList(BookingBase):
    id: int

    class Config:
        from_attributes = True