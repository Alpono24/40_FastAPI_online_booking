from pathlib import Path
from dotenv import load_dotenv
import os



BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

MAIL_USERNAME = os.getenv("MAIL_USERNAME", 'alex.ponomarov@mail.ru')
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM", 'alex.ponomarov@mail.ru')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", '30')

DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite:///./reservation.db')

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM='HS256'