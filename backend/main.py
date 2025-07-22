from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import secrets

app = FastAPI()
security = HTTPBasic()

ADMIN_PASSWORD = "admin123"  # Задай свой пароль

# Данные (в памяти)
CATEGORIES: Dict[str, Dict[str, Any]] = {}
ITEMS: Dict[str, Dict[str, Any]] = {}

# CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return True

# --- Категории ---
@app.get("/categories")
def get_categories(auth: bool = Depends(check_auth)):
    return list(CATEGORIES.values())

@app.post("/categories")
def add_category(category: Dict[str, Any], auth: bool = Depends(check_auth)):
    key = category.get("category_name")
    if not key or key in CATEGORIES:
        raise HTTPException(status_code=400, detail="Category already exists or no name")
    CATEGORIES[key] = category
    return category

@app.put("/categories/{category_name}")
def update_category(category_name: str, category: Dict[str, Any], auth: bool = Depends(check_auth)):
    if category_name not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    CATEGORIES[category_name].update(category)
    return CATEGORIES[category_name]

@app.delete("/categories/{category_name}")
def delete_category(category_name: str, auth: bool = Depends(check_auth)):
    if category_name not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    del CATEGORIES[category_name]
    return {"ok": True}

# --- Товары ---
@app.get("/items")
def get_items(auth: bool = Depends(check_auth)):
    return list(ITEMS.values())

@app.post("/items")
def add_item(item: Dict[str, Any], auth: bool = Depends(check_auth)):
    key = item.get("item_id")
    if not key or str(key) in ITEMS:
        raise HTTPException(status_code=400, detail="Item already exists or no id")
    ITEMS[str(key)] = item
    return item

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Dict[str, Any], auth: bool = Depends(check_auth)):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    ITEMS[item_id].update(item)
    return ITEMS[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: str, auth: bool = Depends(check_auth)):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    del ITEMS[item_id]
    return {"ok": True}

# --- Для теста: заполнить начальными данными ---
@app.post("/init_data")
def init_data(auth: bool = Depends(check_auth)):
    global CATEGORIES, ITEMS
    CATEGORIES = {
        # ... сюда можно вставить твои категории ...
    }
    ITEMS = {
        # ... сюда можно вставить твои товары ...
    }
    return {"ok": True} 