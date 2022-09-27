from sqlalchemy.orm import Session

from ..models import front_end as models
from ..models import basic as basicmodels
from ..schemas import front_end as schemas

def list_tipos_conteudo(db: Session):

    model = models.TipoConteudo
    query = db.query(model)
    #nao tem tipo situacao
    #query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def get_tipo_conteudo(db: Session, sg_tipo_conteudo: str):

    model = models.TipoConteudo
    query = db.query(model)
    query = query.filter(model.sg_tipo_conteudo==sg_tipo_conteudo)

    return query.first()


def list_conteudos(db: Session):

    model = models.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def list_conteudos_por_tipo(db: Session, cd_tipo_conteudo: int, skip: int = None, 
                            limit : int = None):

    model = models.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_conteudo==cd_tipo_conteudo)
    query = query.filter(model.cd_tipo_situacao==1)

    if skip or limit:
        skip = skip or 0
        limit = limit or 100
        query = query.offset(skip).limit(limit)

    return query.all()

def get_conteudo(db: Session, cd_conteudo: int):

    model = models.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_conteudo==cd_conteudo)

    return query.first()

def get_arq_tema(db: Session, cd_tema: int):

    model = basicmodels.Tema
    query = db.query(model)
    query = query.filter(model.cd_tema==cd_tema)

    return query.first()