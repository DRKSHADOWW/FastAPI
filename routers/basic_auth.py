from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "12345"
    },
     "andres2": {
        "username": "andres2",
        "full_name": "Murillo2",
        "email": "andresdavid13052@hotmail.com",
        "disabled": True,
        "password": "123452"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
    
async def current_user(token: str = Depends(oauth2)):
    user  = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
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
    if not form.password == user.password:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "La contraseña no es correcta"
        )
        
    return {"access_token": user.username, "token_type": "bearer"}
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
    
