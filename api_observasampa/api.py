from fastapi import FastAPI
from v1 import basic_app, front_end
import uvicorn
import asyncio
import time
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_504_GATEWAY_TIMEOUT

from config import REQUEST_TIMEOUT_ERROR

#pode colocar markdown
description = """
## API para o OBSERVA**SAMPA**.

Desenvolvimento interno - time de **tecnologia de SEPEP** 🚀
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


#middleware to handle timeouts
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        return await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_ERROR)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse({'detail': 'Request processing time excedeed limit',
                             'processing_time': process_time},
                            status_code=HTTP_504_GATEWAY_TIMEOUT)

app.include_router(basic_app, prefix="/v1/basic")
app.include_router(front_end, prefix="/v1/front_end")


