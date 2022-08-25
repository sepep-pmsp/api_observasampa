from fastapi import FastAPI
from v1 import basic_app, dash_educacao
import uvicorn

app = FastAPI(openapi_url="/")
app.include_router(basic_app, prefix="/basic")
app.include_router(dash_educacao, prefix="/dashboards/educacao")

