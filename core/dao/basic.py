from sqlalchemy.orm import Session

from ..models import basic as basicmodels
from ..schemas import basic as basicschemas


def list_indicadores(db: Session, skip: int = 0, limit: int = 100):

    model = basicmodels.Indicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.offset(skip).limit(limit)


    return query.all()

def get_indicador(db: Session, cd_indicador: int):

    model = basicmodels.Indicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_indicador==cd_indicador)

    return query.first()

def resultados_indicador(db: Session, cd_indicador: int):

    model = basicmodels.ResultadoIndicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_indicador==cd_indicador)

    return query.all()

def list_regioes(db: Session, skip: int = 0, limit: int = 100):

    model = basicmodels.Regiao
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.offset(skip).limit(limit)

    return query.all()

def list_niveis_regioes(db: Session, skip: int = 0, limit: int = 100):

    model = basicmodels.NivelRegiao
    query = db.query(model)
    #Nivel regiao nao tem tipo de situacao
    #query = query.filter(model.cd_tipo_situacao==1)
    query = query.offset(skip).limit(limit)

    return query.all()

def get_nivel_regiao(db: Session, cd_nivel_regiao: int):

    model = basicmodels.NivelRegiao
    query = db.query(model) 
    query = query.filter(model.cd_nivel_regiao == cd_nivel_regiao)

    return query.first()

def list_regioes_nivel(db: Session, cd_nivel_regiao: int):

    model = basicmodels.Regiao
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_nivel_regiao==cd_nivel_regiao)

    return query.all()

def list_periodos(db: Session, skip: int = 0, limit: int = 100):

    model = basicmodels.Periodo
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.offset(skip).limit(limit)

    return query.all()

def periodos_indicador(db: Session, cd_indicador: int):

    resultados = resultados_indicador(db = db, cd_indicador=cd_indicador)

    periodos = list(set([r.periodo for r in resultados]))

    return periodos