from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

products = []
orders = []

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class Order(BaseModel):
    product_id: int
    quantity: int

@app.get("/")
async def root():
    return {"message": "Welcome to the Shopping Cart System!"}

@app.get("/products")
async def get_products():
    return products

@app.post("/products")
async def add_product(product: Product):
    products.append(product)
    return {"message": "Product added!", "product": product}

@app.post("/orders")
async def create_order(order: Order):
    product = next((p for p in products if p.id == order.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock.")
    product.stock -= order.quantity
    orders.append(order)
    return {"message": "Order placed!", "order": order}
