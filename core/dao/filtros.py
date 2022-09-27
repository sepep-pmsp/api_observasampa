
from core.models.database import SessionLocal
import core.models.basic as basicmodels
import core.models.front_end as front_end_models

from io import BytesIO

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def resultados_por_nivel(resultados, nivel):
    
    niveis = {'Distrito', 'Município', 'Subprefeitura'}
    if nivel not in niveis:
        raise ValueError(f'Nivel {nivel} must be in {niveis}')
    
    #achar uma forma mais performatica de fazer
    filtrado = [r for r in resultados
                 if r.regiao.nivel.dc_nivel_regiao==nivel]
    
    return filtrado

def resultados_por_nivel_cd(resultados, cd_nivel_regiao):

    filtrado = [r for r in resultados
                if r.regiao.nivel.cd_nivel_regiao == cd_nivel_regiao]

    return filtrado

def periodo_resultado(r):

    return r.periodo.vl_periodo

def regiao_resultado(r):

    return r.regiao.nm_regiao

def valor_resultado(r):

    return r.vl_indicador_resultado

def valor_resultado_var(r):

    return r.vl_variavel_resultado

def nivel_regiao_resultado(r):

    return r.regiao.nivel.dc_nivel_regiao


def image_conteudo(r):

    #ESTA INVERTIDO NO BANCO KKK
    img = r.aq_conteudo
    io = BytesIO(img)

    return io

def arquivo_conteudo(r):

    #MESMO DO ANTERIOR: INVERTERAM IMG E ARQUIVO
    arq = r.aq_imagem_conteudo
    io = BytesIO(arq)

    return io

def icone_tema(r):

    arq = r.aq_icone_tema
    io = BytesIO(arq)

    return io


def nomes_niveis():

    db_gen = get_db()
    db = next(db_gen)
    model = basicmodels.NivelRegiao
    query = db.query(model)
    niveis = query.all()

    return [n.sg_nivel_regiao for n in niveis]

def nomes_temas():

    db_gen = get_db()
    db = next(db_gen)
    model = basicmodels.Tema
    query = db.query(model)
    query = query.filter(model.cd_tipo_situacao==1)
    temas = query.all()

    return [tema.nm_tema for tema in temas]

def siglas_tipo_conteudo():

    db_gen = get_db()
    db = next(db_gen)
    model = front_end_models.TipoConteudo
    query = db.query(model)
    tipos = query.all()

    return [tipo.sg_tipo_conteudo for tipo in tipos]