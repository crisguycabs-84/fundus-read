from fastapi import FastAPI

app = FastAPI(title="fundus-read api")

@app.get("/health")
def health():
    return {"status": "ok"}

from pydantic import BaseModel
from passlib.context import CryptContext
import psycopg2
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    cc: str
    password: str

@app.post("/auth/login")
def login(data: LoginRequest):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()

    cur.execute(
        'SELECT password_hash, is_active FROM "Usuarios" WHERE cc = %s',
        (data.cc,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return {"success": False, "message": "Usuario no encontrado"}

    password_hash, is_active = row

    if not is_active:
        return {"success": False, "message": "Usuario inactivo"}

    if not pwd_context.verify(data.password, password_hash):
        return {"success": False, "message": "Credenciales inválidas"}

    return {"success": True}