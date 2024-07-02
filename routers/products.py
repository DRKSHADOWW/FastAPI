from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags= ["products"], # separa el archivo products en docs
                   responses={404: {"mesagge": "No encontrado"}})

product_list = ["producto1", "producto2", "producto3", "producto4", "producto1" ]
    

@router.get("/")
async def products():
    return product_list
    
@router.get("/{id}")
async def products(id: int):
    return product_list[id]

