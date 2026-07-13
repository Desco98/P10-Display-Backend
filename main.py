import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router as api_router
from mqtt import mqtt_manager

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start MQTT client background task
    await mqtt_manager.start()
    yield
    # Shutdown: Stop MQTT client cleanly
    await mqtt_manager.stop()

app = FastAPI(
    title="P10 Matrix Backend",
    description="FastAPI backend for P10 Controller with MQTT integration",
    lifespan=lifespan
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "P10 Matrix Backend API is running"}
