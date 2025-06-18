from fastapi import APIRouter, Query
from app.config import settings
from app.services.redis_client import r
import httpx
import json
from app.core.rate_limiter import limiter
from fastapi import Request

router = APIRouter(prefix="/weather", tags=["Weather"])

WEATHER_URL = "https://api.weatherapi.com/v1/current.json"

@router.get("/")
@limiter.limit("10/minute")
async def get_weather(request: Request, city: str = Query(..., min_length=2)):
    cache_key = f"weather:{city.lower()}"
    cached = r.get(cache_key)

    if cached:
        print(f"Cache hit for {city}")
        return json.loads(cached)
    else:
        print(f"Fetching new data for {city} from API")

    params = {
        "key": settings.WEATHER_API_KEY,
        "q": city,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "Failed to fetch weather")}

        # Store in Redis for 10 minutes
        r.setex(cache_key, 600, json.dumps(data))

        return data
