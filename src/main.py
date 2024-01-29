from datetime import datetime
import logging

from fastapi import FastAPI

from src.routers.urls_router import urls_router

app = FastAPI()
app.include_router(urls_router)


logging.basicConfig(
    filename="shortly_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")


@app.middleware("http")
async def log_request(request, call_next):
    start_time = datetime.utcnow()

    if request.client:
        logging.info(
            f"{start_time} - {request.method} - {request.url.path} - "
            f"Client IP: {request.client.host}"
        )

    response = await call_next(request)

    if request.client:
        logging.info(
            f"{start_time} - {request.method} - {request.url.path} - "
            f"Client IP: {request.client.host} - Response Status Code: {response.status_code}"
        )

    return response
