from fastapi import FastAPI
from routers import products, users, basic_auth, jwt_auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)


app.include_router(basic_auth.router)
app.include_router(jwt_auth.router)
app.mount("/static", StaticFiles(directory="static"), name="static") # forma de llamar recursos estaticos como una imagen


# inicia el server: uvicorn main:app --reload
# Detener el server CTRL + C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

@app.get("/")
async def root():
    return "estamos en el main"

