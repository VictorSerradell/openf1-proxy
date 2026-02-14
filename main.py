# archivo: main.py (ACTUALIZADO)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import openf1, health, metrics, ws
from utils.cache import cache

app = FastAPI(
    title="OpenF1 Enterprise Proxy API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(openf1.router)
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(ws.router)


@app.on_event("startup")
async def startup():
    await cache.init()


@app.on_event("shutdown")
async def shutdown():
    pass
