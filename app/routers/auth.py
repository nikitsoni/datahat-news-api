from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from app.schemas.user import UserSignup, UserLogin
from app.models.user import User
from app.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.services.redis_client import r
from app.config import settings
from app.schemas.user import RefreshTokenRequest
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User registered successfully."}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    r.setex(f"refresh:{db_user.email}", settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):

    refresh_token = payload.refresh_token
    try:
        token_data = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if token_data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        email = token_data.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Optional: check Redis
    stored = r.get(f"refresh:{email}")
    if stored != refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")

    new_access_token = create_access_token({"sub": email})
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }