import bcrypt
import jwt
import os
from fastapi import HTTPException
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def hash_password(password: str) -> str:
    # hash password before saving to database
 pwd_bytes = password.encode('utf-8')     # converting password to array of bytes
 salt = bcrypt.gensalt() # generating the salt
 hashed = bcrypt.hashpw(pwd_bytes, salt) # Hashing the password
 return hashed

def verify_password(password: str, hashed: str) -> bool:
    # compare plain password with hashed password from database
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(username: str) -> str:
    payload = {
        "sub": username,                                    # subject — who is logging
        "exp": datetime.utcnow() + timedelta(hours=1)      # token expired after an hour
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return payload["sub"]  # return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")