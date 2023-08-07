import jwt
from clients import postgres
from typing import Annotated
from datetime import datetime, timedelta
from passlib.context import CryptContext
from decouple import config
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

# Initialize Security
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = config("JWT_SECRET")

# Initialize Clients
# 1. Database connection
dbClient = postgres.Client(config("DATABASE_URL"))


def create_access_token(username: str) -> str:
    to_encode = {
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "sub": username,
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def authenticate_user(db: postgres.ConnectionClient, username: str, password: str):
    username, dbPassword = db.get_user_with_password(username)
    if not dbPassword:
        return False
    if not passwordContext.verify(password, dbPassword):
        return False
    return username


@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[postgres.ConnectionClient, Depends(dbClient)],
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_unauthorized,
            detail="Incorrect username or password",
        )
    return {"access_token": create_access_token(user), "token_type": "bearer"}
