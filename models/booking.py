from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    first_name  = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    user_email = Column(String)
    service_id = Column(Integer, ForeignKey("services.id"))
    service = relationship("Service", back_populates="bookings")

