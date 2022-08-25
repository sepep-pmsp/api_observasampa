from fastapi import APIRouter

from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

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


@app.get("/indicadores_sexo_educacao_municipio/", response_model=schemas.DadosCsv, tags=['Dashboard Educação'])
def indicadores_sexo_educacao_municipio(db: Session = Depends(get_db)):

    csv_data = dao.indicadores_sexo_educacao_municipio(db)
    return csv_data
