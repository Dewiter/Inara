from fastapi import FastAPI

from routers import api_router

app = FastAPI(title="Inara")
app.include_router(api_router)
