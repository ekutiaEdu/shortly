from fastapi import FastAPI

from src.routers.urls_router import urls_router

app = FastAPI()
app.include_router(urls_router)
