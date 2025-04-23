from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == user.email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10, exclude_user_id: int = None, search: str = None):
    query = db.query(User)
    if exclude_user_id:
        query = query.filter(User.id != exclude_user_id)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def get_friend_suggestions(db: Session, user_id: int, limit: int = 5):
    # Simplified: Randomly select users excluding self and friends
    friends = db.query(Friend).filter(
        (Friend.user_id == user_id) | (Friend.friend_id == user_id),
        Friend.status == FriendStatus.ACCEPTED
    ).all()
    friend_ids = {f.friend_id if f.user_id == user_id else f.user_id for f in friends}
    friend_ids.add(user_id)
    return db.query(User).filter(~User.id.in_(friend_ids)).limit(limit).all()