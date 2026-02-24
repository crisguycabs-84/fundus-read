from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import os
import psycopg2

app = FastAPI(title="fundus-read api")

# bcrypt context (para verificar contra password_hash)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    cc: str
    password: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/login")
def login(data: LoginRequest):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute(
            "SELECT password_hash, is_active FROM usuarios WHERE cc = %s",
            (data.cc,)
        )
        row = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    if not row:
        return {"success": False, "message": "Usuario no encontrado"}

    password_hash, is_active = row

    if not is_active:
        return {"success": False, "message": "Usuario inactivo"}

    if not pwd_context.verify(data.password, password_hash):
        return {"success": False, "message": "Credenciales inválidas"}

    return {"success": True}