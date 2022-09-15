from fastapi import APIRouter, Query

from typing import List, Union

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.dao import front_end as dao
from core.models import front_end as models
from core.schemas import front_end as schemas
from core.models.database import SessionLocal, engine

from core.dao.filtros import siglas_tipo_conteudo


app = APIRouter()

TIPOS_CONTEUDO = siglas_tipo_conteudo()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tipo_conteudo/", response_model=List[schemas.TipoConteudo], tags=['Front-end'])
def read_indicadores(db: Session = Depends(get_db)):

    tipos = dao.list_tipos_conteudo(db)
    return tipos

