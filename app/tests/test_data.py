from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.friend import Friend
from app.core.security import get_password_hash
import random
from faker import Faker
import bcrypt

fake = Faker()

def create_test_users(db: Session, count: int = 10):
    users = []
    for _ in range(count):
        # Generate a unique username
        username = fake.user_name()
        while db.query(User).filter(User.username == username).first():
            username = fake.user_name()
            
        user = User(
            username=username,
            email=fake.email(),
            hashed_password=get_password_hash("test123"),
            full_name=fake.name(),
            bio=fake.text(max_nb_chars=200)
        )
        db.add(user)
        users.append(user)
    db.commit()
    return users

def create_test_friendships(db: Session, users: list, max_friends: int = 5):
    for user in users:
        # Randomly select friends for each user
        potential_friends = [u for u in users if u.id != user.id]
        num_friends = random.randint(1, min(max_friends, len(potential_friends)))
        friends = random.sample(potential_friends, num_friends)
        
        for friend in friends:
            # Create friendship in both directions
            friendship1 = Friend(user_id=user.id, friend_id=friend.id)
            friendship2 = Friend(user_id=friend.id, friend_id=user.id)
            db.add(friendship1)
            db.add(friendship2)
    
    db.commit()

def populate_test_data():
    db = next(get_db())
    try:
        # Create test users
        users = create_test_users(db)
        # Create friendships
        create_test_friendships(db, users)
        print("Test data populated successfully!")
    except Exception as e:
        print(f"Error populating test data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_test_data() 