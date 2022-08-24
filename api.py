from fastapi import FastAPI
from v1 import basic_app
import uvicorn

app = FastAPI(openapi_url="/")
app.include_router(basic_app, prefix="/basic")
