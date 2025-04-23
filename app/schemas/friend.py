from pydantic import BaseModel
from enum import Enum
from typing import Optional

class FriendStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class FriendRequest(BaseModel):
    friend_id: int

class Friend(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: FriendStatus

    class Config:
        from_attributes = True