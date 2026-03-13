from fastapi import FastAPI, Query, status, Response, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="FastAPI Assignment 3 - Day 4")

# Initial Products List
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

# --- Models ---

class NewProduct(BaseModel):
    name: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    in_stock: bool = True

class ProductUpdate(BaseModel):
    price: Optional[int] = None
    in_stock: Optional[bool] = None

# --- Helper Functions ---

def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

# --- Endpoints ---

@app.get("/")
def home():
    return {"message": "FastAPI Day 4 CRUD Assignment API"}

# Q1: Get All Products
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

# Q5: Inventory Audit (Placed ABOVE /{product_id})
@app.get("/products/audit")
def product_audit():
    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]
    
    # total_stock_value = sum of (price * 10) for in-stock items only
    stock_value = sum(p["price"] * 10 for p in in_stock_list)
    
    # most_expensive: name + price of the priciest product (even if out of stock)
    if not products:
        return {"message": "No products available"}
        
    priciest = max(products, key=lambda p: p["price"])
    
    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {"name": priciest["name"], "price": priciest["price"]},
    }

# Bonus: Bulk Discount (Placed ABOVE /{product_id})
@app.put("/products/discount")
def bulk_discount(
    category: str = Query(..., description="Category to apply discount to"),
    discount_percent: int = Query(..., ge=1, le=99, description="Percentage (1-99) of discount")
):
    updated = []
    for p in products:
        if p["category"].lower() == category.lower():
            # new_price = int(price * (1 - discount_percent / 100))
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)
            
    if not updated:
        return {"message": f"No products found in category: {category}"}
        
    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated,
    }

# GET Product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    return product

# Q1: Add Products (POST)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: NewProduct, response: Response):
    # Duplicate check (Case-insensitive)
    if any(p["name"].lower() == product.name.lower() for p in products):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Product with this name already exists"}
    
    # ID Generation
    next_id = max(p["id"] for p in products) + 1 if products else 1
    
    new_product = product.model_dump()
    new_product["id"] = next_id
    products.append(new_product)
    
    return {"message": "Product added", "product": new_product}

# Q2: Update Product (PUT)
@app.put("/products/{product_id}")
def update_product(
    product_id: int, 
    response: Response, 
    price: Optional[int] = Query(None), 
    in_stock: Optional[bool] = Query(None)
):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    
    # Update fields if provided
    if price is not None:
        product["price"] = price
    if in_stock is not None:
        product["in_stock"] = in_stock
        
    return {"message": "Product updated", "product": product}

# Q3: Delete Product (DELETE)
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    
    products.remove(product)
    return {"message": f"Product '{product['name']}' deleted"}
