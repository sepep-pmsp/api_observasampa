import json
from json import JSONDecodeError
from bs4 import BeautifulSoup

from ..utils.data_munging import remover_acentos

def padrao_nome_regiao(nome):

    lower = nome.lower()
    sem_acento = remover_acentos(lower)
    upper = sem_acento.upper()

    return upper

def parse_formula(formula):

    try:
        parsed = []
        formula = json.loads(formula)
        for item in formula:
            parsed.append(item.get('caractere', ''))

        return ' '.join(parsed)

    except (JSONDecodeError, ValueError):
        return formula

def parse_fonte(fonte):

    try:
        parsed = []
        fonte = json.loads(fonte)
        for item in fonte:
            parsed.append(item.get('nm_fonte', ''))

        return '; '.join(parsed)
        
    except (JSONDecodeError, ValueError):
        return fonte

def html_sanitizer(v):

    soup = BeautifulSoup(v)
    allowed = {'h1', 'h2', 'h3', 'h4', 'hr', 'p', 'a', 'table', 'td', 'tr', 'th'}
    for tag in soup.find_all(name=True):
        if tag.name not in allowed:
            tag.name = 'p'
        attrs = list(tag.attrs.keys())
        for attribute in attrs:
            if attribute != 'name':
                del tag[attribute]

    return soup.prettify()
            
