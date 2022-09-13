from sqlalchemy.orm import Session

from ..models import basic as basicmodels
from ..schemas import basic as basicschemas

from .filtros import resultados_por_nivel_cd

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

def list_temas(db: Session):

    model = basicmodels.Tema
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def resultados_indicador(db: Session, cd_indicador: int):

    model = basicmodels.ResultadoIndicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_indicador==cd_indicador)

    return query.all()

def resultados_indicador_nivel_regiao(db: Session, cd_indicador: int, cd_nivel_regiao: int):

    model = basicmodels.ResultadoIndicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_indicador==cd_indicador)
    r = query.all()

    return resultados_por_nivel_cd(r, cd_nivel_regiao)

def list_regioes(db: Session, skip: int = 0, limit: int = 100):

    model = basicmodels.Regiao
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.offset(skip).limit(limit)

    return query.all()

def list_niveis_regioes(db: Session):

    model = basicmodels.NivelRegiao
    query = db.query(model)
    #Nivel regiao nao tem tipo de situacao
    #query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def get_nivel_regiao(db: Session, cd_nivel_regiao: int):

    model = basicmodels.NivelRegiao
    query = db.query(model) 
    query = query.filter(model.cd_nivel_regiao == cd_nivel_regiao)

    return query.first()

def get_nivel_regiao_sg(db: Session, sg_nivel_regiao: str):

    model = basicmodels.NivelRegiao
    query = db.query(model) 
    query = query.filter(model.sg_nivel_regiao == sg_nivel_regiao)

    return query.first()

def list_regioes_nivel(db: Session, cd_nivel_regiao: int):

    model = basicmodels.Regiao
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_nivel_regiao==cd_nivel_regiao)

    return query.all()

def list_periodos(db: Session):

    model = basicmodels.Periodo
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def periodos_indicador(db: Session, cd_indicador: int):

    resultados = resultados_indicador(db = db, cd_indicador=cd_indicador)

    periodos = list(set([r.periodo for r in resultados]))

    return periodos

def list_variaveis(db: Session, skip: int = 0, limit: int = 100):

    model = basicmodels.Variavel
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.offset(skip).limit(limit)


    return query.all()

def get_variavel(db: Session, nm_resumido_variavel: str):

    model = basicmodels.Variavel
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.nm_resumido_variavel==nm_resumido_variavel)

    return query.first()

def resultados_variavel(db: Session, nm_resumido_variavel: str):

    variavel = get_variavel(db, nm_resumido_variavel=nm_resumido_variavel)
    model = basicmodels.ResultadoVariavel
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_variavel==variavel.cd_variavel)

    return query.all()

def resultados_variavel_nivel_regiao(db: Session, nm_resumido_variavel: str, cd_nivel_regiao: int):

    variavel = get_variavel(db, nm_resumido_variavel=nm_resumido_variavel)
    model = basicmodels.ResultadoVariavel
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_variavel==variavel.cd_variavel)
    r = query.all()

    return resultados_por_nivel_cd(r, cd_nivel_regiao)