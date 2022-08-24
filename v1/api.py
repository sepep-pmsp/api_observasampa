from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from core.dao import basic as basicdao
from core.models import basic as basicmodels
from core.schemas import basic as basicschemas
from core.models.database import SessionLocal, engine

basicmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/indicadores/", response_model=List[basicschemas.IndicadorBase])
def read_indicadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    indicadores = basicdao.list_indicadores(db, skip=skip, limit=limit)
    return indicadores

@app.get("/indicadores/{cd_indicador}", response_model=basicschemas.IndicadorReport)
def read_indicador(cd_indicador: int, db: Session = Depends(get_db)):

    indicador = basicdao.get_indicador(db, cd_indicador=cd_indicador)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador Não Encontrado")
    return indicador

@app.get("/resultados/{cd_indicador}", response_model=List[basicschemas.ResultadoIndicador])
def read_indicador(cd_indicador: int, db: Session = Depends(get_db)):

    indicador = basicdao.get_indicador(db, cd_indicador=cd_indicador)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador Não Encontrado")

    resultados = basicdao.resultados_indicador(db, cd_indicador=indicador.cd_indicador)
    
    return resultados