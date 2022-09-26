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

@app.get("/conteudos/", response_model=List[schemas.ConteudoBase],  tags=['Front-end'])
def read_resultados_indicador(sg_tipo_conteudo : str = Query(enum=TIPOS_CONTEUDO),
                        db: Session = Depends(get_db)):

    tipo_conteudo = dao.get_tipo_conteudo(db, sg_tipo_conteudo=sg_tipo_conteudo)
    if tipo_conteudo is None:
        raise HTTPException(status_code=404, detail=f"Tipo conteudo {sg_tipo_conteudo} não Encontrado")

    resultados = dao.list_conteudos_por_tipo(db, cd_tipo_conteudo=tipo_conteudo.cd_tipo_conteudo)
    
    return resultados

