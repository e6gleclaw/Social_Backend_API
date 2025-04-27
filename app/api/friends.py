from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.friend import Friend, FriendRequest, FriendStatus
from app.crud.friend import create_friend_request, update_friend_request, get_friend_requests, get_friends
from app.api.users import get_current_user
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema
import random

router = APIRouter()

@router.post("/request", response_model=Friend)
def send_friend_request(
    friend_request: FriendRequest,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friend = create_friend_request(db, current_user.id, friend_request.friend_id)
    return friend

@router.put("/request/{request_id}", response_model=Friend)
def update_friend_request_status(
    request_id: int,
    status: FriendStatus,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friend_request = db.query(Friend).filter(Friend.id == request_id, Friend.friend_id == current_user.id).first()
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found or unauthorized")
    friend = update_friend_request(db, request_id, status)
    return friend

@router.get("/requests", response_model=List[Friend])
def list_friend_requests(current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    requests = get_friend_requests(db, current_user.id)
    return requests

@router.get("/", response_model=List[UserSchema])
def list_friends(current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    friends = get_friends(db, current_user.id)
    return friends

@router.get("/suggestions", response_model=List[dict])
async def get_friend_suggestions(
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all users except current user and existing friends
    existing_friends = db.query(Friend).filter(
        Friend.user_id == current_user.id,
        Friend.status == "accepted"
    ).all()
    friend_ids = [f.friend_id for f in existing_friends]
    
    # Get potential friends (excluding current user and existing friends)
    potential_friends = db.query(UserModel).filter(
        UserModel.id != current_user.id,
        UserModel.id.not_in_(friend_ids)
    ).all()
    
    # Randomly select 5 users (or less if not enough)
    suggestions = random.sample(
        potential_friends,
        min(5, len(potential_friends))
    )
    
    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "bio": user.bio
        }
        for user in suggestions
    ]