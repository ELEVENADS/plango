import uvicorn
from fastapi import FastAPI

from app.api.v1.generate import router as generate_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="PlanGoDaily Agent", version="1.0.0")

app.include_router(generate_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"service": "PlanGoDaily Agent", "status": "running"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=18000,
        reload=True,
    )
