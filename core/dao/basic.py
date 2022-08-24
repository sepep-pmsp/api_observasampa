from sqlalchemy.orm import Session

from ..models import basic as basicmodels
from ..schemas import basic as basicschemas


def list_indicadores(db: Session, skip: int = 0, limit: int = 100):

    query = db.query(basicmodels.Indicador).offset(skip).limit(limit)


    return query.all()

def get_indicador(db: Session, cd_indicador: int):

    query = db.query(basicmodels.Indicador)
    query = query.filter(basicmodels.Indicador.cd_indicador==cd_indicador)

    return query.first()

def resultados_indicador(db: Session, cd_indicador: int):

    query = db.query(basicmodels.ResultadoIndicador)
    query = query.filter(basicmodels.ResultadoIndicador.cd_indicador==cd_indicador)

    return query.all()

def list_regioes(db: Session, skip: int = 0, limit: int = 100):

    query = db.query(basicmodels.Regiao).offset(skip).limit(limit)

    return query.all()

def list_periodos(db: Session, skip: int = 0, limit: int = 100):

    query = db.query(basicmodels.Periodo).offset(skip).limit(limit)

    return query.all()