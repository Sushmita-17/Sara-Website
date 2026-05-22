import mysql.connector
from fastapi import HTTPException
from ..config import DB_CONFIG

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")
