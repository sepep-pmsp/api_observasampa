


def resultados_por_nivel(resultados, nivel):
    
    niveis = {'Distrito', 'Município', 'Subprefeitura'}
    if nivel not in niveis:
        raise ValueError(f'Nivel {nivel} must be in {niveis}')
    
    #achar uma forma mais performatica de fazer
    filtrado = [r for r in resultados
                 if r.regiao.nivel.dc_nivel_regiao==nivel]
    
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

