import json
from json import JSONDecodeError
from bs4 import BeautifulSoup
import pandas as pd

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

    return formatados_final


def filtrar_temas_front(v):

    temas_validos = [tema
                     for tema in v
                     if tema.cd_tipo_situacao == 1]
    
    return temas_validos