from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth import get_current_user
from models.booking import Booking
from models.user import User
from schemas.booking import BookingCreate, BookingList, BookingUpdate
from core.database import get_db
from fastapi import HTTPException
from core.mailer import send_confirmation_email
from sqlalchemy.orm import joinedload


router = APIRouter()


@router.get("/")
async def get_bookings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings


@router.get("/{booking_id}")
async def get_booking(booking_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    return booking


@router.post("/", response_model=BookingList)
async def create_booking(booking: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # await send_confirmation_email(new_booking.user_email, new_booking.service_id)
    return new_booking


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking_to_delete = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_to_delete:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    db.delete(booking_to_delete)
    db.commit()
    return {"message": "Бронирование успешно удалено"}


@router.put("/{booking_id}")
async def update_booking(booking_id: int, updates: BookingUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_booking = (db.query(Booking)
                        .options(joinedload(Booking.service))
                        .filter(Booking.id == booking_id)
                        .first())

    if not existing_booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    updated_fields = updates.model_dump(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(existing_booking, field, value)

    db.commit()
    db.refresh(existing_booking)

    return existing_booking

