from sqlalchemy.orm import Session
from sqlalchemy import distinct

from ..models import front_end as models
from ..models import basic as basicmodels
from ..schemas import front_end as schemas
from ..schemas import basic as basicschemas
from . import basic as basicdao

from .filtros import get_lst_indicadores, sanitize_and_truncate

def list_dash(db: Session):

    model = basicmodels.Dashboard
    query = db.query(model)
    query=query.filter(model.in_publicado == 'S')
    query=query.filter(model.cd_status_dashboard=='A')
    query = query.order_by(model.nr_ordem_exibicao)

    return query.all()

def get_dashboard_full(db: Session, cd_gerenciador_dashboard:str):

    model = basicmodels.Dashboard
    query = db.query(model)
    query = query.filter(model.cd_gerenciador_dashboard == cd_gerenciador_dashboard)
    #garantir que vai mostrar só publicado, mesmo se o cara advinhe o codigo
    query=query.filter(model.in_publicado == 'S')

    return query.first()

def list_dash_carrossel(db: Session):

    model = basicmodels.Dashboard
    query = db.query(model)
    query=query.filter(model.in_publicado == 'S')
    query=query.filter(model.cd_status_dashboard=='A')
    query = query.order_by(model.nr_ordem_exibicao)

    return query.limit(5).all()

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
    query = query.order_by(model.dt_atualizacao.desc())
    
    return query.all()

def list_conteudos_por_tipo(db: Session, cd_tipo_conteudo: int, skip: int = None, 
                            limit : int = None, truncate: bool = False, max_chars: int = 100):

    model = models.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_conteudo==cd_tipo_conteudo)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.order_by(model.dt_atualizacao.desc())
    if skip or limit:
        skip = skip or 0
        limit = limit or 100
        query = query.offset(skip).limit(limit)

    results = query.all()
    if truncate:
        for r in results:
            conteudo = r.tx_conteudo
            truncado = sanitize_and_truncate(conteudo, max_chars)
            r.__setattr__('txt_truncado', truncado)
    
    return results

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

def get_txt_institucional(db: Session):

    dados = {'titulo' : 'TX_MD_INSTITUCIONAL_TITULO',
            'resumo' : 'TX_MD_INSTITUCIONAL_RESUMO',
            'txt_completo' : 'TX_MD_INSTITUCIONAL_COMPLETO'}
    model = models.ParametrosSistema

    for attr_name, cd_chave in dados.items():
        query = db.query(model)
        query = query.filter(model.cd_chave_parametro==cd_chave)
        r = query.first()

        dados[attr_name] = r.vl_chave_parametro

    return dados

def get_ficha_indicador(db: Session, cd_indicador: int):

    indicador = basicdao.get_indicador(db, cd_indicador)
    resultados = basicdao.resultados_indicador(db, cd_indicador)

    indicador.__setattr__('resultados', resultados)

    return indicador

def search_indicador_nome(db: Session, query, nom_substring : str):
    
    model = basicmodels.Indicador
    query = query.filter(model.nm_indicador.contains(nom_substring))

    return query

def search_indicador_tema(db: Session, query, temas : list):

    query_aux = db.query(basicmodels.tema_indicador)
    query_aux = query_aux.join(basicmodels.Tema)
    query_aux = query_aux.join(basicmodels.Indicador)
    query_aux = query_aux.filter(basicmodels.Tema.cd_tema.in_(temas)) 
    cd_indicadores_tema = [r.cd_indicador for r in query_aux.all() if r.cd_tipo_situacao==1]

    model = basicmodels.Indicador
    query = query.filter(model.cd_indicador.in_(cd_indicadores_tema))

    return query

def search_indicador_nivel_regional(db: Session, query, niveis_regionais: list):

    query_aux = db.query(basicmodels.Regiao)
    query_aux = query_aux.filter(basicmodels.Regiao.cd_nivel_regiao.in_(niveis_regionais))
    query_aux = query_aux.with_entities(basicmodels.Regiao.cd_regiao)
    regioes_nivel = query_aux.all()
    regioes_nivel = [regiao.cd_regiao for regiao in regioes_nivel] 

    query_aux_2 = db.query(basicmodels.ResultadoIndicador)
    query_aux_2 = query_aux_2.filter(basicmodels.ResultadoIndicador.cd_regiao.in_(regioes_nivel))
    query_aux_2 = query_aux_2.with_entities(basicmodels.ResultadoIndicador.cd_indicador)
    query_aux_2 = query_aux_2.distinct(basicmodels.ResultadoIndicador.cd_indicador)
    cd_indicadores_nivel = [r.cd_indicador for r in query_aux_2.all()]
    model = basicmodels.Indicador
    query = query.filter(model.cd_indicador.in_(cd_indicadores_nivel))

    return query

def search_indicadores_regiao(db: Session, query, regioes: list):


    query_aux = db.query(basicmodels.ResultadoIndicador)
    query_aux = query_aux.filter(basicmodels.ResultadoIndicador.cd_regiao.in_(regioes))
    query_aux = query_aux.with_entities(basicmodels.ResultadoIndicador.cd_indicador)
    query_aux = query_aux.distinct(basicmodels.ResultadoIndicador.cd_indicador)
    cd_indicadores_regioes = [r.cd_indicador for r in query_aux.all()]

    model = basicmodels.Indicador
    query = query.filter(model.cd_indicador.in_(cd_indicadores_regioes))

    return query


def search_indicadores(db: Session, search : schemas.SearchIndicador, skip: int = None, limit: int=None):


    model = basicmodels.Indicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)

    nom_busca = search.busca_textual
    if nom_busca:
        query = search_indicador_nome(db, query, nom_busca)

    temas = search.cd_temas
    if temas:
        query = search_indicador_tema(db, query, temas)

    niveis_regionais = search.cd_niveis_regionais
    regioes = search.cd_regioes
    #soh busca nivel regional se nao especificar regiao
    if niveis_regionais and not regioes:
        query = search_indicador_nivel_regional(db, query, niveis_regionais)

    if regioes:
        query = search_indicadores_regiao(db, query, regioes)

    if skip or limit:
        skip = skip or 0
        limit = limit or 100
        query = query.offset(skip).limit(limit)

    return query.all()

def search_resultados_indicador(db: Session, search: schemas.SearchResultadosIndicador,
                        skip: int = None, limit: int = None):

    cd_indicador = search.cd_indicador

    model = basicmodels.ResultadoIndicador
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_indicador==cd_indicador)

    niveis_regionais = search.cd_niveis_regionais
    if niveis_regionais:

        model_regiao = basicmodels.Regiao
        query_aux = db.query(model_regiao)
        query_aux = query_aux.filter(model_regiao.cd_nivel_regiao.in_(niveis_regionais))
        cd_regioes = [r.cd_regiao for r in query_aux.all()]

        query = query.filter(model.cd_regiao.in_(cd_regioes))
    
    regioes = search.cd_regioes
    if regioes:

        query = query.filter(model.cd_regiao.in_(regioes))


    if skip or limit:
        skip = skip or 0
        limit = limit or 100
        query = query.offset(skip).limit(limit)

    return query.all()
