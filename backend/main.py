from fastapi import FastAPI

app = FastAPI(title="fundus-read api")

@app.get("/health")
def health():
    return {"status": "ok"}
