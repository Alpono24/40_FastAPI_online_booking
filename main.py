from fastapi import FastAPI
from core.database import engine
from api import services, bookings, register
from models.base import Base


app = FastAPI()

app.include_router(register.router, prefix="/register", tags=["Register"])
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])



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


