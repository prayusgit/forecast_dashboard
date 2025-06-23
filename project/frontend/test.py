from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Depends, Path
from pydantic import BaseModel, Field

app = FastAPI(
    title="eSewa ML Forecast API",
    description="Predicts future transaction volume & growth",
    version="1.0.0",
    contact={
        "name": "Prayush Bhattarai",
        "email": "prayush@esewa.com.np"
    },
)

class Item(BaseModel):
    name: str = Field(..., alias='username')
    price: float
    in_stock: bool = True

@app.post("/items/")
def create_item(item: Item):
    return {"message": f"{item.name} added", "price": item.price}

from typing import Optional

@app.get("/frontend")
def show_dashboard(view: str = 'summary'):
    return {"view_mode": view}


@app.post("/upload/{name}")
async def upload_file(name: str,file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }



def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret123":
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get("/secure/", dependencies=[Depends(verify_api_key)])
def secure_endpoint():
    return {"message": "Welcome!"}
from fastapi import Query

def pagination(skip: int = Query(0), limit: int = Query(10)):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def list_items(p=Depends(pagination)):
    return {"pagination": p}

@app.get("/orders/{name}", dependencies=[Depends(pagination)])
def list_orders(name:str = Path(...),p=Depends(pagination)):
    return {"pagination": p}


def get_api_key(x_api_key: str = Depends(lambda: "secret123")):
    if x_api_key != "secret123":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.get("/products/")
def get_products(api_key: str = Depends(get_api_key)):
    return {"msg": "Products list"}

@app.get("/users/")
def get_users(api_key: str = Depends(get_api_key)):
    return {"msg": "Users list"}
