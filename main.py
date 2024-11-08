from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from get_embeddings import get_embeddings

app = FastAPI()

def get_db():
    conn = psycopg2.connect("dbname=postgres user=postgres password=admin123 host=localhost")
    try:
        yield conn
    finally:
        conn.close()

class Product(BaseModel):
    id: int
    name: str
    description: str

class Embedding(BaseModel):
    id: int
    embedding: List[float]

@app.get("/getProducts/", response_model=List[Product])
def get_products(db: psycopg2.extensions.connection = Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM products;")
    products = cur.fetchall()
    return products


@app.get("/getProductsByQuery/{user_query}", response_model=List[Product])
def get_products_by_query(user_query: str, db: psycopg2.extensions.connection = Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)
    embedded_query = get_embeddings(user_query)
    query = """
        SELECT id, name, description
        FROM products
        JOIN embeddings
        USING (id)
        WHERE 1 - (embedding <=> %s::vector) > 0.5 
        LIMIT 5;
    """
    cur.execute(query, (embedded_query,))
    products = cur.fetchall()
    return products