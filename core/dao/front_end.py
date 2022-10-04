from sqlalchemy.orm import Session

from ..models import front_end as models
from ..models import basic as basicmodels
from ..schemas import front_end as schemas
from ..schemas import basic as basicschemas
from . import basic as basicdao

from .filtros import get_lst_indicadores

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
                            limit : int = None):

    model = models.Conteudo
    query = db.query(model)
    query = query.filter(model.cd_tipo_conteudo==cd_tipo_conteudo)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.order_by(model.dt_atualizacao.desc())
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

def list_indicadores_cd(db: Session, lst_cd_indicadores : list=None, only_codes = False):


    model = basicmodels.Indicador
    query = db.query(model)
    #garantir apenas os indicadores ativos
    query = query.filter(model.cd_tipo_situacao==1)
    #se estiver vazio, vai direto
    if lst_cd_indicadores is None or len(lst_cd_indicadores)==0:
        if only_codes:
            return get_lst_indicadores(query)
        else:
            return query
    #se nao, 
    query = query.filter(model.cd_indicador.in_(lst_cd_indicadores))

    if only_codes:
        return get_lst_indicadores(query)

    return query


def search_indicador_nome(db: Session, nom_substring : str = None, lst_indicadores : list=None):
    
    if nom_substring is None or len(nom_substring)==0 or nom_substring=='string':
        return list_indicadores_cd(db, lst_indicadores, only_codes=True)
    
    model = basicmodels.Indicador
    query = list_indicadores_cd(db, lst_indicadores, only_codes=False)
    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.nm_indicador.contains(nom_substring))

    return get_lst_indicadores(query)

def search_indicador_tema(db: Session, cd_tema_list : list=None,  lst_indicadores : list=None):

   
    if cd_tema_list is None or len(cd_tema_list)==0:
        return list_indicadores_cd(db, lst_indicadores, only_codes=True)

    else:
        #primeiro precisamos buscar os indicadores daquele tema
        query_aux = db.query(basicmodels.tema_indicador)
        query_aux = query_aux.join(basicmodels.Tema)
        query_aux = query_aux.join(basicmodels.Indicador)
        query_aux = query_aux.filter(basicmodels.Tema.cd_tema.in_(cd_tema_list)) 
        cd_indicadores_tema = [r.cd_indicador for r in query_aux.all()]

        #depois pegamos nossos indicadores já filtrados
        #e filtramos eles para selecionar os indicadores do tema
        query = list_indicadores_cd(db, lst_indicadores, only_codes=False)
        model = basicmodels.Indicador
        query = query.filter(model.cd_indicador.in_(cd_indicadores_tema))

        return get_lst_indicadores(query)

def search_indicador_regiao(db: Session, cd_regiao_list:list = None, lst_indicadores : list=None):


    if cd_regiao_list is None or len(cd_regiao_list)==0:
        return list_indicadores_cd(db, lst_indicadores, only_codes=True)

    query = list_indicadores_cd(db, lst_indicadores, only_codes=False)
    query = query.join(basicmodels.ResultadoIndicador, 
        basicmodels.Indicador.cd_indicador == basicmodels.ResultadoIndicador.cd_indicador)
    query = query.filter(basicmodels.ResultadoIndicador.cd_regiao.in_(cd_regiao_list))
    
    return get_lst_indicadores(query)
    

def search_indicador_nivel_regiao(db: Session, cd_nivel_regiao_list : list=None, lst_indicadores : list=None):

    if cd_nivel_regiao_list is None or len(cd_nivel_regiao_list)==0:
        return list_indicadores_cd(db, lst_indicadores, only_codes=True)

    #primeiro precisamos listar as regioes para cada nivel
    query_aux = db.query(basicmodels.Regiao)
    query_aux = query_aux.filter(basicmodels.Regiao.cd_nivel_regiao.in_(cd_nivel_regiao_list))
    regioes_nivel = query_aux.all()
    regioes_nivel = [regiao.cd_regiao for regiao in regioes_nivel] 

    #e filtramos nossos indicadores para aquela regiao
    query = list_indicadores_cd(db, lst_indicadores, only_codes=False)
    query = query.join(basicmodels.ResultadoIndicador, 
        basicmodels.Indicador.cd_indicador == basicmodels.ResultadoIndicador.cd_indicador)
    query = query.filter(basicmodels.ResultadoIndicador.cd_regiao.in_(regioes_nivel))
    
    return get_lst_indicadores(query)

def search_temas_dos_indicadores(db: Session, lst_cd_indicadores : list = None, cd_tema_list: list =  None):

    model = basicmodels.Tema
    query = db.query(model)

    if lst_cd_indicadores is None or len(lst_cd_indicadores)==0:
        query = query.filter(model.cd_tipo_situacao==1)
        return query.all()
    
    query_aux = db.query(basicmodels.tema_indicador)
    query_aux = query_aux.join(model)
    query_aux = query_aux.join(basicmodels.Indicador)
    query_aux = query_aux.filter(basicmodels.Indicador.cd_indicador.in_(lst_cd_indicadores))
    cd_temas_filtro = [item.cd_tema for item in query_aux.all() if item.cd_tipo_situacao==1]

    if cd_tema_list is not None and len(cd_tema_list)>0:
        query = query.filter(model.cd_tema.in_(cd_tema_list))

    query = query.filter(model.cd_tipo_situacao==1)
    query = query.filter(model.cd_tema.in_(cd_temas_filtro))

    return query.all()

def search_nivel_regiao_dos_indicadores(db: Session, cd_regiao_list : list = None, cd_nivel_regiao_list : list = None):

    model = basicmodels.NivelRegiao
    query = db.query(model)
    
    if cd_regiao_list is None or len(cd_regiao_list)==0:
        #nivel regiao nao tem tipo de situacao
        #query = query.filter(model.cd_tipo_situacao==1)
        return query.all()

    query_aux = db.query(basicmodels.Regiao)
    query_aux = query_aux.filter(basicmodels.Regiao.cd_regiao.in_(cd_regiao_list))
    regioes = query_aux.all()
    cd_nivel_regiao_2 = [r.cd_nivel_regiao for r in regioes]

    if cd_nivel_regiao_list is not None and len(cd_nivel_regiao_list)>0:
        query = query.filter(model.cd_nivel_regiao.in_(cd_nivel_regiao_list))

    query = query.filter(model.cd_nivel_regiao.in_(cd_nivel_regiao_2))

    return query.all()

def search_regioes_dos_indicadores_e_niveis(db:Session, lst_cd_nivel_regiao: list=None,
                                             cd_regiao_list: list=None):

    model = basicmodels.Regiao
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)

    if lst_cd_nivel_regiao is None or len(lst_cd_nivel_regiao)==0:
        #se estiver vazio, pegamos todos os possíveis
        niveis_regionais = search_nivel_regiao_dos_indicadores(db)
        lst_cd_nivel_regiao = [n.cd_nivel_regiao for n in niveis_regionais]

    query = query.filter(model.cd_nivel_regiao.in_(lst_cd_nivel_regiao))

    if cd_regiao_list is not None and len(cd_regiao_list)>0:
        query = query.filter(model.cd_regiao.in_(cd_regiao_list))

    return query.all()


def search_indicadores(db: Session, search : schemas.SearchIndicador)->schemas.SearchIndicador:


    #primeiro verificamos se já não há indicadores selecionados
    #se não houver, vamos retornar uma lista com os códigos de todos os indicadores
    print('puxando indicadores')
    lst_cd_indicadores = search.indicadores or []
    lst_cd_indicadores = [indi.cd_indicador for indi in lst_cd_indicadores]
    lst_cd_indicadores = list_indicadores_cd(db, lst_cd_indicadores, only_codes=True)

    #filtramos a lista pelo nome do indicador
    print('buscando pelo nome')
    nom_substring = search.busca_textual
    lst_cd_indicadores = search_indicador_nome(db, nom_substring, lst_cd_indicadores)

    #depois pelos temas
    print('pelo tema')
    cd_tema_list = search.temas or []
    cd_tema_list = [t.cd_tema for t in cd_tema_list]
    lst_cd_indicadores = search_indicador_tema(db, cd_tema_list, lst_cd_indicadores)

    #em seguida pelo nivel de regiao
    print('pelo nivel de regiao')
    cd_nivel_regiao_list = search.niveis_regionais or []
    cd_nivel_regiao_list = [n.cd_nivel_regiao for n in cd_nivel_regiao_list]
    lst_cd_indicadores = search_indicador_nivel_regiao(db, cd_nivel_regiao_list, lst_cd_indicadores)

    #por ultimo pela regiao
    print('pela regiao')
    cd_regiao_list = search.regioes or []
    cd_regiao_list = [r.cd_regiao for r in cd_regiao_list]
    lst_cd_indicadores = search_indicador_regiao(db, cd_regiao_list, lst_cd_indicadores)


    #agora fazemos o "caminho de volta"
    #e filtramos os dados de acordo com os indicadores encontrados
    #e recriamos os objetos de busca
    # com o detalhe que sempre mantemos o filtro anterior
    # entrao se ja tinha selecionado uma Sub, vai retornar soh os distritos dessa sub
    print('pegando os temas')
    temas = search_temas_dos_indicadores(db, lst_cd_indicadores, cd_tema_list)
    
   
    print('pegando os niveis de regiao')
    niveis_regionais = search_nivel_regiao_dos_indicadores(db, cd_regiao_list, cd_nivel_regiao_list)
    print('pegando as regioes')
    lst_cd_nivel_regiao = [n.cd_nivel_regiao for n in niveis_regionais]
    regioes = search_regioes_dos_indicadores_e_niveis(db, lst_cd_nivel_regiao, cd_regiao_list)
    
    #agora podemos atualizar os niveis regionais para baterem com as regioes
    niveis_regioes = set([r.cd_nivel_regiao for r in regioes])
    niveis_regionais = [n for n in niveis_regionais if n.cd_nivel_regiao in niveis_regioes]

    #e geramos os indicadores
    print('pegando os indicadores')
    query_indicadores = list_indicadores_cd(db, lst_cd_indicadores, only_codes=False)
    indicadores = query_indicadores.all()

    #por ultimo, construimos a resposta
    print('construindo a resposta')
    response = schemas.SearchIndicador(
        #retornamos a mesma busca feita anteriormente
        busca_textual = search.busca_textual,
        #os indicadores filtrados
        indicadores = indicadores,
        #os parametros de busca atualizados
        temas = temas,
        niveis_regionais = niveis_regionais,
        regioes = regioes
    )

    print('retornando a resposta')

    #e retornamos ela
    return response