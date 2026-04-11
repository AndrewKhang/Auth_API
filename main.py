from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from auth import hash_password,verify_password,create_token,verify_token,create_refresh_token
from database import init_db, create_user,get_user,get_refresh_token,save_refresh_token,delete_refresh_tokens
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
app = FastAPI()
init_db() 
class UserRegister(BaseModel):
    username: str
    password: str
    
@app.post("/register")
def hashpassword(user:UserRegister):
    hashed = hash_password(user.password)
    create_user(user.username, hashed)
    return {"message": "User registered successfully!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = get_user(form_data.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password!")
    
    delete_refresh_tokens(db_user["id"])
    token = create_token(form_data.username)
    refresh_token = create_refresh_token(form_data.username)
    expires_at = datetime.utcnow() + timedelta(days=7)
    save_refresh_token(db_user["id"], refresh_token, expires_at)
    return {"access_token": token, "token_type": "bearer","refresh_token": refresh_token}

@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    return user

@app.post("/refresh")
def refresh(refresh_token: str):
    # 1. find refresh token in database
    db_token = get_refresh_token(refresh_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token!")
    # 2. verify token expired?
    username = verify_token(refresh_token)
    # 3. create new access token 
    new_access_token= create_token(username)
    # 4. return new access token 
    return {"new_access_token": new_access_token, "token_type": "bearer"}

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    # 1. take username from access token
    username = verify_token(token)

    # 2. get user_id
    user = get_user(username)
    user_id = user["id"]
    delete_refresh_tokens( user_id)

    return {"message": "Logged out successfully!"}