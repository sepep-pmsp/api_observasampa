from fastapi import APIRouter

from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.responses import StreamingResponse

from core.dao import dash_educacao as dao
from core.schemas import dash_educacao as schemas
from core.models.database import SessionLocal, engine


app = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/indicadores_sexo_educacao_municipio/", tags=['Dashboard Educação'], 
        response_class=StreamingResponse)
def indicadores_sexo_educacao_municipio(db: Session = Depends(get_db)):

    io = dao.indicadores_sexo_educacao_municipio(db)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="text/csv"
       )
    
    response.headers["Content-Disposition"] = "attachment; filename=indicadores_sexo_educacao_municipio.csv"

    return response

@app.get("/distritos/", tags=['Dashboard Educação'], 
        response_class=StreamingResponse)
def distritos(db: Session = Depends(get_db)):

    io = dao.distritos(db)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="text/csv"
       )
    
    response.headers["Content-Disposition"] = "attachment; filename=distritos.csv"

    return response

@app.get("/indicadores_educacao_distritos/", tags=['Dashboard Educação'], 
        response_class=StreamingResponse)
def indicadores_educacao_distritos(db: Session = Depends(get_db)):

    io = dao.indicadores_educacao_distritos(db)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="text/csv"
       )
    
    response.headers["Content-Disposition"] = "attachment; filename=indicadores_educacao_distritos.csv"

    return response

@app.get("/indicadores_educacao_municipio/", tags=['Dashboard Educação'], 
        response_class=StreamingResponse)
def indicadores_educacao_municipio(db: Session = Depends(get_db)):

    io = dao.indicadores_educacao_municipio(db)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="text/csv"
       )
    
    response.headers["Content-Disposition"] = "attachment; filename=indicadores_educacao_municipio.csv"

    return response

@app.get("/periodos/", tags=['Dashboard Educação'], 
        response_class=StreamingResponse)
def periodos(db: Session = Depends(get_db)):

    io = dao.periodos(db)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="text/csv"
       )
    
    response.headers["Content-Disposition"] = "attachment; filename=periodos.csv"

    return response

@app.get("/indicadores_raca_cor_educacao_municipio/", tags=['Dashboard Educação'], 
        response_class=StreamingResponse)
def indicadores_raca_cor_educacao_municipio(db: Session = Depends(get_db)):

    io = dao.indicadores_raca_cor_educacao_municipio(db)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="text/csv"
       )
    
    response.headers["Content-Disposition"] = "attachment; filename=indicadores_raca_cor_educacao_municipio.csv"

    return response
