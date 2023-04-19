from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query, status

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


# inventory = {
#     1: {
#         "name": "Milk",
#         "price": 3.99,
#         "brand": "Regular"
#     }
# }

inventory = {}


@app.get("/")
def home():
    return {"Data": "Hello!"}


@app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(description="The ID of the Item you'd like to view.", gt=0, lt=2)):
def get_item(item_id: int = Path(description="The ID of the Item you'd like to view.", gt=0)):  # noqa: B008
    return inventory[item_id]


# @app.get("/get-by-name/{item_id}")
# def get_item(*, item_id: int, name: Optional[str] = None, test: int):
#     for item_id in inventory:
#         if inventory[item_id]["name"] == name:
#             return inventory[item_id]
#     return {"Data": "Not found"}


@app.get("/get-by-name")
def get_item_by_name(name: str = Query(None, title="Name", description="Name of item")):  # noqa: B008
    for item_id in inventory:
        # if inventory[item_id]["name"] == name:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found.")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        # return {"Error": "Item ID is already exist."}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists.")

    # inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist.")

    if item.name is not None:
        inventory[item_id].name = item.name
    if item.price is not None:
        inventory[item_id].price = item.price
    if item.brand is not None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the Item you'd like to delete.", gt=0)):  # noqa: B008
    if item_id not in inventory:
        # return {"Error": "Item ID does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist.")

    del inventory[item_id]
    return {"Success": "Item deleted!"}
