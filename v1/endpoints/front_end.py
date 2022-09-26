from fastapi import APIRouter, Query

from typing import List, Union

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.responses import StreamingResponse

from core.dao import front_end as dao
from core.models import front_end as models
from core.schemas import front_end as schemas
from core.models.database import SessionLocal, engine

from core.dao.filtros import siglas_tipo_conteudo, arquivo_conteudo, image_conteudo


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
def read_tipo_conteudos(db: Session = Depends(get_db)):

    tipos = dao.list_tipos_conteudo(db)
    return tipos

@app.get("/conteudos/", response_model=List[schemas.ConteudoBase],  tags=['Front-end'])
def read_conteudos(sg_tipo_conteudo : str = Query(enum=TIPOS_CONTEUDO),
                        db: Session = Depends(get_db)):

    tipo_conteudo = dao.get_tipo_conteudo(db, sg_tipo_conteudo=sg_tipo_conteudo)
    if tipo_conteudo is None:
        raise HTTPException(status_code=404, detail=f"Tipo conteudo {sg_tipo_conteudo} não Encontrado")

    resultados = dao.list_conteudos_por_tipo(db, cd_tipo_conteudo=tipo_conteudo.cd_tipo_conteudo)
    
    return resultados

@app.get("/conteudos/{cd_conteudo}", response_model=schemas.ConteudoReport,  tags=['Front-end'])
def get_conteudo(cd_conteudo : int, db: Session = Depends(get_db)):

    conteudo = dao.get_conteudo(db, cd_conteudo=cd_conteudo)
    if conteudo is None:
        raise HTTPException(status_code=404, detail=f"Conteudo {cd_conteudo} não Encontrado")
    
    return conteudo

@app.get("/conteudos/{cd_conteudo}/imagem", tags=['Front-end'], 
        response_class=StreamingResponse)
def img_conteudo(cd_conteudo : int, db: Session = Depends(get_db)):


    conteudo = dao.get_conteudo(db, cd_conteudo=cd_conteudo)
    if conteudo is None:
        raise HTTPException(status_code=404, detail=f"Conteudo {cd_conteudo} não Encontrado")
    elif not conteudo.aq_conteudo:
        raise HTTPException(status_code=404, detail=f"Conteudo {cd_conteudo} não possui imagem")

    io = image_conteudo(conteudo)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="image"
       )
    
    response.headers["Content-Disposition"] = f"attachment; filename=conteudo_{conteudo.cd_conteudo}.img"

    return response


@app.get("/conteudos/{cd_conteudo}/arquivo", tags=['Front-end'], 
        response_class=StreamingResponse)
def arq_conteudo(cd_conteudo : int, db: Session = Depends(get_db)):


    conteudo = dao.get_conteudo(db, cd_conteudo=cd_conteudo)
    if conteudo is None:
        raise HTTPException(status_code=404, detail=f"Conteudo {cd_conteudo} não Encontrado")
    elif not conteudo.aq_imagem_conteudo:
        raise HTTPException(status_code=404, detail=f"Conteudo {cd_conteudo} não possui arquivo")

    io = arquivo_conteudo(conteudo)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="PDF"
       )
    
    response.headers["Content-Disposition"] = f"attachment; filename=conteudo_{conteudo.cd_conteudo}.pdf"

    return response

