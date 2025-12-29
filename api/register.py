from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database import get_db
from core.auth import get_current_user, hash_password, authenticate_user, create_access_token, SECURITY_SCHEME
from schemas.user import UserCreate
from models.user import User

router = APIRouter()

@router.post("/register/")
async def register(user_create: UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(
            (User.first_name == user_create.first_name) &
            (User.last_name == user_create.last_name) &
            (User.user_email == user_create.user_email) &
            (User.phone_number == user_create.phone_number)
        ).first()
    )

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с такими данными уже зарегистрирован!")

    # Производим регистрацию нового пользователя
    hashed_password = hash_password(user_create.password)
    new_user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        user_email=user_create.user_email,
        phone_number=user_create.phone_number,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    return {"message": "Регистрация прошла успешно"}

@router.post("/login/")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Неправильные учетные данные")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.user_email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/about_me")
async def about_me(current_user: User = Depends(get_current_user)):
    return current_user
