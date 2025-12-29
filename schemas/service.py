from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ServiceBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    @validator('start_time', 'end_time', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValueError(f'Invalid date format "{value}"')
        return value


class ServiceList(ServiceBase):
    id: int

    class Config:
        from_attributes = True