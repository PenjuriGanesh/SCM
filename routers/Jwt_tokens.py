from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError # type: ignore
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from Models.model import Signup_details
from config.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, User_details
from typing import Dict

# OAuth2PasswordBearer for extracting the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Function to create an access token with an optional expiration time
def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(email:str):
    # print("email",email)
    Existing_user= User_details.find_one({'email': email})
    # print("Existing_user",Existing_user)
    if not  Existing_user:
        return None
    else:
        return Existing_user

def decode_token(token: str) -> Signup_details:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    if token is None:
        return None

    token = token.removeprefix("Bearer").strip()
    # print("tokentoken222",token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("payload",payload)
        username: str = payload.get("email")
        # print("username",username)
        if username is None:
            raise credentials_exception
        user = get_user(username)
        # print("useruser")
        return user
    except JWTError as e:
        print(e)
        raise credentials_exception

def verify_token(token: str = Depends(oauth2_scheme)):
    # print(f"Received token: {token}")  # Debugging line
    try:
        payload = decode_token(token)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


# Function to get the current user from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials"
    )
    if not token:
        raise credentials_exception
    try:
        token = token.removeprefix("Bearer").strip()  # Remove "Bearer" prefix
        payload = decode_token(token)
        email = payload.get("email")
        if not email:
            raise credentials_exception
        # Assuming `User_details` is your MongoDB collection
        user_data = User_details.find_one({"email": email})
        if not user_data:
            raise credentials_exception
        return user_data
    except JWTError:
        raise credentials_exception
