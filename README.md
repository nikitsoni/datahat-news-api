# 📰 News & Weather Aggregator API

A FastAPI backend that provides real-time News (with authentication) and Weather (public) data using external APIs. Built for take-home assignment.

---

## 🚀 Features

- ✅ Signup/Login with JWT authentication
- ✅ Access-protected `/news` endpoint using NewsAPI
- ✅ Public `/weather` endpoint using OpenWeatherMap
- ✅ Redis caching to reduce API calls
- ✅ Refresh token support
- ✅ Rate limiting with SlowAPI
- ✅ Dockerized (with Redis)

---

## 🛠️ Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy + SQLite
- Redis
- Docker + Docker Compose
- NewsAPI.org
- OpenWeatherMap.org

---

## 📦 Installation

### 🔧 Local Setup

```bash
git clone https://github.com/yourusername/news-weather-api.git
cd news-weather-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


## 📦 Docker Setup

```bash
docker-compose up --build
