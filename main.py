from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from auth import hash_password,verify_password,create_token,verify_token
from database import init_db, create_user,get_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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
    
    token = create_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    return user