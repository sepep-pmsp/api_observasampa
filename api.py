from fastapi import FastAPI
from v1 import basic_app, dash_educacao
import uvicorn

#pode colocar markdown
description = """
## API para o OBSERVA**SAMPA**.

Desenvolvimento interno - time de **tecnologia de SEPEP** 🚀

Em parceria com PRODAM.
"""

app = FastAPI(openapi_url="/",
    title="OBSERVASAMPA",
    description=description,
    version="0.0.1",
    #terms_of_service="http://example.com/terms/",
    contact={
        "name": "SEPEP",
        "url": "https://www.prefeitura.sp.gov.br/cidade/secretarias/governo/planejamento/",
        "email": "hpougy@prefeitura.sp.gov.br",
    },
    license_info={
        "name": "AGPL V3.0",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
    )
app.include_router(basic_app, prefix="/basic")
app.include_router(dash_educacao, prefix="/dashboards/educacao")

