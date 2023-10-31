import json
from json import JSONDecodeError
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
import numpy as np

from ..utils.data_munging import remover_acentos
from ..dao import get_db_obj
from ..dao.basic import get_variavel

def padrao_nome_regiao(nome):

    lower = nome.lower()
    sem_acento = remover_acentos(lower)
    upper = sem_acento.upper()

    return upper

def parse_formula(formula):

    try:
        parsed = []
        formula_load = json.loads(formula)
        if formula_load is None:
            return ''
        for item in formula_load:
            parsed.append(item.get('caractere', ''))

        return ' '.join(parsed)

    except (JSONDecodeError, ValueError):
        if formula is None:
            return ''
    return str(formula)

def get_var_names(formula, return_vars=False):

    db = get_db_obj()
    formula_nova = []
    vars = []
    for item in formula.split(' '):
        if item.lower().startswith('v'):
            var_obj = get_variavel(db, nm_resumido_variavel=item)
            vars.append(var_obj)
            item = var_obj.nm_completo_variavel
            #envelopa em aspas simples
            item = f"'{item}'"
        formula_nova.append(item)

    db.close()
    if return_vars:
        return vars

    return ' '.join(formula_nova)

def parse_fonte(fonte):

    try:
        parsed = []
        fonte_load = json.loads(fonte)
        if fonte_load is None:
            return ''
        for item in fonte_load:
            parsed.append(item.get('nm_fonte', ''))
        print(parsed)
        return '; '.join(parsed)
        
    except (JSONDecodeError, ValueError):
        if fonte is None:
            return ''
    return str(fonte)

def html_sanitizer(v):

    soup = BeautifulSoup(v)
    allowed = {'h1', 'h2', 'h3', 'h4', 'h5', 'hr', 'p', 'a', 'table', 'td', 'tr', 'th',
                'b', 'i', 'span', 'br', 'a', 'br'}
    allowed_attr = {'name', 'href'}
    for tag in soup.find_all(name=True):
        if tag.name not in allowed:
            tag.name = 'p'
        attrs = list(tag.attrs.keys())
        for attribute in attrs:
            if attribute not in allowed_attr:
                del tag[attribute]

    return soup.prettify()
            

def fill_na_resultados(formatados:dict)->dict:

    formatados_final = {}
    for nivel_name, nivel_values in formatados.items():
        df = pd.DataFrame(nivel_values).fillna('')
        formatados_final[nivel_name] = df.to_dict()

    return formatados_final

def ordenar_results_por_nivel_regiao(formatados:dict)->dict:

    ordem = {
        'País' : 1,
        'Estado' : 2,
        'Município' : 3,
        'Subprefeitura' : 4,
        'Distrito' : 5,
    }

    em_ordem = OrderedDict()
    
    niveis_ordenados = sorted(list(formatados.keys()), key = lambda x: ordem.get(x, 1000), reverse=False)

    for nivel in niveis_ordenados:
        em_ordem[nivel]=formatados[nivel]
    
    return em_ordem


def format_resultados_front(v):

    formatados = {}
    for r in v:
        nivel = r.regiao.nivel.dc_nivel_regiao
        regiao = r.regiao.nm_regiao
        #titlecase para ficar mais bonito
        regiao = str(regiao).title()
        periodo = r.periodo.vl_periodo
        valor = r.vl_indicador_resultado

        if nivel not in formatados:
            formatados[nivel] = {}
        if regiao not in formatados[nivel]:
            formatados[nivel][regiao] = {}
        
        #se tirver mais de um valor por regiao por periodo
        #vai pegar o ultimo, o que sinceramente ateh eh bom
        #porque nao deveria ter mais de um valor
        formatados[nivel][regiao][periodo] = valor
    
    formatados_final = fill_na_resultados(formatados)
    formatados_final = ordenar_results_por_nivel_regiao(formatados_final)

    return formatados_final


def filtrar_temas_front(v):

    temas_validos = [tema
                     for tema in v
                     if tema.cd_tipo_situacao == 1]
    
    return temas_validos


def arrumar_datatypes_df(df:pd.DataFrame)->pd.DataFrame:

    #transformando colunas numericas
    cols_dados = [col for col in df.columns if col not in ('região', 'nivel_regional', 'indicador')]
    for col in cols_dados:
        #lidando com os zeros
        df[col] = df[col].apply(lambda x: '0' if x == 0 else x)
        df[col] = df[col].astype(str)
        #lidando com as strings vazias
        df[col] = df[col].apply(lambda x: np.nan if (x == 'None' or x == '' or x == 'nan') else x)
        try:
            df[col] = df[col].astype(int)
        except ValueError:
            try:
                df[col] = df[col].astype(float)
            except ValueError as e:
                #mantem como string mesmo
                print(f'dei erro: {e} - na coluna {col}')

    return df


def ordem_colunas(col:str)->int:

        ordem = {
        'região' : 1,
        'nivel_regional' : 2,
        'indicador' : 3
        }

        try:
            return ordem[col]
        except KeyError:
            return int(col)
            


def transformar_df(indicador):

    resultados = indicador.resultados
    formatados = format_resultados_front(resultados)
    
    dfs = []
    for nivel, valores in formatados.items():
        df = pd.DataFrame(valores)
        df = df.T
        df['nivel_regional'] = nivel
        df['indicador'] = indicador.nm_indicador
        df = df.reset_index()
        df = df.rename({'index' : 'região'}, axis=1)

        #ordena as colunas
        cols = sorted(df.columns, key=ordem_colunas)
        df = df[cols]
        dfs.append(df)
    
    df = pd.concat(dfs)
    
    #deixa os dados em float quando couber
    df = arrumar_datatypes_df(df)

    return df