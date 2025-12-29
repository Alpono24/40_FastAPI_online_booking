# from fastapi import FastAPI
# from core.database import engine, get_db
# from api import services, bookings, register
# from models.base import Base
#
# app = FastAPI()
#
# app.include_router(register.router, prefix="/register", tags=["Register"])
# app.include_router(services.router, prefix="/services", tags=["Services"])
# app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
#
#
# Base.metadata.create_all(bind=engine)


from fastapi import FastAPI, Security, Depends
from starlette.status import HTTP_403_FORBIDDEN
from core.database import engine, get_db
from api import services, bookings, register
from models.base import Base

# Новая схема авторизации Bearer


app = FastAPI()


# app.include_router(register.router, prefix="/d", tags=["Index"])
app.include_router(register.router, prefix="/register", tags=["Register"])
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])


# Объединяем собственную схему безопасности с автоматической генерацией документации
original_openapi_schema = app.openapi_schema
if original_openapi_schema:
    original_openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    original_openapi_schema["security"] = [{"BearerAuth": []}]
else:
    original_openapi_schema = {}

app.openapi_schema = original_openapi_schema


Base.metadata.create_all(bind=engine)


