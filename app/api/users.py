from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import OAuth2PasswordBearer, get_current_user
from app.schemas.user import User, UserUpdate, UserResponse
from app.crud.user import get_user_by_email, get_user_by_id, update_user, get_users, get_friend_suggestions
from jose import JWTError, jwt
from app.core.config import settings
from sqlalchemy import or_

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=User)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
def update_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = update_user(db, current_user.id, user_update)
    return updated_user

@router.get("/", response_model=List[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get users with pagination
    users = db.query(User).filter(
        User.id != current_user.id
    ).offset(offset).limit(page_size).all()
    
    return users

@router.get("/suggestions", response_model=List[User])
def friend_suggestions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    suggestions = get_friend_suggestions(db, current_user.id)
    return suggestions

@router.get("/search", response_model=List[UserResponse])
async def search_users(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Search users by username or full name
    users = db.query(User).filter(
        User.id != current_user.id,
        or_(
            User.username.ilike(f"%{query}%"),
            User.full_name.ilike(f"%{query}%")
        )
    ).offset(offset).limit(page_size).all()
    
    return users