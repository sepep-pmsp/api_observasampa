from fastapi import APIRouter, Query

from typing import List, Union

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.dao import basic as basicdao
from core.dao import filtros
from core.models import basic as basicmodels
from core.schemas import basic as basicschemas
from core.models.database import SessionLocal, engine

basicmodels.Base.metadata.create_all(bind=engine)

app = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

NIVEIS_REGIOES = filtros.nomes_niveis()

@app.get("/temas/", response_model=List[basicschemas.TemaReport], tags=['Indicadores'])
def read_indicadores(db: Session = Depends(get_db)):

    temas = basicdao.list_temas(db)
    return temas


@app.get("/indicadores/", response_model=List[basicschemas.IndicadorBase], tags=['Indicadores'])
def read_indicadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    indicadores = basicdao.list_indicadores(db, skip=skip, limit=limit)
    return indicadores

@app.get("/indicadores/{cd_indicador}", response_model=basicschemas.IndicadorReport,  tags=['Indicadores'])
def read_indicador_detail(cd_indicador: int, db: Session = Depends(get_db)):

    indicador = basicdao.get_indicador(db, cd_indicador=cd_indicador)
    if indicador is None:
        raise HTTPException(status_code=404, detail=f"Indicador {cd_indicador} Não Encontrado")
    return indicador

@app.get("/indicadores/{cd_indicador}/resultados", response_model=List[basicschemas.ResultadoIndicador],  tags=['Indicadores'])
def read_resultados_indicador(cd_indicador: int, nivel_regional : str = Query(enum=NIVEIS_REGIOES),
                        db: Session = Depends(get_db)):

    indicador = basicdao.get_indicador(db, cd_indicador=cd_indicador)
    if indicador is None:
        raise HTTPException(status_code=404, detail=f"Indicador {cd_indicador} Não Encontrado")

    if nivel_regional:
        nivel = basicdao.get_nivel_regiao_sg(db, sg_nivel_regiao=nivel_regional)
        resultados = basicdao.resultados_indicador_nivel_regiao(db, cd_indicador=indicador.cd_indicador,
                                                                cd_nivel_regiao=nivel.cd_nivel_regiao)

        return resultados

    resultados = basicdao.resultados_indicador(db, cd_indicador=indicador.cd_indicador)
    
    return resultados


@app.get("/regioes/niveis/", response_model=List[basicschemas.NivelRegiao], tags=['Regiões'])
def list_niveis(db: Session = Depends(get_db)):

    niveis = basicdao.list_niveis_regioes(db)
    return niveis

@app.get("/regioes/", response_model=List[basicschemas.Regiao], tags=['Regiões'])
def list_regioes(cd_nivel_regiao: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    if cd_nivel_regiao:
        nivel = basicdao.get_nivel_regiao(db, cd_nivel_regiao = cd_nivel_regiao)
        if nivel is None:
            raise HTTPException(status_code=404, detail=f'Nivel {cd_nivel_regiao} não existente')
        regioes = basicdao.list_regioes_nivel(db, cd_nivel_regiao = nivel.cd_nivel_regiao)
        return regioes

    regioes = basicdao.list_regioes(db, skip=skip, limit=limit)
    return regioes


 

@app.get("/periodos/", response_model=List[basicschemas.Periodo], tags=['Períodos'])
def list_periodos(lst_indicadores: Union[List[str], None] = Query(default=None),
                db: Session = Depends(get_db)):

    if lst_indicadores is not None:
        periodos = set()
        for cd_indicador in lst_indicadores:
            indicador = basicdao.get_indicador(db=db, cd_indicador = cd_indicador)
            if indicador is None:
                raise HTTPException(status_code=404, detail=f'Indicador {cd_indicador} não existente')
            periodos_ind = basicdao.periodos_indicador(db, cd_indicador=indicador.cd_indicador)
            periodos.update(periodos_ind)
        return periodos

    periodos = basicdao.list_periodos(db)
    return periodos

@app.get("/periodos/{cd_indicador}", response_model=List[basicschemas.Periodo], tags=['Períodos', 'Indicadores'])
def list_periodos_indicador(cd_indicador: int, db: Session = Depends(get_db)):

    indicador = basicdao.get_indicador(db=db, cd_indicador = cd_indicador)

    if indicador is None:
        raise HTTPException(status_code=404, detail=f'Indicador {cd_indicador} não existente')

    periodos = basicdao.periodos_indicador(db, cd_indicador=indicador.cd_indicador)
    return periodos

@app.get("/variaveis/", response_model=List[basicschemas.VariavelBase], tags=['Variaveis'])
def read_variaveis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    variaveis = basicdao.list_variaveis(db, skip=skip, limit=limit)
    return variaveis

@app.get("/variaveis/{nm_resumido_variavel}", response_model=basicschemas.VariavelReport,  tags=['Variaveis'])
def read_variavel_detail(nm_resumido_variavel: str, db: Session = Depends(get_db)):

    variavel = basicdao.get_variavel(db, nm_resumido_variavel=nm_resumido_variavel)
    if variavel is None:
        raise HTTPException(status_code=404, detail=f"Variavel {nm_resumido_variavel} Não Encontrada")
    return variavel

@app.get("/variaveis/{nm_resumido_variavel}/resultados", response_model=List[basicschemas.ResultadoVariavel],  tags=['Variaveis'])
def read_resultados_indicador(nm_resumido_variavel: str,  nivel_regional : str = Query(enum=NIVEIS_REGIOES),
                             db: Session = Depends(get_db)):

    variavel = basicdao.get_variavel(db, nm_resumido_variavel=nm_resumido_variavel)
    if variavel is None:
        raise HTTPException(status_code=404, detail=f"Variavel {nm_resumido_variavel} Não Encontrada")

    
    if nivel_regional:
        nivel = basicdao.get_nivel_regiao_sg(db, sg_nivel_regiao=nivel_regional)
        resultados = basicdao.resultados_variavel_nivel_regiao(db, nm_resumido_variavel=variavel.nm_resumido_variavel,
                                                                cd_nivel_regiao=nivel.cd_nivel_regiao)

        return resultados

    resultados = basicdao.resultados_variavel(db, nm_resumido_variavel=variavel.nm_resumido_variavel)
    
    return resultados
