from sqlalchemy.orm import Session
from app.models.friend import Friend, FriendStatus
from app.schemas.friend import FriendRequest
from fastapi import HTTPException
from app.models.user import User 


def create_friend_request(db: Session, user_id: int, friend_id: int):
    if user_id == friend_id:
        raise HTTPException(status_code=400, detail="Cannot send friend request to self")
    existing_request = db.query(Friend).filter(
        ((Friend.user_id == user_id) & (Friend.friend_id == friend_id)) |
        ((Friend.user_id == friend_id) & (Friend.friend_id == user_id))
    ).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="Friend request already exists")
    friend_request = Friend(user_id=user_id, friend_id=friend_id, status=FriendStatus.PENDING)
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return friend_request

def update_friend_request(db: Session, request_id: int, status: FriendStatus):
    friend_request = db.query(Friend).filter(Friend.id == request_id).first()
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    friend_request.status = status
    db.commit()
    db.refresh(friend_request)
    return friend_request

def get_friend_requests(db: Session, user_id: int, status: FriendStatus = FriendStatus.PENDING):
    return db.query(Friend).filter(Friend.friend_id == user_id, Friend.status == status).all()

def get_friends(db: Session, user_id: int):
    friends = db.query(Friend).filter(
        ((Friend.user_id == user_id) | (Friend.friend_id == user_id)),
        Friend.status == FriendStatus.ACCEPTED
    ).all()
    friend_ids = [
        f.friend_id if f.user_id == user_id else f.user_id
        for f in friends
    ]
    return db.query(User).filter(User.id.in_(friend_ids)).all()