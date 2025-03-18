# ## basics

# from typing import Union, Optional
# from pydantic import BaseModel
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.encoders import jsonable_encoder
# from pymongo import MongoClient
# from mongodb import *
# from bson.json_util import dumps

# ## aditionals

# from fastapi import HTTPException
# from fastapi import FastAPI
# from fastapi_sqlalchemy import DBSessionMiddleware, db

# from sql.schema import User as user_json

# from sql.models import User as user_db
# from sql.models import Base

# from sqlalchemy import create_engine
 

# class Especificaciones(BaseModel):
#     pantalla: Union[str, None] = None
#     cámara: Union[str, None] = None
#     almacenamiento: Union[str, None] = None
#     procesador: Union[str, None] = None
#     ram: Union[str, None] = None
#     resolucion: Union[str, None] = None
#     tamanio: Union[str, None] = None
#     tipo: Union[str, None] = None

# class Product(BaseModel):
#     nombre: str
#     categoria: str
#     precio: float
#     stock: int
#     especificaciones: Optional[Especificaciones] = None

# app = FastAPI()

# database = "postgresql://postgres:1234@localhost:5432/test"

# app.add_middleware(DBSessionMiddleware, db_url=database)
# engine = create_engine(database)
# Base.metadata.create_all(bind=engine)

# # ✅ Add CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change to your frontend URL in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def root():
#     return {"Hello": "test"}

# @app.post("/put_item/")
# def put_item(product: Product):
#     product_dict = jsonable_encoder(product)
#     productos.insert_one(product_dict)
#     return {"Estado": "Realizado"}

# @app.get("/get_items/")
# def get_data():
#     data = list(productos.find({}).limit(5))  # Get first 5 documents
#     lista = []

#     for i in data:
#         lista.append({
#             "id": str(i["_id"]),  # Convert MongoDB ObjectId to string
#             "precio": i["precio"]
#         })

#     return lista

# @app.post("/put_user/")
# def put_user(user: user_json):
#     existing_user = db.session.query(user_db).filter(user_db.username == user.username).first()

#     if existing_user:
#         return {"Estado": "No Realizado"} 

#     # If the username doesn't exist, proceed with insertion
#     user_dict = jsonable_encoder(user)
#     db_user = user_db(**user_dict)
#     db.session.add(db_user)
#     db.session.commit()
    
#     return {"Estado": "Realizado"}



# @app.get("/get_user/")
# def get_user(username: str, password: str):
#     existing_user = db.session.query(user_db).filter(
#         user_db.username == username,
#         user_db.password == password
#     ).first()

#     if existing_user is None:
#         return {"Estado": "No Realizado"}

#     return {
#         "Estado": "Realizado",
#         "username": existing_user.username,
#         "password": existing_user.password
#     }


# class prod_duenio(BaseModel):
#     duenio: Union[str, None] = None
#     producto: Union[str, None] = None
#     precio: Union[float, None] = None


# @app.post("/put_prods_duenio/")
# def get_user(product: prod_duenio):
#    product_dict = jsonable_encoder(product)
#    productos_duenio.insert_one(product_dict)
#    return {"Estado": "Realizado"}

# @app.get("/get_prods_duenio/")
# def get_user(duenio: str):
#     prods = list(productos_duenio.find({"duenio": duenio}))

#     for prod in prods:
#         prod["_id"] = str(prod["_id"])

#     return {"products": prods}


## 🔹 Imports

from typing import Union, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import boto3
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import create_engine
from decimal import Decimal
from datetime import datetime

from sql.schema import User as user_json
from sql.models import User as user_db
from sql.models import Base
from mongodb import *

## 🔹 Pydantic Models

class Especificaciones(BaseModel):
    pantalla: Union[str, None] = None
    cámara: Union[str, None] = None
    almacenamiento: Union[str, None] = None
    procesador: Union[str, None] = None
    ram: Union[str, None] = None
    resolucion: Union[str, None] = None
    tamanio: Union[str, None] = None
    tipo: Union[str, None] = None

class Product(BaseModel):
    clave: str  # Partition Key
    nombre: str
    categoria: str
    precio: float
    stock: int
    especificaciones: Optional[Especificaciones] = None

class ProdDuenio(BaseModel):
    duenio: Union[str, None] = None
    producto: Union[str, None] = None
    precio: Union[float, None] = None

## 🔹 FastAPI Setup

app = FastAPI()

database2 = "postgresql://postgres:Pp75982723@test-usuario.crgygo2mye4q.us-east-2.rds.amazonaws.com:5432/postgres"

app.add_middleware(DBSessionMiddleware, db_url=database2)
engine = create_engine(database2)
Base.metadata.create_all(bind=engine)

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## 🔹 Utility function to fix Decimal issue
def convert_floats(obj):
    """Recursively converts float values in a dictionary to Decimal."""
    if isinstance(obj, list):
        return [convert_floats(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_floats(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))  # Convert float to Decimal safely
    return obj

## 🔹 API Routes

@app.get("/")
def root():
    return {"Hello": "test"}

# ✅ Insert a Product (DynamoDB) with Unique Timestamp
@app.post("/put_item/")
def put_item(product: Product):
    product_dict = jsonable_encoder(product)
    product_dict = convert_floats(product_dict)  # Convert float fields to Decimal

    # Add a unique timestamp (string format)
    product_dict["timestamp"] = datetime.utcnow().isoformat()

    # Insert into DynamoDB
    productos.put_item(Item=product_dict)

    return {"Estado": "Realizado"}

# ✅ Get Products (DynamoDB)
@app.get("/get_items/")
def get_data():
    response = productos.scan(Limit=5)  # Get first 5 items
    items = response.get("Items", [])

    # Convert Decimal to float before returning
    for item in items:
        if "precio" in item:
            item["precio"] = float(item["precio"])
    
    return items

# ✅ Insert User (PostgreSQL)
@app.post("/put_user/")
def put_user(user: user_json):
    existing_user = db.session.query(user_db).filter(user_db.username == user.username).first()

    if existing_user:
        return {"Estado": "No Realizado"}

    user_dict = jsonable_encoder(user)
    db_user = user_db(**user_dict)
    db.session.add(db_user)
    db.session.commit()

    return {"Estado": "Realizado"}

# ✅ Get User (PostgreSQL)
@app.get("/get_user/")
def get_user(username: str, password: str):
    existing_user = db.session.query(user_db).filter(
        user_db.username == username,
        user_db.password == password
    ).first()

    if existing_user is None:
        return {"Estado": "No Realizado"}

    return {
        "Estado": "Realizado",
        "username": existing_user.username,
        "password": existing_user.password
    }

# ✅ Insert Product Owner Data (DynamoDB) with Unique Timestamp
@app.post("/put_prods_duenio/")
def put_prods_duenio(product: ProdDuenio):
    product_dict = jsonable_encoder(product)
    product_dict = convert_floats(product_dict)  # Convert float fields to Decimal

    # Add a unique timestamp
    product_dict["timestamp"] = datetime.utcnow().isoformat()

    # Insert into DynamoDB
    productos_duenio.put_item(Item=product_dict)

    return {"Estado": "Realizado"}

# ✅ Get Products by Owner (DynamoDB)
@app.get("/get_prods_duenio/")
def get_prods_duenio(duenio: str):
    response = productos_duenio.scan(FilterExpression="duenio = :d", ExpressionAttributeValues={":d": duenio})
    items = response.get("Items", [])

    for item in items:
        if "precio" in item:
            item["precio"] = float(item["precio"])  # Convert Decimal to float for response

    return {"products": items}