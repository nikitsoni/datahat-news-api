import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 43200))
    ALGORITHM = "HS256"
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

settings = Settings()
