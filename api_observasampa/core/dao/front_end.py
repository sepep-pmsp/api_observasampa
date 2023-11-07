from sqlalchemy.orm import Session
from sqlalchemy import distinct
from sqlalchemy import func
from typing import List

from ..schemas.transformacoes import parse_formula, get_var_names
from ..models import front_end as models
from ..models import basic as basicmodels
from ..schemas import front_end as schemas
from . import basic as basicdao

from .filtros import get_lst_indicadores, sanitize_and_truncate, format_resultados_front

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

def set_next_previous_conteudo(db: Session, conteudo:models.Conteudo)->models.Conteudo:

    conteudos_mesmo_tipo = list_conteudos_por_tipo(db, cd_tipo_conteudo=int(conteudo.cd_tipo_conteudo))
    for i, cont in enumerate(conteudos_mesmo_tipo):

        if cont.cd_conteudo == conteudo.cd_conteudo:
            #se for o primeiro, o previous eh o ultimo
            if i == 0:
                conteudo.__setattr__('previous', None)
            else:
                conteudo.__setattr__('previous', conteudos_mesmo_tipo[i-1].cd_conteudo)
            if i == len(conteudos_mesmo_tipo):
                conteudo.__setattr__('next', None)
            else:
                conteudo.__setattr__('next', conteudos_mesmo_tipo[i+1].cd_conteudo)

def get_conteudo(db: Session, cd_conteudo: int):

    model = models.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_conteudo==cd_conteudo)

    conteudo = query.first()

    set_next_previous_conteudo(db, conteudo)

    return conteudo

def get_arq_tema(db: Session, cd_tema: int):

    model = basicmodels.Tema
    query = db.query(model)
    query = query.filter(model.cd_tema==cd_tema)

    return query.first()


def get_param_sistema(db: Session, param_type:str):

    tipos = {'equipe' : 'TX_MD_INSTITUCIONAL_TITULO',
            'footer' : 'TX_MD_INSTITUCIONAL_RESUMO',
            'institucional' : 'TX_MD_INSTITUCIONAL_COMPLETO'}

    chave = tipos[param_type]
    model = models.ParametrosSistema
    query = db.query(model)

    query = query.filter(model.cd_chave_parametro==chave)
    r = query.first()

    return r.vl_chave_parametro

def get_txt_institucional(db: Session):

    dados = {
    "sections" : [
            {"title" : "<h2>ObservaSampa</h2>",
            "body" : get_param_sistema(db, 'institucional')
        },
            {"title" : "<h2>Equipe</h2>",
            "body" : get_param_sistema(db, 'equipe')
        }
        ],
    "footer" : get_param_sistema(db, 'footer')
    }

    return dados

def get_ficha_indicador(db: Session, cd_indicador: int):

    indicador = basicdao.get_indicador(db, cd_indicador)
    if indicador is None:
        return None
    
    #colocando os resultados
    resultados = basicdao.resultados_indicador(db, cd_indicador)
    indicador.__setattr__('resultados', resultados)

    #agora vamos ter que substituir as variaveis
    #porque a tabela cross indicador_variavel nao está mais sendo utilizada
    #para isso, vamos ter que parsear a formula do indicador
    formula = indicador.dc_formula_indicador
    formula = parse_formula(formula)
    variaveis = get_var_names(formula, return_vars=True)
    indicador.__setattr__('variaveis', variaveis)

    return indicador

def search_indicador_nome(db: Session, query, nom_substring : str):

    nom_substring = nom_substring.lower().strip()

    model = basicmodels.Indicador
    query = query.filter(func.lower(model.nm_indicador).contains(nom_substring))

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

    r = query.all()
    r = format_resultados_front(r)

    return r
