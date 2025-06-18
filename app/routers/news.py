from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from app.config import settings
import httpx
from app.core.rate_limiter import limiter
from fastapi import Request

router = APIRouter(prefix="/news", tags=["News"])

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

@router.get("/")
@limiter.limit("5/minute")
async def get_news(request: Request, search: str = Query(None), user=Depends(get_current_user)):
    params = {
        "apiKey": settings.NEWS_API_KEY,
        "country": "us",
    }
    if search:
        params["q"] = search

    async with httpx.AsyncClient() as client:
        response = await client.get(NEWS_API_URL, params=params)
        return response.json()
