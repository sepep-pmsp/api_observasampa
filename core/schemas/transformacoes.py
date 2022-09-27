import json
from json import JSONDecodeError

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