from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Define a model for user data
class User(BaseModel):
    id: int
    name: str
    email: str


# In-memory "database" of users
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]


# Always say "Hello"
@app.get("/")
def root():
    return {"message": "Hello World 🧉"}


# Endpoint to get the list of users
@app.get("/api/users", response_model=List[User])
async def get_users():
    return users_db


# Endpoint to create a new user
@app.post("/api/users", response_model=User)
async def create_user(user: User):
    # Use model_dump instead of dict to convert the Pydantic model to a dictionary
    users_db.append(user.model_dump())
    return user


# Endpoint to get a user by ID
@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
