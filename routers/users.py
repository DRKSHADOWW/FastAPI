from fastapi import APIRouter, HTTPException
from pydantic import BaseModel 



router = APIRouter()

# inicia el server: uvicorn users:app --reload

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url:str
    age: int
    
users_list = [User(id=1, name = "brais", surname="moure", url="Https://moure.dev", age=35),
              User(id=2,name = "braisre", surname="cadrymoure", url="Https://mourereu.dev", age=55),
              User(id=3,name = "braismo", surname="reumoure", url="Https://mourecar.dev", age=65)]

# @app.get("/usersjson")
# async def usersjson():
#     return [{"name": "Andrés", "surname": "sombra", "url": "https://mouredev.com/python", "age": 23},
#             {"name": "David", "surname": "sangre", "url": "https://mouredev.com/python", "age": 45},
#             {"name": "Murillo", "surname": "aguacaliente", "url": "https://mouredev.com/python", "age": 56}]

@router.get("/users")
async def users():
    return users_list

#path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
    
#Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)
    
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Usuario no encontrado"}
    
# Añadir usuarios POST
@router.post("/user/", status_code=201)
async def add_user(user: User):
     if type(search_user(user.id)) == User:
         raise HTTPException(status_code=204, detail="El usuario ya existe")
     else:  
        users_list.append(user)
        return user
        
# Actualizar Datos PUT
@router.put("/user/")
async def update_user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        return {"Error": "No se ha actualizado el usuario"}
    else:
        return user

# Eliminación
@router.delete("/user/{id}")
async def delete_user(id: int):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            
    if not found:
        return {"Error": "No se ha elimnado el usuario"}
        
        