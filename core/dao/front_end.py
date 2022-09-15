from sqlalchemy.orm import Session

from ..models import front_end as models
from ..schemas import front_end as schemas

def list_tipos_conteudo(db: Session):

    model = models.TipoConteudo
    query = db.query(model)
    #nao tem tipo situacao
    #query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def get_tipo_conteudo(db: Session, cd_tipo_conteudo: int):

    model = models.TipoConteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_conteudo==cd_tipo_conteudo)

    return query.firts()


def list_conteudos(db: Session):

    model = basicmodels.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)

    return query.all()

def list_conteudos_por_tipo(db: Session, cd_tipo_conteudo: int):

    model = basicmodels.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_conteudo==cd_tipo_conteudo)

    return query.all()