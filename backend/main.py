from fastapi import FastAPI

app = FastAPI(title="fundus-read api")

@app.get("/health")
def health():
    return {"status": "ok"}

from pydantic import BaseModel
from passlib.context import CryptContext

from fastapi import HTTPException
import os, psycopg2

@app.post("/auth/login")
def login(data: LoginRequest):
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute(
            "SELECT password_hash, is_active FROM usuarios WHERE cc = %s",
            (data.cc,)
        )
        row = cur.fetchone()
    except Exception as e:
        # Esto hará que Swagger muestre el error exacto
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try: cur.close()
        except: pass
        try: conn.close()
        except: pass

    if not row:
        return {"success": False, "message": "Usuario no encontrado"}

    password_hash, is_active = row
    if not is_active:
        return {"success": False, "message": "Usuario inactivo"}

    if not pwd_context.verify(data.password, password_hash):
        return {"success": False, "message": "Credenciales inválidas"}

    return {"success": True}