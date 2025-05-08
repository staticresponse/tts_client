from fastapi import FastAPI
from routers import processor

app = FastAPI()

app.include_router(processor.router)

@app.get("/")
async def root():
    return {"status": "operational"}
