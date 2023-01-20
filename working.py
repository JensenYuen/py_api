from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}

@app.get("/")
async def API_health():
    return {"Data": {
        "statusCode": 200,
        "health": "ok"
    }}

@app.get("/get-item/{item_id}")
async def get_item(item_id: int = Path(None, description="The ID of the item you want")):
    return inventory[item_id]

@app.get("/get-by-name")
async def get_item(name: str = Query(None, title="Name", description="Name of item.")):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]

    raise HTTPException(status_code=404, detail="Item name not found")

@app.post("/create-item")
async def create_item(item: Item):
    item_count = len(inventory)
    inventory[item_count + 1] = item

    return item

@app.put("/update-item/{item_id}")
async def update_item(item: UpdateItem, item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exists.")

    if item.name:
        inventory[item_id].name = item.name
    if item.price:
        inventory[item_id].price = item.price
    if item.brand:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
async def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exists.")

    del inventory[item_id]
    return {"Success": "Item deleted"}
