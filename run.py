from fastapi import FastAPI
from api.routes import enrich_route


app = FastAPI()
app.include_router(enrich_route.router)