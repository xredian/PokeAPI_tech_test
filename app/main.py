from fastapi import FastAPI
from app.api.api import router


app = FastAPI(title="Poke-berries statistics API")
app.include_router(router)

