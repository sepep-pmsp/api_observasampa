from fastapi import APIRouter, Query
import pandas as pd

from typing import List, Union, Dict

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.responses import StreamingResponse, FileResponse

from core.dao import get_db
from core.dao import front_end as dao
from core.dao import basic as basicdao
from core.models import front_end as models
from core.models import basic as basicmodels
from core.schemas import front_end as schemas
from core.schemas import basic as basicschemas
from core.schemas.transformacoes import transformar_df
from core.models.database import SessionLocal, engine

from core.dao.filtros import siglas_tipo_conteudo, arquivo_conteudo, image_conteudo, icone_tema, image_dashboard


app = APIRouter()

TIPOS_CONTEUDO = siglas_tipo_conteudo()


@app.get("/dashboards/", response_model=List[schemas.DashboardSimples], tags=['Front-end'])
def read_dashboard(db: Session = Depends(get_db)):

    dashs = dao.list_dash(db)
    return dashs 

@app.get("/dashboards/{cd_dashboard}", response_model=schemas.Dashboard,  tags=['Front-end'])
def get_conteudo(cd_dashboard : int, db: Session = Depends(get_db)):

    dash = dao.get_dashboard_full(db, cd_dashboard)
    if dash is None:
        raise HTTPException(status_code=404, detail=f"Dashboard {cd_dashboard} não Encontrado")
    
    return dash 

@app.get("/dashboards/{cd_dashboard}/imagem", tags=['Front-end'], 
        response_class=StreamingResponse)
def img_dashboard(cd_dashboard : int, db: Session = Depends(get_db)):


    dash = dao.get_dashboard_full(db, cd_gerenciador_dashboard=cd_dashboard)
    if dash is None:
        raise HTTPException(status_code=404, detail=f"Dashboard {cd_dashboard} não Encontrado")
    elif not dash.aq_icone_gerenciador_dashboard:
        raise HTTPException(status_code=404, detail=f"Dashboard {cd_dashboard} não possui imagem")

    io = image_dashboard(dash)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="image/png"
       )
    
    #se quiser retornar como download descomenta abaixo
    #response.headers["Content-Disposition"] = f"attachment; filename=dashboard_{dash.cd_gerenciador_dashboard}.png"

    return response   

@app.get("/carrossel/", response_model=List[schemas.DashboardCarrossel], tags=['Front-end'])
def read_dashboard(db: Session = Depends(get_db)):

    dashs = dao.list_dash_carrossel(db)

    for dash in dashs:
        #achar uma maneira de inspecionar o endpoint direto
        link_img = app.url_path_for('img_dashboard', cd_dashboard=dash.cd_gerenciador_dashboard)
        dash.__setattr__('link_img', link_img)

    return dashs    

@app.get("/tipo_conteudo/", response_model=List[schemas.TipoConteudo], tags=['Front-end'])
def read_tipo_conteudos(db: Session = Depends(get_db)):

    tipos = dao.list_tipos_conteudo(db)
    return tipos

@app.get("/conteudos/", response_model=List[schemas.ConteudoBase],  tags=['Front-end'])
def read_conteudos(sg_tipo_conteudo : str = Query(enum=TIPOS_CONTEUDO), truncate : bool = False, max_chars : int = 100,
                        skip : int = None, limit : int = None, db: Session = Depends(get_db)):

    tipo_conteudo = dao.get_tipo_conteudo(db, sg_tipo_conteudo=sg_tipo_conteudo)
    if tipo_conteudo is None:
        raise HTTPException(status_code=404, detail=f"Tipo conteudo {sg_tipo_conteudo} não Encontrado")

    resultados = dao.list_conteudos_por_tipo(db, cd_tipo_conteudo=tipo_conteudo.cd_tipo_conteudo,
                                            skip = skip, limit = limit, truncate=truncate, max_chars=max_chars)

    for r in resultados:
        if r.aq_imagem_conteudo:
            r.__setattr__('has_arq', True)
        if r.aq_conteudo:
            r.__setattr__('has_img', True)
    
    return resultados

@app.get("/conteudos/{cd_conteudo}", response_model=schemas.ConteudoReport,  tags=['Front-end'])
def get_conteudo(cd_conteudo : int, db: Session = Depends(get_db)):

    conteudo = dao.get_conteudo(db, cd_conteudo=cd_conteudo)

    if conteudo is None:
        raise HTTPException(status_code=404, detail=f"Conteudo {cd_conteudo} não Encontrado")
    if conteudo.aq_imagem_conteudo:
        conteudo.__setattr__('has_arq', True)
    if conteudo.aq_conteudo:
        conteudo.__setattr__('has_img', True)

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
                            media_type="image/png"
       )
    
    #se quiser retornar como download
    #response.headers["Content-Disposition"] = f"attachment; filename=conteudo_{conteudo.cd_conteudo}.png"

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
                            media_type="application/pdf"
       )
    
    response.headers["Content-Disposition"] = f"attachment; filename=conteudo_{conteudo.cd_conteudo}.pdf"

    return response

@app.get("/ficha_indicador/{cd_indicador}", response_model=schemas.FichaIndicador,  tags=['Front-end'])
def ficha_indicador(cd_indicador: int, db: Session = Depends(get_db)):

    indicador = dao.get_ficha_indicador(db, cd_indicador=cd_indicador)
    if indicador is None:
        raise HTTPException(status_code=404, detail=f"Indicador {cd_indicador} Não Encontrado")
    return indicador

@app.get("/temas/", response_model=List[schemas.TemaBase], tags=['Front-end'])
def read_temas(db: Session = Depends(get_db)):

    temas = basicdao.list_temas(db)
    return temas

@app.get("/temas/{cd_tema}/icone", tags=['Front-end'], 
        response_class=StreamingResponse)
def img_tema(cd_tema : int, db: Session = Depends(get_db)):


    tema = dao.get_arq_tema(db, cd_tema=cd_tema)
    if tema is None:
        raise HTTPException(status_code=404, detail=f"Tema {cd_tema} não Encontrado")
    elif not tema.aq_icone_tema:
        raise HTTPException(status_code=404, detail=f"Tema {cd_tema} não possui arquivo")

    io = icone_tema(tema)

    response = StreamingResponse(iter([io.getvalue()]),
                            media_type="img/png"
       )
    
    response.headers["Content-Disposition"] = f"attachment; filename=icone_tema_{tema.cd_tema}.png"

    return response

@app.get("/txt_institucional/", response_model=schemas.Institucional, tags=['Front-end'])
def get_txt_institucional(db: Session = Depends(get_db)):

    institucional = dao.get_txt_institucional(db)
    return institucional

@app.get("/regioes/niveis/", response_model=List[basicschemas.NivelRegiao], tags=['Front-end'])
def list_niveis(db: Session = Depends(get_db)):

    niveis = basicdao.list_niveis_regioes(db)
    return niveis

@app.get("/regioes/", response_model=List[basicschemas.Regiao], tags=['Front-end'])
def list_regioes(cd_nivel_regiao: int = None, skip: int = None, limit: int = None, db: Session = Depends(get_db)):

    if cd_nivel_regiao:
        nivel = basicdao.get_nivel_regiao(db, cd_nivel_regiao = cd_nivel_regiao)
        if nivel is None:
            raise HTTPException(status_code=404, detail=f'Nivel {cd_nivel_regiao} não existente')
        regioes = basicdao.list_regioes_nivel(db, cd_nivel_regiao = nivel.cd_nivel_regiao, skip=skip, limit=limit)
        return regioes

    regioes = basicdao.list_regioes(db, skip=skip, limit=limit)
    return regioes

@app.get("/dados_home_page", response_model=List[schemas.DadosHomePage],  tags=['Front-end'])
def dados_home():
    '''Mock endpoint que depois deve puxar os dados do banco.
    Esta sendo feito assim para permitir atualizacao dos dados na homepage posteriormente.'''

    dados = [ 
        { 
            "titulo": "População 2022", 
            "valor": "11.451.999 habitantes", 
            "fonte": "IBGE – Censo 2022" 
        },
                 { 
            "titulo": "Área do Município", 
            "valor": "1.527,69 km²", 
            "fonte": "SMUL/PMSP" 
        },
        { 
            "titulo": "Produto Interno Bruto (2021)", 
            "valor": "R$ 829,0 bilhões", 
            "fonte": "IBGE" 
        },
        { 
            "titulo": "Participação no PIB do Brasil (2021)", 
            "valor": "9,2%", 
            "fonte": "IBGE" 
        }

    ] 
    
    return dados

@app.post("/search_indicadores", response_model=List[schemas.IndicadorBaseFront], tags=['Front-end'])
def post_search_indicador(search:schemas.SearchIndicador, skip: int = None, limit: int = None, db: Session= Depends(get_db)):

    response = dao.search_indicadores(db, search, skip, limit)

    return response

@app.post("/search_resultados_indicador", response_model=Dict, tags=['Front-end'])
def post_search_indicador(search:schemas.SearchResultadosIndicador, skip: int = None, limit: int = None, db: Session= Depends(get_db)):

    response = dao.search_resultados_indicador(db, search, skip, limit)

    return response

@app.get("/download_resultados_indicador",  response_class=FileResponse, tags=['Front-end'])
def download_resultados(cd_indicador: int, db: Session = Depends(get_db)):

    indicador = dao.get_ficha_indicador(db, cd_indicador=cd_indicador)
    if indicador is None:
        raise HTTPException(status_code=404, detail=f"Indicador {cd_indicador} Não Encontrado")

    df = transformar_df(indicador)
    print(df.dtypes)
    return StreamingResponse(
        iter([df.to_csv(sep=';', encoding='latin-1', decimal=',', quotechar='"')]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
    )


