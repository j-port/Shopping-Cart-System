from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Preloaded Products
products = [
    {"id": 1, "name": "Table", "price": 120.0, "stock": 10},
    {"id": 2, "name": "Chair", "price": 45.0, "stock": 20},
    {"id": 3, "name": "Laptop", "price": 1000.0, "stock": 5},
    {"id": 4, "name": "Phone", "price": 700.0, "stock": 8},
    {"id": 5, "name": "Headphones", "price": 150.0, "stock": 15},
]

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

@app.get("/products", response_model=List[Product])
async def get_products():
    return products

@app.post("/products")
async def add_product(product: Product):
    if any(p["id"] == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product ID already exists.")
    products.append(product.dict())
    return {"message": "Product added!", "product": product}

@app.post("/orders")
async def create_order(order: Order):
    product = next((p for p in products if p["id"] == order.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if product["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock.")
    
    product["stock"] -= order.quantity
    orders.append(order.dict())
    return {"message": "Order placed!", "order": order}

@app.get("/orders", response_model=List[Order])
async def get_orders():
    return orders
