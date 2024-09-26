from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define a model for user data
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(UserCreate):
    id: int


# In-memory "database" of users
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]


# Helper function to get the next available ID
def get_next_id() -> int:
    return max(user["id"] for user in users_db) + 1


# Dependency to simulate database access
async def get_db():
    yield users_db


# Endpoint to get the list of users
@app.get("/api/users", response_model=List[User])
async def get_users(db: List[dict] = Depends(get_db)):
    logger.info("Fetching all users")
    return db


# Endpoint to create a new user
@app.post("/api/users", response_model=User)
async def create_user(user: UserCreate, db: List[dict] = Depends(get_db)):
    new_user = User(id=get_next_id(), **user.model_dump())
    db.append(new_user.model_dump())
    logger.info(f"Created new user: {new_user}")
    return new_user


# Endpoint to get a user by ID
@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: List[dict] = Depends(get_db)):
    user = next((user for user in db if user["id"] == user_id), None)
    if user is None:
        logger.warning(f"User with id {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Fetched user: {user}")
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
