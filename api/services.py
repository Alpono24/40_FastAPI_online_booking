from fastapi import APIRouter, Depends, Request, Security
from sqlalchemy.orm import Session
from models.service import Service
from schemas.service import ServiceCreate, ServiceList, ServiceUpdate
from core.database import get_db
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from collections import OrderedDict
from models.user import User
from core.auth import get_current_user, SECURITY_SCHEME

router = APIRouter()


@router.get("/")
async def get_services(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services


@router.get("/{service_id}")
async def get_service(service_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    return service


@router.post("/", response_model=ServiceList)
async def create_service(service: ServiceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = service.model_dump()
    new_service = Service(
        title=data.get("title"),
        description=data.get("description"),
        start_time=data["start_time"],
        end_time=data["end_time"]
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    ordered_data = OrderedDict([
        ("id", new_service.id),
        ("title", new_service.title),
        ("description", new_service.description),
        ("start_time", new_service.start_time.isoformat()),
        ("end_time", new_service.end_time.isoformat())
    ])
    return ordered_data


@router.delete("/{service_id}")
async  def delete_service(service_id: int, current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    service_to_delete = db.query(Service).filter(Service.id == service_id).first()
    if not service_to_delete:
        raise HTTPException(status_code=404, detail="Сервис не найден")
    db.delete(service_to_delete)
    db.commit()
    return {"message": "Сервис успешно удалён"}


@router.put("/{service_id}")
async def update_service(service_id: int, updates: ServiceUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_service = (db.query(Service)
                        .options(joinedload(Service.bookings))
                        .filter(Service.id == service_id)
                        .first())

    if not existing_service:
        raise HTTPException(status_code=404, detail="Сервис не найден")

    updated_fields = updates.model_dump(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(existing_service, field, value)

    db.commit()
    db.refresh(existing_service)

    return existing_service
















