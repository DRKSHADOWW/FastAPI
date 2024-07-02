from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 3
SECRET = "$2y$10$beh1auTBy.DrT.GbAEsOWOUHf4VOyo8x5tq8RmzIpkS/j6PowdcoO"


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str
    
users_db = {
    "andres": {
        "username": "andres",
        "full_name": "Murillo",
        "email": "andresdavid1305@hotmail.com",
        "disabled": False,
        "password": "$2y$10$vXN56QCTjl6261lXT/h6Xuga7Nh5WuGak8der86705UwlMQKByQnO"
    },
     "andres2": {
        "username": "andres2",
        "full_name": "Murillo2",
        "email": "andresdavid13052@hotmail.com",
        "disabled": True,
        "password": "$2y$10$2BIXyiiWhuJj5GxKc6wrT./233lliRV88W0DELCPFHuaFXAKLsqAK"
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
         raise exception
     
    return search_user(username)
    
       
        
async def current_user(user: User = Depends(auth_user)):   
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
            
        )
    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto"
        )
        
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "La contraseña no es correcta"
        )
         
    
    access_token = {"sub": user.username, 
                    "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION) }
        
    
        
    return {"access_token": jwt.encode(access_token, SECRET,  algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
    